"""Validate run identity, code version, artifact integrity, and numerical contents."""

import csv
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons.runner import implementation_digest


def validate_run(identifier: str, run_dir: Path) -> list[str]:
    try:
        lesson = resolve_lesson(identifier)
    except ValueError:
        from pai_lab.providers import provider_for

        provider = provider_for(identifier)
        if provider is None:
            return ["unknown lesson provider"]
        return provider.validate_run(identifier, run_dir)
    errors = []
    try:
        receipt = json.loads((run_dir / "run.json").read_text())
        summary = json.loads((run_dir / "summary.json").read_text())
        experiment = json.loads((run_dir / "experiment.json").read_text())
        if receipt.get("schema_version") not in {2, 3} or receipt.get("status") != "executed":
            errors.append("run was not successfully executed")
        if receipt.get("lesson") != lesson.id or summary.get("lesson_id") != lesson.id:
            errors.append("run lesson identity mismatch")
        if receipt.get("implementation_digest") != implementation_digest(
            lesson.id if receipt.get("schema_version") == 3 else None
        ):
            errors.append("implementation changed since execution; rerun experiment")
        for input_run in receipt.get("inputs", []):
            source = Path(input_run["run_dir"])
            if source.resolve() == run_dir.resolve():
                errors.append("input receipt cannot refer to itself")
            elif hashlib.sha256((source / "run.json").read_bytes()).hexdigest() != input_run["receipt_sha256"]:
                errors.append("input run receipt changed")
            else:
                errors += ["input evidence: " + error for error in validate_run(input_run["lesson"], source)]
        required = (set(lesson.expected_artifacts) | {"plot.png", "experiment.json"}) - {"run.json"}
        hashes = receipt.get("artifacts", {})
        for relative in required:
            if relative not in hashes:
                errors.append(f"required artifact missing from receipt: {relative}")
        for relative, expected in hashes.items():
            path = (run_dir / relative).resolve()
            if not path.is_relative_to(run_dir.resolve()):
                errors.append("artifact path escapes run directory")
                continue
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                errors.append(f"artifact checksum mismatch: {relative}")
        if not experiment.get("checks") or not all(
            value is True for value in experiment["checks"].values()
        ):
            errors.append("experiment acceptance criteria failed")
        with (run_dir / "trace.csv").open() as stream:
            values = np.array([[float(v) for v in row] for row in list(csv.reader(stream))[1:]])
        if (
            values.ndim != 2
            or values.shape[1] != 3
            or len(values) < 1
            or not np.isfinite(values).all()
        ):
            errors.append("invalid numeric trace")
        if (
            not np.isfinite(summary["metric_value"])
            or summary["metric_value"] != experiment["metric"]
        ):
            errors.append("summary metric disagrees with measured experiment")
        images = {name for name in required | set(hashes) if name.endswith(".png")}
        for name in images:
            pixels = np.asarray(Image.open(run_dir / name))
            if min(pixels.shape[:2]) < 100 or float(pixels.std()) < 1.0:
                errors.append(f"empty visualization: {name}")
        from pai_lab.lessons.acceptance import measurement_errors

        errors += measurement_errors(lesson.id, run_dir, values, experiment)
    except (OSError, ValueError, KeyError, TypeError, IndexError, AttributeError) as error:
        errors.append(f"unreadable run evidence: {error}")
    return errors


def comparison_errors(identifier: str, baseline: Path, comparison: Path | None) -> list[str]:
    if comparison is None:
        if identifier not in {
            "core-00",
            "core-02",
            "core-03",
            "core-fr3-01",
            "core-enlight-01",
            "core-dexterity-01",
        }:
            from pai_lab.providers import provider_for

            provider = provider_for(identifier)
            if provider is None or provider.requires_comparison(identifier):
                return ["this lesson requires a separate comparison run"]
        return validate_run(identifier, baseline)
    errors = validate_run(identifier, baseline) + validate_run(identifier, comparison)
    if baseline.resolve() == comparison.resolve():
        errors.append("comparison must be a separate execution")
    if errors:
        return errors
    a = json.loads((baseline / "summary.json").read_text())
    b = json.loads((comparison / "summary.json").read_text())
    ae = json.loads((baseline / "experiment.json").read_text())
    be = json.loads((comparison / "experiment.json").read_text())
    # A legacy variant is one declared intervention, including documented dependent changes.
    if ae["variant"] != be["variant"]:
        changed = 1
    else:
        ap, bp = ae.get("parameters", {}), be.get("parameters", {})
        changed = sum(ap.get(key) != bp.get(key) for key in ap.keys() | bp.keys())
    if sum(a[key] != b[key] for key in ("seed", "samples")) + changed != 1:
        errors.append("change exactly one of seed, samples, variant, or a named parameter")
    return errors


def validate_review(identifier: str, run_dir: Path) -> list[str]:
    try:
        review = json.loads((run_dir / "review.json").read_text())
        if review.get("lesson") != identifier or not str(review.get("notes", "")).strip():
            return ["invalid lesson review"]
        return comparison_errors(
            identifier,
            run_dir,
            Path(review["comparison_run"]) if review.get("comparison_run") else None,
        )
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return [f"unreadable or missing review; use pal lesson review: {error}"]
