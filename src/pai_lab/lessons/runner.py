"""Small deterministic baselines shared by all lesson entry points."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path

from pai_lab.bundle import validate_bundle
from pai_lab.catalog import ROOT, Lesson, resolve_lesson


@dataclass(frozen=True)
class LessonResult:
    lesson_id: str
    seed: int
    samples: int
    metric_name: str
    metric_value: float
    changed_metric_value: float
    units: str
    status: str
    verification: str
    safety_level: str
    artifact_digest: str


def _trace(lesson: Lesson, seed: int, samples: int) -> list[tuple[float, float, float]]:
    """Return deterministic reference/response values without optional imports."""

    phase = (sum(ord(char) for char in lesson.id) + seed) % 31 / 31.0
    response: list[tuple[float, float, float]] = []
    for index in range(samples):
        time_s = index * 0.02
        reference = math.sin(2.0 * math.pi * (0.2 + phase * 0.1) * time_s)
        observed = reference * (0.96 if lesson.stage == "core" else 0.93)
        observed += 0.01 * math.cos(index * 0.17 + phase)
        response.append((time_s, reference, observed))
    return response


def run_lesson(
    identifier: str,
    *,
    output_dir: Path,
    seed: int = 7,
    samples: int = 64,
    headless: bool = True,
) -> LessonResult:
    """Execute a deterministic teaching baseline and persist inspectable output."""

    lesson = resolve_lesson(identifier)
    if samples < 8:
        raise ValueError("samples must be at least 8")
    if lesson.stage == "hardware" and not headless:
        raise PermissionError("hardware lessons only run offline/read-only through this command")
    if lesson.id == "sim-deploy-01":
        manifest = ROOT / "examples/sim-deploy-01/sample_candidate/manifest.json"
        bundle_errors = validate_bundle(manifest)
        if bundle_errors:
            raise RuntimeError("invalid sample candidate: " + "; ".join(bundle_errors))
    output_dir.mkdir(parents=True, exist_ok=True)
    trace = _trace(lesson, seed, samples)
    mean_error = sum(abs(reference - observed) for _, reference, observed in trace) / samples
    changed_trace = _trace(lesson, seed + 1, samples)
    changed_error = sum(
        abs(reference - observed) for _, reference, observed in changed_trace
    ) / samples
    trace_path = output_dir / "trace.csv"
    with trace_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(("time_s", "reference", "observed"))
        writer.writerows((f"{t:.4f}", f"{r:.8f}", f"{o:.8f}") for t, r, o in trace)
    digest = hashlib.sha256(trace_path.read_bytes()).hexdigest()
    result = LessonResult(
        lesson_id=lesson.id,
        seed=seed,
        samples=samples,
        metric_name="mean_absolute_tracking_error",
        metric_value=round(mean_error, 10),
        changed_metric_value=round(changed_error, 10),
        units="normalized",
        status="offline-read-only" if lesson.stage == "hardware" else "passed",
        verification=lesson.verification,
        safety_level=lesson.safety_level,
        artifact_digest=digest,
    )
    (output_dir / "summary.json").write_text(
        json.dumps(asdict(result), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    report = (
        f"# {lesson.id} run report\n\n"
        f"- Generated: {datetime.now(UTC).isoformat()}\n"
        f"- Action: deterministic headless baseline (`--seed {seed}`)\n"
        f"- Expected: finite trace with {samples} samples\n"
        f"- Observed: {result.metric_name} = {result.metric_value} {result.units}\n"
        f"- Try it: seed {seed + 1} produced {result.changed_metric_value} {result.units}\n"
        f"- Recovery: run `pal lesson check {lesson.id}` before retrying\n"
        f"- Verification: `{lesson.verification}`\n"
        f"- Safety: `{lesson.safety_level}`; no hardware command was emitted\n"
    )
    (output_dir / "lesson-report.md").write_text(report, encoding="utf-8")
    return result


def check_lesson(identifier: str) -> list[str]:
    """Statically verify a lesson's docs, entry point, and command contract."""

    lesson = resolve_lesson(identifier)
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
