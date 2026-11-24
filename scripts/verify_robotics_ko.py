"""Re-run selected software lessons without modifying learner history."""

from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import uuid
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from unittest.mock import patch

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons import learning, runner
from pai_lab.lessons.evidence import validate_run
from pai_lab.lessons.inputs import record
from pai_lab.local import write_json
from pai_lab.readiness import gaps

# Each lesson is independent of learner-owned datasets and physical inputs.
SOFTWARE_LESSONS = frozenset(
    [
        "core-01",
        "core-04",
        "core-enlight-02",
        "core-enlight-03",
        "core-enlight-04",
        "core-enlight-05",
        "core-fr3-04",
        "core-fr3-05",
        "core-fr3-09",
        "core-fr3-10",
        "core-data-01",
        "core-il-01",
        "core-rl-01",
        "core-teleop-01",
        "sim-ros-01",
        "sim-enlight-03",
        "sim-enlight-04",
        "sim-enlight-05",
    ]
)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def runtime_versions() -> dict:
    versions = {"python": platform.python_version()}
    for package in ("mujoco", "numpy", "scipy", "matplotlib", "isaacsim", "isaacsim-core", "torch"):
        try:
            versions[package] = version(package)
        except PackageNotFoundError:
            continue
    if shutil.which("nvidia-smi"):
        try:
            gpu = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5,
                check=True,
            )
            versions["nvidia_gpu_driver"] = gpu.stdout.strip()
        except (OSError, subprocess.SubprocessError):
            versions["nvidia_gpu_driver"] = "unverified"
    return versions


def lesson_metrics(identifier: str, path: Path) -> dict:
    summary = read_json(path / "summary.json")
    experiment = read_json(path / "experiment.json")["payload"]
    result = {
        "metric": summary["metric_name"],
        "value": summary["metric_value"],
        "unit": summary["units"],
    }
    for key in (
        "tcp_rmse_m",
        "joint_rmse_rad",
        "parameter_l1_change",
        "reload_error",
        "parameter_delta",
        "reload_max_error",
        "performance_verified",
        "epoch",
        "model",
        "engine",
        "heldout_mse",
        "episodes",
        "transitions",
    ):
        if key in experiment:
            result[key] = experiment[key]
    evaluation_path = path / "evaluation.json"
    if evaluation_path.exists():
        evaluation = read_json(evaluation_path)
        result["evaluation"] = {
            "successes": evaluation["successes"],
            "attempts": len(evaluation["episodes"]),
            "required_successes": evaluation["required_successes"],
            "passed": evaluation["performance_verified"],
        }
    if "parameter_l1_change" in result and (
        result["parameter_l1_change"] <= 0 or result["reload_error"] > 1e-12
    ):
        raise ValueError("optimizer update or checkpoint reload check failed")
    return result


