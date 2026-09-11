"""The public ``pal`` command-line interface."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pai_lab import feedback
from pai_lab.assets import check_sources, fetch_bundle
from pai_lab.catalog import (
    ROOT,
    STAGES,
    Lesson,
    Stage,
    load_catalog,
    resolve_lesson,
    validate_catalog,
)
from pai_lab.hardware import preflight
from pai_lab.host import detect_host
from pai_lab.lessons import check_lesson, implementation_status, run_lesson
from pai_lab.local import local_root, write_json
from pai_lab.plugins import discover_robot_plugins
from pai_lab.progress import (
    CourseProgress,
    load_progress,
    mark_complete,
    save_progress,
    select_lesson,
)
from pai_lab.readiness import completion_gaps, gaps
from pai_lab.setup_plan import (
    SETUP_PROFILES,
    SetupProfile,
    apply_plan,
    create_plan,
    normalize_profile,
    verify_setup,
    write_plan,
)

PUBLIC_ROBOTS = ("fr3", "g1", "wuji", "enlight", "sharpa", "aloha")


def _emit(value: Any, json_output: bool) -> None:
    if json_output:
        print(json.dumps(value, indent=2, sort_keys=True))
    elif isinstance(value, dict):
        for key, item in value.items():
            if isinstance(item, (dict, list, tuple)):
                print(f"{key}={json.dumps(item, sort_keys=True)}")
            else:
                print(f"{key}={item}")
    else:
        print(value)


def host_detect(json_output: bool) -> int:
    profile = detect_host()
    _emit(profile.to_dict(), json_output)
    return 0 if "python-3.12" in profile.capabilities else 2


def doctor(json_output: bool) -> int:
    """Deprecated alias for host detection plus repository validation."""

    result = detect_host().to_dict()
    errors = validate_catalog() + check_sources()
    result.update({"deprecated": "use `pal host detect`", "repository_errors": errors})
    _emit(result, json_output)
    return 1 if errors else 0


def setup_plan_command(
    profile: SetupProfile,
    stage: Stage | None,
    robots: tuple[str, ...],
    output: Path,
    json_output: bool,
) -> int:
    plan = create_plan(profile, robots, legacy_stage=stage)
    write_plan(plan, output)
    result = plan.to_dict()
    result["path"] = str(output)
    _emit(result, json_output)
    return 0


def setup_apply_command(path: Path, json_output: bool) -> int:
    code = apply_plan(path)
    _emit({"applied": code == 0, "exit_code": code, "plan": str(path)}, json_output)
    return code


def course_init(through: Stage, robots: tuple[str, ...], electives: bool, json_output: bool) -> int:
    progress = load_progress()
    progress.through, progress.robots, progress.include_electives = through, robots, electives
    save_progress(progress)
    _emit(progress.to_dict(), json_output)
    return 0


def _lesson_row(lesson: Lesson, progress: CourseProgress) -> dict[str, object]:
    return {
        "id": lesson.id,
        "aliases": lesson.aliases,
        "stage": lesson.stage,
        "track": lesson.track,
        "status": ("needs-review" if completion_gaps(lesson.id) else "complete")
        if lesson.id in progress.completed
        else "pending",
        "prerequisites": lesson.prerequisites,
        "capabilities": lesson.capabilities,
        "elective": lesson.elective,
        "verification": lesson.verification,
        "implementation": lesson.implementation,
        "title": lesson.title,
    }


def course_list(status_only: bool, json_output: bool) -> int:
    progress = load_progress()
    rows = [
        _lesson_row(lesson, progress)
        for lesson in load_catalog()
        if select_lesson(lesson, progress)
        and (not status_only or lesson.id not in progress.completed or completion_gaps(lesson.id))
    ]
    if json_output:
        _emit(rows, True)
    else:
        for row in rows:
            print(
                f"{row['id']}\t{row['status']}\t{row['stage']}\t{row['track']}\t"
                f"{row['verification']}\t{row['title']}"
            )
    return 0


def _local_capabilities() -> set[str]:
    capabilities = set(detect_host().capabilities)
    path = ROOT / ".local" / "capabilities.json"
    if path.is_file():
        raw = json.loads(path.read_text(encoding="utf-8"))
        # Legacy/user-authored lists are intentionally informational only. Only a
        # receipt written by a pal verifier may add non-hardware capabilities.
        if raw.get("schema_version") == 2 and raw.get("source") == "pal-verify":
            protected = {
                "robot-runtime",
                "isolated-network",
                "fr3-hardware",
                "wuji-hardware",
                "enlight-hardware",
            }
            capabilities.update(
                str(item)
                for item in raw.get("verified_capabilities", [])
                if str(item) not in protected
            )
    safety_root = ROOT / ".local" / "safety"
    for robot in ("fr3", "wuji", "enlight"):
        receipt = safety_root / f"{robot}-read-only.json"
        if receipt.is_file() and json.loads(receipt.read_text(encoding="utf-8")).get("ready"):
            capabilities.add(f"read-only-preflight-{robot}")
    return capabilities


def course_runnable(without_hardware: bool, json_output: bool) -> int:
    rows: list[dict[str, object]] = []
    for lesson in load_catalog():
        hardware_free = lesson.stage != "hardware" or lesson.id == "hw-common-01"
        if without_hardware and not hardware_free:
            continue
        missing = gaps(lesson, prerequisites=False)
        rows.append(
            {
                "id": lesson.id,
                "title": lesson.title,
                "profile": (
                    "runtime-offline"
                    if lesson.id == "hw-common-01"
                    else "isaac"
                    if "isaac-sim" in lesson.capabilities
                    else "gpu"
                    if "nvidia-cuda" in lesson.capabilities
                    else "ros"
                    if "ros2-jazzy" in lesson.capabilities
                    else "core"
                ),
                "hardware_free": hardware_free,
                "implementation": lesson.implementation,
                "available_now": lesson.implementation == "implemented" and not missing,
                "missing_capabilities": missing,
            }
        )
    if json_output:
        _emit(rows, True)
    else:
        for row in rows:
            state = "available" if row["available_now"] else "prepare"
            print(f"{row['id']}\t{state}\t{row['profile']}\t{row['title']}")
    return 0


def next_lesson(json_output: bool) -> int:
    progress = load_progress()
    blocked: list[dict[str, object]] = []
    for lesson in load_catalog():
        if not select_lesson(lesson, progress) or (
            lesson.id in progress.completed and not completion_gaps(lesson.id)
        ):
            continue
        incomplete = [item for item in lesson.prerequisites if item not in progress.completed]
        missing = gaps(lesson)
        if incomplete or missing:
            blocked.append(
                {
                    "id": lesson.id,
                    "incomplete_prerequisites": incomplete,
                    "missing_capabilities": missing,
                }
            )
            continue
        result = _lesson_row(lesson, progress)
        result["eligible"] = True
        _emit(result, json_output)
        return 0
    _emit({"eligible": False, "reason": "no-eligible-lesson", "blocked": blocked}, json_output)
    return 2


def lesson_run_command(
    identifier: str,
    output_dir: Path | None,
    seed: int,
    samples: int,
    headless: bool,
    json_output: bool,
    variant: float = 1.0,
) -> int:
    lesson = resolve_lesson(identifier)
    if implementation_status(lesson.id) != "implemented":
        _emit(
            {
                "status": "reader_test_required",
                "lesson": lesson.id,
                "reason": "lesson is scaffolded until real hardware evidence exists",
            },
            json_output,
        )
        return 2
    progress = load_progress()
    missing_prerequisites = [
        item for item in lesson.prerequisites if item not in progress.completed
    ]
    if missing_prerequisites:
        _emit(
            {
                "status": "blocked",
                "lesson": lesson.id,
                "missing_prerequisites": missing_prerequisites,
            },
            json_output,
        )
        return 2
    missing_capabilities = gaps(lesson)
    if missing_capabilities:
        _emit(
            {
                "status": "capability-unavailable",
                "lesson": lesson.id,
                "missing_capabilities": missing_capabilities,
            },
            json_output,
        )
        return 2
    if identifier.lower() != lesson.id:
        print(f"warning: {identifier} is deprecated; use {lesson.id}", file=sys.stderr)
    run_dir = output_dir or (
        local_root() / "runs" / lesson.id / datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
    )
    write_json(
        local_root() / "session.json",
        {"lesson": lesson.id, "run_dir": str(run_dir.resolve()), "phase": "running"},
    )
    try:
        result = run_lesson(
            lesson.id,
            output_dir=run_dir,
            seed=seed,
            samples=samples,
            headless=headless,
            variant=variant,
        )
    except (PermissionError, RuntimeError, ValueError, FileNotFoundError, ImportError) as error:
        write_json(
            local_root() / "session.json",
            {"lesson": lesson.id, "run_dir": str(run_dir.resolve()), "phase": "failed"},
        )
        _emit(
            {
                "status": "capability-unavailable"
                if isinstance(error, (FileNotFoundError, ImportError))
                else "failed",
                "lesson": lesson.id,
                "error": str(error),
            },
            json_output,
        )
        return 2 if isinstance(error, (FileNotFoundError, ImportError)) else 1
    write_json(
        local_root() / "session.json",
        {"lesson": lesson.id, "run_dir": str(run_dir), "phase": "inspect"},
    )
    payload = {
        "status": result.status,
        "lesson": lesson.id,
        "run_dir": str(run_dir),
        "result": result.__dict__,
    }
    _emit(payload, json_output)
    return 0


def lesson_check_command(identifier: str, json_output: bool, run_dir: Path | None = None) -> int:
    lesson = resolve_lesson(identifier)
    errors = check_lesson(lesson.id)
    if run_dir is not None:
        from pai_lab.lessons.evidence import validate_run

        errors += validate_run(lesson.id, run_dir)
    errors += gaps(lesson)
    result = {"lesson": lesson.id, "valid": not errors, "errors": errors}
    _emit(result, json_output)
    return 1 if errors else 0


def lesson_finish_command(identifier: str, run_dir: Path, json_output: bool) -> int:
    from pai_lab.lessons.evidence import validate_review, validate_run

    lesson = resolve_lesson(identifier)
    errors = check_lesson(lesson.id) + gaps(lesson) + validate_run(lesson.id, run_dir)
    if feedback.pending(lesson.id):
        errors.append("unresolved feedback; inspect pal feedback list")
    errors += validate_review(lesson.id, run_dir)
    if errors:
        _emit({"status": "blocked", "lesson": lesson.id, "errors": errors}, json_output)
        return 2
    progress = load_progress()
    mark_complete(progress, lesson, run_dir.resolve())
    save_progress(progress)
    write_json(
        local_root() / "session.json",
        {"lesson": lesson.id, "run_dir": str(run_dir.resolve()), "phase": "finished"},
    )
    _emit({"status": "complete", "lesson": lesson.id, "run_dir": str(run_dir)}, json_output)
    return 0


def lesson_review_command(
    identifier: str, run_dir: Path, comparison: Path, notes: str, json_output: bool
) -> int:
    from pai_lab.lessons.evidence import comparison_errors

    lesson = resolve_lesson(identifier)
    errors = comparison_errors(lesson.id, run_dir, comparison)
    if not notes.strip():
        errors.append("explain the observed result and comparison")
    if errors:
        _emit({"status": "blocked", "errors": errors}, json_output)
        return 2
    write_json(
        run_dir / "review.json",
        {
            "lesson": lesson.id,
            "comparison_run": str(comparison.resolve()),
            "notes": notes,
            "reviewed_at": datetime.now(UTC).isoformat(),
        },
    )
    _emit({"status": "reviewed", "lesson": lesson.id}, json_output)
    return 0


def list_robots(json_output: bool) -> int:
    names = sorted(set(PUBLIC_ROBOTS).union(discover_robot_plugins()))
    _emit(names, json_output)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pal")
    commands = parser.add_subparsers(dest="command", required=True)

    host = commands.add_parser("host")
    host_commands = host.add_subparsers(dest="host_command", required=True)
    host_detect_parser = host_commands.add_parser("detect")
    host_detect_parser.add_argument("--json", action="store_true")

    setup = commands.add_parser("setup")
    setup_commands = setup.add_subparsers(dest="setup_command", required=True)
    plan = setup_commands.add_parser("plan")
    plan_selection = plan.add_mutually_exclusive_group(required=True)
    plan_selection.add_argument("--profile", choices=SETUP_PROFILES)
    plan_selection.add_argument("--stage", choices=STAGES)
    plan.add_argument("--robot", action="append", default=[])
    plan.add_argument("--out", type=Path, default=ROOT / ".local" / "setup-plan.json")
    plan.add_argument("--json", action="store_true")
    apply = setup_commands.add_parser("apply")
    apply.add_argument("plan", type=Path)
    apply.add_argument("--json", action="store_true")
    verify = setup_commands.add_parser("verify")
    verify_selection = verify.add_mutually_exclusive_group(required=True)
    verify_selection.add_argument("--profile", choices=SETUP_PROFILES)
    verify_selection.add_argument("--stage", choices=STAGES)
    verify.add_argument("--robot", action="append", default=[])
    verify.add_argument("--json", action="store_true")

    course = commands.add_parser("course")
    course_commands = course.add_subparsers(dest="course_command", required=True)
    init = course_commands.add_parser("init")
    init.add_argument("--through", choices=STAGES, default="core")
    init.add_argument("--robot", action="append", default=[])
    init.add_argument("--include-electives", action="store_true")
    init.add_argument("--json", action="store_true")
    for name in ("list", "status", "next"):
        item = course_commands.add_parser(name)
        item.add_argument("--json", action="store_true")
    runnable = course_commands.add_parser("runnable")
    runnable.add_argument("--without-hardware", action="store_true", required=True)
    runnable.add_argument("--json", action="store_true")

    lesson = commands.add_parser("lesson")
    lesson_commands = lesson.add_subparsers(dest="lesson_command", required=True)
    run = lesson_commands.add_parser("run")
    run.add_argument("lesson_id")
    run.add_argument("--output-dir", type=Path)
    run.add_argument("--seed", type=int, default=7)
    run.add_argument("--samples", type=int, default=64)
    run.add_argument("--variant", type=float, default=1.0)
    run.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    run.add_argument("--json", action="store_true")
    check = lesson_commands.add_parser("check")
    check.add_argument("lesson_id")
    check.add_argument("--run-dir", type=Path)
    check.add_argument("--json", action="store_true")
    finish = lesson_commands.add_parser("finish")
    finish.add_argument("lesson_id")
    finish.add_argument("--run-dir", type=Path, required=True)
    finish.add_argument("--json", action="store_true")
    review = lesson_commands.add_parser("review")
    review.add_argument("lesson_id")
    review.add_argument("--run-dir", type=Path, required=True)
    review.add_argument("--comparison-run-dir", type=Path, required=True)
    review.add_argument("--notes", required=True)
    review.add_argument("--json", action="store_true")

    feedback_parser = commands.add_parser("feedback")
    feedback_commands = feedback_parser.add_subparsers(dest="feedback_command", required=True)
    feedback_add = feedback_commands.add_parser("add")
    feedback_add.add_argument("text")
    feedback_add.add_argument("--lesson")
    feedback_add.add_argument("--urgent", action="store_true")
    feedback_add.add_argument("--json", action="store_true")
    feedback_list = feedback_commands.add_parser("list")
    feedback_list.add_argument("--json", action="store_true")
    feedback_resolve = feedback_commands.add_parser("resolve")
    feedback_resolve.add_argument("id")
    feedback_resolve.add_argument("--evidence", required=True)
    feedback_resolve.add_argument("--json", action="store_true")

    assets = commands.add_parser("assets")
    assets_commands = assets.add_subparsers(dest="assets_command", required=True)
    fetch = assets_commands.add_parser("fetch")
    fetch.add_argument("bundle")
    fetch.add_argument("--json", action="store_true")

    hardware = commands.add_parser("hardware")
    hardware_commands = hardware.add_subparsers(dest="hardware_command", required=True)
    hardware_preflight = hardware_commands.add_parser("preflight")
    hardware_preflight.add_argument("robot", choices=("fr3", "wuji", "enlight"))
    hardware_preflight.add_argument("--read-only", action="store_true", required=True)
    hardware_preflight.add_argument("--snapshot", type=Path)
    hardware_preflight.add_argument("--json", action="store_true")

    sources = commands.add_parser("sources")
    sources_commands = sources.add_subparsers(dest="sources_command", required=True)
    source_check = sources_commands.add_parser("check")
    source_check.add_argument("--json", action="store_true")

    doctor_parser = commands.add_parser("doctor", help="deprecated: use host detect")
    doctor_parser.add_argument("--format", choices=("text", "json"), default="text")
    tutorial = commands.add_parser("tutorial", help="deprecated: use course")
    tutorial_commands = tutorial.add_subparsers(dest="tutorial_command", required=True)
    for name in ("list", "status", "next"):
        tutorial_commands.add_parser(name)
    robot = commands.add_parser("robot")
    robot_commands = robot.add_subparsers(dest="robot_command", required=True)
    robot_list = robot_commands.add_parser("list")
    robot_list.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "host":
        return host_detect(args.json)
    if args.command == "setup":
        if args.setup_command == "plan":
            profile = normalize_profile(args.profile, args.stage)
            return setup_plan_command(profile, args.stage, tuple(args.robot), args.out, args.json)
        if args.setup_command == "apply":
            return setup_apply_command(args.plan, args.json)
        profile = normalize_profile(args.profile, args.stage)
        result = verify_setup(profile, tuple(args.robot))
        _emit(result, args.json)
        return 0 if result["ready"] else 2
    if args.command == "course":
        if args.course_command == "init":
            return course_init(args.through, tuple(args.robot), args.include_electives, args.json)
        if args.course_command == "next":
            return next_lesson(args.json)
        if args.course_command == "runnable":
            return course_runnable(args.without_hardware, args.json)
        return course_list(args.course_command == "status", args.json)
    if args.command == "lesson":
        if args.lesson_command == "check":
            return lesson_check_command(args.lesson_id, args.json, args.run_dir)
        if args.lesson_command == "finish":
            return lesson_finish_command(args.lesson_id, args.run_dir, args.json)
        if args.lesson_command == "review":
            return lesson_review_command(
                args.lesson_id, args.run_dir, args.comparison_run_dir, args.notes, args.json
            )
        return lesson_run_command(
            args.lesson_id,
            args.output_dir,
            args.seed,
            args.samples,
            args.headless,
            args.json,
            args.variant,
        )
    if args.command == "feedback":
        try:
            value = (
                feedback.add(args.text, args.lesson, args.urgent)
                if args.feedback_command == "add"
                else feedback.resolve(args.id, args.evidence)
                if args.feedback_command == "resolve"
                else feedback.items()
            )
        except ValueError as error:
            _emit({"error": str(error)}, args.json)
            return 2
        _emit(value, args.json)
        return 0
    if args.command == "assets":
        receipt = fetch_bundle(args.bundle)
        _emit(receipt, args.json)
        return 0
    if args.command == "hardware":
        snapshot = args.snapshot or ROOT / ".local" / "hardware" / f"{args.robot}.json"
        if not snapshot.is_file():
            _emit(
                {"ready": False, "status": "capability-unavailable", "snapshot": str(snapshot)},
                args.json,
            )
            return 2
        result = preflight(args.robot, snapshot, read_only=args.read_only)
        if result["ready"]:
            result["recorded_at"] = datetime.now(UTC).isoformat()
            safety_receipt = ROOT / ".local" / "safety" / f"{args.robot}-read-only.json"
            safety_receipt.parent.mkdir(parents=True, exist_ok=True)
            safety_receipt.write_text(
                json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
            )
        _emit(result, args.json)
        return 0 if result["ready"] else 3
    if args.command == "sources":
        errors = check_sources()
        _emit({"valid": not errors, "errors": errors}, args.json)
        return 1 if errors else 0
    if args.command == "doctor":
        return doctor(args.format == "json")
    if args.command == "tutorial":
        print("warning: `pal tutorial` is deprecated; use `pal course`", file=sys.stderr)
        return (
            next_lesson(False)
            if args.tutorial_command == "next"
            else course_list(args.tutorial_command == "status", False)
        )
    if args.command == "robot":
        return list_robots(args.json)
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
