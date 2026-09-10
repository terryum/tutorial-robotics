"""Typed access to the versioned curriculum catalog."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, cast

ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = ROOT / "curriculum" / "catalog.json"
Stage = Literal["core", "sim", "hardware"]
STAGES: tuple[Stage, ...] = ("core", "sim", "hardware")


@dataclass(frozen=True)
class Lesson:
    """One executable curriculum node."""

    id: str
    aliases: tuple[str, ...]
    stage: Stage
    track: str
    order: int
    title: str
    title_ko: str
    platforms: tuple[str, ...]
    capabilities: tuple[str, ...]
    prerequisites: tuple[str, ...]
    elective: bool
    entrypoint: str
    check: str
    expected_artifacts: tuple[str, ...]
    source_refs: tuple[str, ...]
    verification: str
    safety_level: str
    implementation: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Lesson:
        return cls(
            id=str(value["id"]),
            aliases=tuple(str(item) for item in value["aliases"]),
            stage=cast(Stage, value["stage"]),
            track=str(value["track"]),
            order=int(value["order"]),
            title=str(value["title"]),
            title_ko=str(value["title_ko"]),
            platforms=tuple(str(item) for item in value["platforms"]),
            capabilities=tuple(str(item) for item in value["capabilities"]),
            prerequisites=tuple(str(item) for item in value["prerequisites"]),
            elective=bool(value["elective"]),
            entrypoint=str(value["entrypoint"]),
            check=str(value["check"]),
            expected_artifacts=tuple(str(item) for item in value["expected_artifacts"]),
            source_refs=tuple(str(item) for item in value["source_refs"]),
            verification=str(value["verification"]),
            safety_level=str(value["safety_level"]),
            implementation=str(
                value.get(
                    "implementation",
                    "scaffolded" if str(value["id"]) in {
                        "hw-common-02",
                        "hw-fr3-01",
                        "hw-wuji-01",
                        "hw-wuji-02",
                        "hw-enlight-01",
                        "hw-enlight-02",
                        "hw-enlight-03",
                        "hw-enlight-wuji-01",
                    } else "implemented",
                )
            ),
        )


def load_catalog(path: Path = CATALOG_PATH) -> tuple[Lesson, ...]:
    """Load lessons in stable curriculum order."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    lessons = [Lesson.from_dict(item) for item in raw["lessons"]]
    return tuple(sorted(lessons, key=lambda lesson: lesson.order))


def lesson_map() -> dict[str, Lesson]:
    """Return canonical and legacy IDs mapped to the same lesson."""

    result: dict[str, Lesson] = {}
    for lesson in load_catalog():
        result[lesson.id.lower()] = lesson
        result.update({alias.lower(): lesson for alias in lesson.aliases})
    return result


def resolve_lesson(identifier: str) -> Lesson:
    """Resolve a canonical lesson ID or one-major-release legacy alias."""

    try:
        return lesson_map()[identifier.lower()]
    except KeyError as error:
        raise ValueError(f"unknown lesson: {identifier}") from error


def validate_catalog() -> list[str]:
    """Validate IDs, aliases, graph closure, paths, and enumerated values."""

    lessons = load_catalog()
    errors: list[str] = []
    ids = [lesson.id for lesson in lessons]
    aliases = [alias.lower() for lesson in lessons for alias in lesson.aliases]
    known = set(ids)
    if len(lessons) != 49:
        errors.append(f"expected 49 lessons, found {len(lessons)}")
    if len(set(ids)) != len(ids):
        errors.append("duplicate canonical lesson id")
    if len(set(aliases)) != len(aliases):
        errors.append("duplicate legacy alias")
    if [lesson.order for lesson in lessons] != list(range(1, len(lessons) + 1)):
        errors.append("lesson order must be consecutive starting at 1")
    for lesson in lessons:
        if lesson.stage not in STAGES:
            errors.append(f"{lesson.id}: invalid stage {lesson.stage}")
        if lesson.verification not in {
            "ci-checked",
            "maintainer-checked",
            "reader_test_required",
        }:
            errors.append(f"{lesson.id}: invalid verification {lesson.verification}")
        if lesson.implementation not in {"implemented", "scaffolded"}:
            errors.append(f"{lesson.id}: invalid implementation {lesson.implementation}")
        if lesson.implementation == "scaffolded" and lesson.verification != "reader_test_required":
            errors.append(f"{lesson.id}: scaffolded lesson must require reader testing")
        if not lesson.source_refs:
            errors.append(f"{lesson.id}: source_refs is empty")
        for prerequisite in lesson.prerequisites:
            if prerequisite not in known:
                errors.append(f"{lesson.id}: unknown prerequisite {prerequisite}")
            elif load_catalog()[ids.index(prerequisite)].order >= lesson.order:
                errors.append(f"{lesson.id}: prerequisite is not earlier: {prerequisite}")
        for relative in (
            lesson.entrypoint,
            f"docs/en/lessons/{lesson.id}.md",
            f"docs/ko/lessons/{lesson.id}.md",
        ):
            if not (ROOT / relative).is_file():
                errors.append(f"{lesson.id}: missing {relative}")
    return errors
