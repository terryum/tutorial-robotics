"""Tutorial discovery without private-repository dependencies."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TUTORIAL_ROOT = ROOT / "tutorials"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class Tutorial:
    tutorial_id: str
    title: str
    robot: str
    prerequisites: tuple[str, ...]
    mode: str
    requirements: tuple[str, ...]
    path: Path


def _field(block: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*[\"']?([^\n\"']*)", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def _list_field(block: str, name: str) -> tuple[str, ...]:
    raw = _field(block, name).strip("[]")
    return tuple(item.strip() for item in raw.split(",") if item.strip())


def discover() -> tuple[Tutorial, ...]:
    tutorials: list[Tutorial] = []
    for path in sorted(TUTORIAL_ROOT.glob("*/*.md")):
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            continue
        block = match.group(1)
        tutorial_id = _field(block, "id")
        title = _field(block, "title")
        tutorials.append(
            Tutorial(
                tutorial_id=tutorial_id,
                title=title,
                robot=path.parent.name,
                prerequisites=_list_field(block, "prerequisites"),
                mode=_field(block, "mode") or "development",
                requirements=_list_field(block, "requires"),
                path=path,
            )
        )
    def sort_key(tutorial: Tutorial) -> tuple[int, str]:
        match = re.match(r"T(\d+)(.*)", tutorial.tutorial_id)
        return (int(match.group(1)), match.group(2)) if match else (9999, tutorial.tutorial_id)

    return tuple(sorted(tutorials, key=sort_key))


def progress() -> dict[str, str]:
    path = ROOT / "state" / "PROGRESS.md"
    statuses: dict[str, str] = {}
    if not path.exists():
        return statuses
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(T\w+)\s*\|.*?\|\s*([^| ]+)\s*\|", line)
        if match:
            statuses[match.group(1)] = match.group(2)
    return statuses


def validate_graph() -> list[str]:
    tutorials = discover()
    ids = {tutorial.tutorial_id for tutorial in tutorials}
    errors: list[str] = []
    for tutorial in tutorials:
        if not tutorial.tutorial_id:
            errors.append(f"missing id: {tutorial.path}")
        for prerequisite in tutorial.prerequisites:
            if prerequisite not in ids:
                errors.append(
                    f"{tutorial.tutorial_id}: unknown prerequisite {prerequisite}"
                )
    return errors
