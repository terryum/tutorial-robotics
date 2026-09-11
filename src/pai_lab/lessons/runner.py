"""Run one real experiment and record independently checkable local evidence."""

from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.catalog import ROOT, resolve_lesson
from pai_lab.lessons.experiment import plot_trace, render
from pai_lab.lessons.specs import LESSON_SPECS
from pai_lab.local import write_json
from pai_lab.providers import provider_for
from pai_lab.readiness import gaps


@dataclass(frozen=True)
class LessonResult:
    lesson_id: str
    seed: int
    samples: int
    operation: str
    metric_name: str
    metric_value: float
    changed_metric_value: float
    units: str
    status: str
    verification: str
    safety_level: str
    artifact_digest: str
    artifacts: tuple[str, ...]


def implementation_status(identifier: str) -> str:
    try:
        return resolve_lesson(identifier).implementation
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        return str(
            next(
                item for item in provider.lessons() if str(item.id).lower() == identifier.lower()
            ).implementation
        )


def implementation_digest(identifier: str | None = None) -> str:
    if identifier is not None:
        from pai_lab.lessons.dependencies import dependency_digest

        return dependency_digest(identifier)

    files = sorted((ROOT / "src/pai_lab").rglob("*.py"))
    files += [
        ROOT / name
        for name in (
            "curriculum/catalog.json",
            "assets/model-lock.json",
            "assets/sources.json",
            "uv.lock",
        )
    ]
    digest = hashlib.sha256()
    for path in files:
        digest.update(str(path.relative_to(ROOT)).encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def run_lesson(
    identifier: str,
    *,
    output_dir: Path,
    seed: int = 7,
    samples: int = 64,
    headless: bool = True,
    variant: float = 1.0,
    parameters: dict[str, float] | None = None,
) -> Any:
    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        return provider.run(
            identifier, output_dir, samples, seed=seed, variant=variant, parameters=parameters or {}
        )
    if lesson.implementation != "implemented":
        raise NotImplementedError(f"{lesson.id}: reader_test_required")
    if samples < 8 or samples > 100000 or not np.isfinite(variant) or variant <= 0:
        raise ValueError("samples must be 8..100000; variant must be finite and positive")
    missing = gaps(lesson)
    if missing:
        raise FileNotFoundError("; ".join(missing))
    if lesson.stage == "hardware" and not headless:
        raise PermissionError("only offline command sink is available")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError("run directory is not empty; choose a new directory to preserve evidence")
    from pai_lab.lessons.parameters import resolve_parameters

    resolved = resolve_parameters(lesson.id, parameters or {}, variant)
    code_digest = implementation_digest(lesson.id)
    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(
        output_dir / "run.json",
        {
            "lesson": lesson.id,
            "status": "running",
            "started_at": datetime.now(UTC).isoformat(),
            "implementation_digest": code_digest,
        },
    )
    from pai_lab.lessons.inputs import inputs

    inputs.set([])
    spec = LESSON_SPECS[lesson.id]
    try:
        if lesson.id in {
            "core-rl-01",
            "core-fr3-07",
            "core-fr3-08",
            "core-data-01",
            "core-il-01",
            "core-aloha-01",
            "core-vla-01",
        }:
            from pai_lab.lessons.learning import run
        elif lesson.track in {"wuji", "dexterity", "g1"} and lesson.stage == "core":
            from pai_lab.lessons.hands import run
        elif lesson.stage == "core":
            from pai_lab.lessons.physics import run
        elif lesson.id in {"sim-deploy-01", "hw-common-01", "sim-enlight-02", "sim-wuji-02"}:
            from pai_lab.lessons.deployment import run
        else:
            from pai_lab.lessons.stacks import run
        from pai_lab.lessons import physics

        experiment = (
            physics.run(lesson.id, output_dir, seed, samples, variant, parameters=resolved)
            if resolved
            else run(lesson.id, output_dir, seed, samples, variant)
        )
        if code_digest != implementation_digest(lesson.id):
            raise RuntimeError("source changed during execution; preserve this run and restart")
        write_json(
            output_dir / "experiment.json",
            {
                "payload": experiment.payload,
                "checks": experiment.checks,
                "metric": experiment.metric,
                "variant": variant,
                "parameters": resolved,
                "requested_parameters": parameters or {},
            },
        )
        if not experiment.checks or not all(experiment.checks.values()):
            raise RuntimeError("experiment acceptance failed: " + json.dumps(experiment.checks))
        if not np.isfinite(experiment.metric) or not np.isfinite(np.asarray(experiment.rows)).all():
            raise RuntimeError("non-finite numeric artifact")
        from pai_lab.lessons.trace_labels import labels

        xlabel, ylabel = labels(lesson.id, spec.units)
        for filename in (
            "trace.csv",
            spec.artifact if spec.artifact.endswith(".csv") else "trace.csv",
        ):
            with (output_dir / filename).open("w", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow([xlabel, "reference", "observed"])
                writer.writerows(experiment.rows)
        if spec.artifact.endswith(".json"):
            write_json(output_dir / spec.artifact, experiment.payload)
        plot_trace(output_dir / "plot.png", experiment.rows, ylabel, xlabel)
        from pai_lab.lessons.observation import save_replay

        save_replay(output_dir, experiment)
        visual = {}
        if experiment.model is not None:
            visual = render(
                output_dir / "frame.png",
                experiment.model,
                experiment.data,
                resolved.get("camera_azimuth", 135.0),
            )
            if visual["std"] < 1.0:
                raise RuntimeError("empty rendering")
            if spec.artifact.endswith(".pgm"):
                from PIL import Image

                Image.open(output_dir / "frame.png").convert("L").save(output_dir / spec.artifact)
        digest = hashlib.sha256((output_dir / spec.artifact).read_bytes()).hexdigest()
        result = LessonResult(
            lesson.id,
            seed,
            samples,
            spec.operation,
            spec.metric,
            float(experiment.metric),
            float(experiment.metric),
            spec.units,
            "executed",
            lesson.verification,
            lesson.safety_level,
            digest,
            (),
        )
        (output_dir / "lesson-report.md").write_text(
            f"# {lesson.id}\n\nMetric: {result.metric_name} = {result.metric_value} {spec.units}\n\n"
            f"Inspect trace.csv, experiment.json, plot.png and frame.png when present.\n\n"
            f"Checks: {json.dumps(experiment.checks)}\n\n"
            "This execution does not mark the lesson complete. Explain the result, run a one-variable comparison, "
            "resolve feedback, then use pal lesson finish with this run directory.\n"
        )
        payload = asdict(result)
        payload["artifacts"] = sorted({p.name for p in output_dir.iterdir()} | {"summary.json"})
        write_json(output_dir / "summary.json", payload)
        hashes = {
            str(p.relative_to(output_dir)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in output_dir.rglob("*")
            if p.is_file() and p.name != "run.json"
        }
        from pai_lab.lessons.dependencies import dependency_manifest

        write_json(
            output_dir / "run.json",
            {
                "schema_version": 3,
                "dependencies": dependency_manifest(lesson.id),
                "inputs": inputs.get() or [],
                "lesson": lesson.id,
                "status": "executed",
                "created_at": datetime.now(UTC).isoformat(),
                "implementation_digest": code_digest,
                "artifacts": hashes,
                "render": visual,
                "checks": experiment.checks,
            },
        )
        return LessonResult(**{**payload, "artifacts": tuple(payload["artifacts"])})
    except BaseException as error:
        write_json(
            output_dir / "run.json",
            {
                "lesson": lesson.id,
                "status": "interrupted" if isinstance(error, KeyboardInterrupt) else "failed",
                "error": str(error),
                "implementation_digest": code_digest,
            },
        )
        raise


def check_lesson(identifier: str) -> list[str]:
    """Verify docs, entry point, implementation status, and command contract."""

    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        provider = provider_for(identifier)
        if provider is None:
            raise
        return provider.check(identifier)
    errors: list[str] = []
    paths = {
        "entrypoint": ROOT / lesson.entrypoint,
        "English lesson": ROOT / "docs" / "en" / "lessons" / f"{lesson.id}.md",
        "Korean lesson": ROOT / "docs" / "ko" / "lessons" / f"{lesson.id}.md",
        "smoke test": ROOT / "tests" / "lessons" / f"test_{lesson.id.replace('-', '_')}.py",
    }
    for label, path in paths.items():
        if not path.is_file():
            errors.append(f"missing {label}: {path.relative_to(ROOT)}")
    entrypoint = paths["entrypoint"]
    if entrypoint.is_file() and f'"{lesson.id}"' not in entrypoint.read_text(encoding="utf-8"):
        errors.append(f"{lesson.entrypoint}: canonical lesson id is not bound")
    for language in ("en", "ko"):
        path = paths["English lesson" if language == "en" else "Korean lesson"]
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        for heading in ("## Action", "## Expected", "## Recovery", "## Try it", "## Checkpoint"):
            if heading not in text:
                errors.append(f"{path.relative_to(ROOT)}: missing heading {heading}")
        if f"pal lesson run {lesson.id}" not in text:
            errors.append(f"{path.relative_to(ROOT)}: missing canonical run command")
    return errors
