"""Compatibility layer for the pre-v1 tutorial registry."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from pai_lab.catalog import ROOT, Lesson, load_catalog, validate_catalog


@dataclass(frozen=True)
class Tutorial:
    tutorial_id: str
    title: str
    robot: str
    prerequisites: tuple[str, ...]
    mode: str
    requirements: tuple[str, ...]
    path: Path


def _compatibility_node(lesson: Lesson) -> Tutorial:
    return Tutorial(
        tutorial_id=lesson.id,
        title=lesson.title,
        robot=lesson.track,
        prerequisites=lesson.prerequisites,
        mode="robot-runtime" if lesson.stage == "hardware" else "development",
        requirements=lesson.capabilities,
        path=ROOT / "docs" / "en" / "lessons" / f"{lesson.id}.md",
    )


def discover() -> tuple[Tutorial, ...]:
    return tuple(_compatibility_node(lesson) for lesson in load_catalog())


def progress() -> dict[str, str]:
    path = ROOT / "state" / "PUBLISHING.md"
    statuses: dict[str, str] = {}
    if not path.is_file():
        return statuses
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*([a-z0-9-]+)\s*\|.*?\|\s*([^| ]+)\s*\|", line)
        if match:
            statuses[match.group(1)] = match.group(2)
    return statuses


def validate_graph() -> list[str]:
    return validate_catalog()
