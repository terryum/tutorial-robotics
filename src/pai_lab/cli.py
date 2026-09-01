"""The public `pal` command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path
import platform
import sys

from pai_lab.plugins import discover_robot_plugins
from pai_lab.tutorials import ROOT, discover, validate_graph


PUBLIC_ROBOTS = ("fr3", "unitree-g1", "wuji-hand2", "sharpa-wave", "aloha")


def doctor() -> int:
    errors = validate_graph()
    checks = {
        "repository": ROOT.is_dir(),
        "tutorials": bool(discover()),
        "python-3.12": sys.version_info[:2] == (3, 12),
        "private-required": False,
    }
    print(f"host={platform.system()} {platform.machine()}")
    for name, value in checks.items():
        print(f"{name}={value}")
    for error in errors:
        print(f"graph-error={error}")
    return 1 if errors or not all(value for key, value in checks.items() if key != "private-required") else 0


def list_tutorials(robot: str | None = None) -> int:
    for tutorial in discover():
        if robot and tutorial.robot != robot:
            continue
        prerequisites = ",".join(tutorial.prerequisites) or "-"
        print(f"{tutorial.tutorial_id}\t{tutorial.robot}\t{prerequisites}\t{tutorial.title}")
    return 0


def list_robots() -> int:
    names = set(PUBLIC_ROBOTS)
    names.update(discover_robot_plugins())
    for name in sorted(names):
        print(name)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="pal")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor")
    tutorial = commands.add_parser("tutorial")
    tutorial_commands = tutorial.add_subparsers(dest="tutorial_command", required=True)
    tutorial_list = tutorial_commands.add_parser("list")
    tutorial_list.add_argument("--robot")
    tutorial_commands.add_parser("status")
    robot = commands.add_parser("robot")
    robot_commands = robot.add_subparsers(dest="robot_command", required=True)
    robot_commands.add_parser("list")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "doctor":
        return doctor()
    if args.command == "tutorial":
        return list_tutorials(getattr(args, "robot", None))
    if args.command == "robot" and args.robot_command == "list":
        return list_robots()
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())