def verify_lessons(args: argparse.Namespace) -> int:
    root = args.output_dir.resolve()
    root.mkdir(parents=True, exist_ok=True)
    receipt = root / "lessons.json"
    host = {
        "system": platform.system(),
        "machine": platform.machine(),
        "version": platform.mac_ver()[0] or platform.release(),
    }
    runtime = runtime_versions()
    state = (
        read_json(receipt)
        if receipt.exists()
        else {"schema_version": 1, "host": host, "runtime": runtime, "lessons": {}}
    )
    if state["host"] != host or state.get("runtime") != runtime:
        raise ValueError("choose a new output directory for this host/runtime version")
    for requested in args.lesson:
        identifier = resolve_lesson(requested).id
        if identifier not in SOFTWARE_LESSONS:
            raise ValueError(f"{identifier} is outside the offline textbook software batch")

    def verified_input(identifier: str) -> Path:
        entry = state["lessons"].get(identifier, {})
        if entry.get("status") != "passed":
            raise FileNotFoundError(f"run {identifier} first in this output directory")
        path = (root / entry["run_dir"]).resolve()
        if not path.is_relative_to(root) or validate_run(identifier, path):
            raise ValueError(f"current validated artifact required from {identifier}")
        return path

    def previous_run(identifier: str) -> Path:
        path = verified_input(identifier)
        record(identifier, path)
        return path

    with (
        patch.dict(os.environ, {"PAL_LOCAL_DIR": str(root / "development-state")}),
        patch.object(learning, "previous_run", previous_run),
    ):
        for requested in args.lesson:
            lesson = resolve_lesson(requested)
            identifier = lesson.id
            previous = state["lessons"].get(identifier, {})
            params = {"seed": args.seed, "samples": args.samples, "variant": args.variant}
            if identifier == "core-il-01":
                data_source = state["lessons"].get("core-data-01", {}).get("run_dir")
            else:
                data_source = None
            settings = {**params, "data_source": data_source} if data_source else params
            if (
                not args.retry
                and previous.get("status") == "passed"
                and previous.get("inputs") == settings
            ):
                path = root / previous["run_dir"]
                if path.resolve().is_relative_to(root) and not validate_run(identifier, path):
                    print(f"{identifier}: reused verified evidence")
                    continue
            path = root / identifier / uuid.uuid4().hex
            row = {"inputs": settings, "run_dir": path.relative_to(root).as_posix()}
            try:
                missing = gaps(lesson, prerequisites=False)
                if identifier == "core-il-01" and not missing:
                    try:
                        verified_input("core-data-01")
                    except (FileNotFoundError, ValueError) as error:
                        missing.append(str(error))
                if missing:
                    row.update(status="blocked", reason="; ".join(missing))
                else:
                    # This isolated process keeps normal platform, capability, asset,
                    # numerical, render and artifact checks. It skips learner completion.
                    with patch.object(
                        runner, "gaps", lambda lesson: gaps(lesson, prerequisites=False)
                    ):
                        runner.run_lesson(identifier, output_dir=path, **params)
                    errors = validate_run(identifier, path)
                    if errors:
                        raise RuntimeError("; ".join(errors))
                    row.update(status="passed", metrics=lesson_metrics(identifier, path))
            except Exception as error:  # noqa: BLE001 - record a per-lesson failure and continue
                row.update(status="failed", reason=f"{type(error).__name__}: {error}")
            state["lessons"][identifier] = row
            write_json(receipt, state)
            print(f"{identifier}: {row['status']} {row.get('reason', '')}", flush=True)
    return int(
        any(state["lessons"][resolve_lesson(item).id]["status"] != "passed" for item in args.lesson)
    )


def summarize(args: argparse.Namespace) -> int:
    """Export numbers only, leaving receipts, filenames and raw artifacts in the run."""
    root = args.mac_run.resolve()
    state = read_json(root / "lessons.json")
    if state["host"]["system"] != "Darwin":
        raise ValueError("Mac evidence requires a macOS run; record WS2 evidence separately")
    lessons = {}
    for identifier, entry in state["lessons"].items():
        if entry["status"] != "passed":
            lessons[identifier] = {"status": entry["status"]}
            continue
        path = (root / entry["run_dir"]).resolve()
        if not path.is_relative_to(root) or validate_run(identifier, path):
            raise ValueError(f"current verified evidence required for {identifier}")
        receipt = read_json(path / "run.json")
        lessons[identifier] = {
            "status": "passed",
            "inputs": {
                key: value for key, value in entry["inputs"].items() if key != "data_source"
            },
            "metrics": lesson_metrics(identifier, path),
            "implementation_sha256": receipt["implementation_digest"],
            "artifact_sha256": read_json(path / "summary.json")["artifact_digest"],
        }
    write_json(
        args.output,
        {
            "schema_version": 1,
            "host": state["host"],
            "software": state["runtime"],
            "lessons": lessons,
        },
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    lessons = commands.add_parser("lessons")
    lessons.add_argument("lesson", nargs="+")
    lessons.add_argument("--output-dir", type=Path, required=True)
    lessons.add_argument("--seed", type=int, default=7)
    lessons.add_argument("--samples", type=int, default=64)
    lessons.add_argument("--variant", type=float, default=1.0)
    lessons.add_argument("--retry", action="store_true")
    summary = commands.add_parser("summarize")
    summary.add_argument("--mac-run", type=Path, required=True)
    summary.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        return verify_lessons(args) if args.command == "lessons" else summarize(args)
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    raise SystemExit(main())
