"""The public `pal` command-line interface."""

from __future__ import annotations

import argparse
import json
import platform
import sys
from typing import Any

from pai_lab.plugins import discover_robot_plugins
from pai_lab.tutorials import ROOT, Tutorial, discover, progress, validate_graph

PUBLIC_ROBOTS = ("fr3", "unitree-g1", "wuji-hand2", "sharpa-wave", "aloha")


def _doctor_checks() -> dict[str, Any]:
    errors = validate_graph()
    return {
        "host": {"system": platform.system(), "machine": platform.machine()},
        "checks": {
            "repository": ROOT.is_dir(),
            "tutorials": bool(discover()),
            "python-3.12": sys.version_info[:2] == (3, 12),
            "private-required": False,
        },
        "graph_errors": errors,
    }


def doctor(output_format: str = "text") -> int:
    result = _doctor_checks()
    checks = result["checks"]
    errors = result["graph_errors"]
    if output_format == "json":
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        host = result["host"]
        print(f"host={host['system']} {host['machine']}")
        for name, value in checks.items():
            print(f"{name}={value}")
        for error in errors:
            print(f"graph-error={error}")
    return 1 if errors or not all(value for key, value in checks.items() if key != "private-required") else 0


def _print_tutorial(tutorial: Tutorial, status: str) -> None:
    prerequisites = ",".join(tutorial.prerequisites) or "-"
    requirements = ",".join(tutorial.requirements) or "-"
    print(
        f"{tutorial.tutorial_id}\t{status}\t{tutorial.mode}\t"
        f"{tutorial.robot}\t{prerequisites}\t{requirements}\t{tutorial.title}"
    )


def list_tutorials(robot: str | None = None, status_only: bool = False) -> int:
    statuses = progress()
    for tutorial in discover():
        if robot and tutorial.robot != robot:
            continue
        status = statuses.get(tutorial.tutorial_id, "pending")
        if status_only and status == "done":
            continue
        _print_tutorial(tutorial, status)
    return 0


def next_tutorial() -> int:
    statuses = progress()
    for tutorial in discover():
        status = statuses.get(tutorial.tutorial_id, "pending")
        if status not in {"pending", "blocked-retry"}:
            continue
        if all(statuses.get(item) == "done" for item in tutorial.prerequisites):
            _print_tutorial(tutorial, status)
            return 0
    print("no-eligible-tutorial")
    return 1


def list_robots() -> int:
    names = set(PUBLIC_ROBOTS)
    names.update(discover_robot_plugins())
    for name in sorted(names):
        print(name)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pal")
    commands = parser.add_subparsers(dest="command", required=True)
    doctor_parser = commands.add_parser("doctor")
    doctor_parser.add_argument("--format", choices=("text", "json"), default="text")
    tutorial = commands.add_parser("tutorial")
    tutorial_commands = tutorial.add_subparsers(dest="tutorial_command", required=True)
    tutorial_list = tutorial_commands.add_parser("list")
    tutorial_list.add_argument("--robot")
    tutorial_commands.add_parser("status")
    tutorial_commands.add_parser("next")
    robot = commands.add_parser("robot")
    robot_commands = robot.add_subparsers(dest="robot_command", required=True)
    robot_commands.add_parser("list")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return doctor(args.format)
    if args.command == "tutorial":
        if args.tutorial_command == "next":
            return next_tutorial()
        return list_tutorials(
            getattr(args, "robot", None), status_only=args.tutorial_command == "status"
        )
    if args.command == "robot" and args.robot_command == "list":
        return list_robots()
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())
