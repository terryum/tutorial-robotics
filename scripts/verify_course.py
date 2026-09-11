"""Developer-only sequential verification. All evidence stays in the selected local session."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from pai_lab.catalog import ROOT, load_catalog
from pai_lab.cli import main as pal
from pai_lab.lessons.evidence import validate_run
from pai_lab.local import write_json
from pai_lab.progress import load_progress


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("core", "ros", "gpu", "isaac", "all"), default="core")
    parser.add_argument("--local-dir", type=Path, default=ROOT / ".local/development/course")
    parser.add_argument("--samples", type=int, default=64)
    args = parser.parse_args()
    local = args.local_dir.resolve()
    if local == (ROOT / ".local").resolve():
        raise ValueError("developer verification must use a separate local state directory")
    os.environ["PAL_LOCAL_DIR"] = str(local)
    pal(["course", "init", "--through", "hardware", "--json"])
    results = []
    teaching = json.loads((ROOT / "curriculum/teaching.json").read_text())
    for lesson in load_catalog():
        if lesson.implementation != "implemented":
            continue
        portable = lesson.stage == "core" or lesson.id in {"sim-deploy-01", "hw-common-01"}
        selected = (
            portable
            if args.profile == "core"
            else portable
            or (args.profile == "ros" and "ros2-jazzy" in lesson.capabilities)
            or (args.profile == "gpu" and "nvidia-cuda" in lesson.capabilities)
            or (args.profile == "isaac" and "isaac-sim" in lesson.capabilities)
            or args.profile == "all"
        )
        if not selected:
            continue
        completed = load_progress().completed.get(lesson.id)
        if completed:
            existing = Path(completed["run_dir"])
            existing = existing if existing.is_absolute() else ROOT / existing
            if not validate_run(lesson.id, existing):
                results.append({"id": lesson.id, "status": "verified-existing"})
                continue
        import uuid

        run_root = local / "runs" / lesson.id / uuid.uuid4().hex
        baseline, comparison = run_root / "baseline", run_root / "comparison"
        comparison_parameters = {"seed": "7", "samples": str(args.samples), "variant": "1"}
        description = teaching[lesson.id]
        comparison_parameters[description["variable"]] = description["value"]
        commands = [
            [
                "lesson",
                "run",
                lesson.id,
                "--output-dir",
                str(baseline),
                "--samples",
                str(args.samples),
                "--seed",
                "7",
                "--json",
            ],
            [
                "lesson",
                "run",
                lesson.id,
                "--output-dir",
                str(comparison),
                "--samples",
                comparison_parameters["samples"],
                "--seed",
                comparison_parameters["seed"],
                "--variant",
                comparison_parameters["variant"],
                "--json",
            ],
            ["lesson", "check", lesson.id, "--run-dir", str(baseline), "--json"],
            [
                "lesson",
                "review",
                lesson.id,
                "--run-dir",
                str(baseline),
                "--comparison-run-dir",
                str(comparison),
                "--notes",
                f"Developer comparison: {description['variable']} changed to {description['value']}. "
                + description["observe"]
                + " Inspected measured artifacts; this is not learner completion.",
                "--json",
            ],
            ["lesson", "finish", lesson.id, "--run-dir", str(baseline), "--json"],
        ]
        code = 0
        for command in commands:
            code = pal(command)
            if code:
                break
        results.append(
            {
                "id": lesson.id,
                "status": "verified" if code == 0 else "blocked",
                "run_dir": str(baseline),
            }
        )
        write_json(local / "verification.json", results)
        if code:
            print(
                json.dumps(
                    {
                        "blocked": lesson.id,
                        "resume": "rerun the same command after resolving the reported gap",
                    }
                ),
                flush=True,
            )
            return code
    write_json(local / "verification.json", results)
    print(json.dumps({"verified": len(results), "profile": args.profile, "local_dir": str(local)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
