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
    lesson = resolve_lesson(identifier)
    errors = []
    try:
        receipt = json.loads((run_dir / "run.json").read_text())
        summary = json.loads((run_dir / "summary.json").read_text())
        experiment = json.loads((run_dir / "experiment.json").read_text())
        if receipt.get("schema_version") != 2 or receipt.get("status") != "executed":
            errors.append("run was not successfully executed")
        if receipt.get("lesson") != lesson.id or summary.get("lesson_id") != lesson.id:
            errors.append("run lesson identity mismatch")
        if receipt.get("implementation_digest") != implementation_digest():
            errors.append("implementation changed since execution; rerun experiment")
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


def comparison_errors(identifier: str, baseline: Path, comparison: Path) -> list[str]:
    errors = validate_run(identifier, baseline) + validate_run(identifier, comparison)
    if baseline.resolve() == comparison.resolve():
        errors.append("comparison must be a separate execution")
    if errors:
        return errors
    a = json.loads((baseline / "summary.json").read_text())
    b = json.loads((comparison / "summary.json").read_text())
    av = json.loads((baseline / "experiment.json").read_text())["variant"]
    bv = json.loads((comparison / "experiment.json").read_text())["variant"]
    if sum(a[key] != b[key] for key in ("seed", "samples")) + (av != bv) != 1:
        errors.append("change exactly one of seed, samples, or variant")
    return errors


def validate_review(identifier: str, run_dir: Path) -> list[str]:
    try:
        review = json.loads((run_dir / "review.json").read_text())
        if review.get("lesson") != identifier or not str(review.get("notes", "")).strip():
            return ["invalid lesson review"]
        return comparison_errors(identifier, run_dir, Path(review["comparison_run"]))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as error:
        return [f"unreadable or missing review; use pal lesson review: {error}"]
