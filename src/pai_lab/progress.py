"""Machine-local course selection and progress."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT, STAGES, Lesson, Stage

PROGRESS_PATH = ROOT / ".local" / "progress.json"
STAGE_RANK = {stage: index for index, stage in enumerate(STAGES)}


@dataclass
class CourseProgress:
    through: Stage
    robots: tuple[str, ...]
    include_electives: bool
    completed: dict[str, dict[str, Any]]

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "through": self.through,
            "robots": list(self.robots),
            "include_electives": self.include_electives,
            "completed": self.completed,
        }


def default_progress() -> CourseProgress:
    return CourseProgress("core", (), False, {})


def load_progress(path: Path | None = None) -> CourseProgress:
    path = path or PROGRESS_PATH
    if not path.is_file():
        return default_progress()
    raw = json.loads(path.read_text(encoding="utf-8"))
    return CourseProgress(
        through=raw.get("through", "core"),
        robots=tuple(raw.get("robots", [])),
        include_electives=bool(raw.get("include_electives", False)),
        completed=dict(raw.get("completed", {})),
    )


def save_progress(progress: CourseProgress, path: Path | None = None) -> None:
    path = path or PROGRESS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(progress.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def select_lesson(lesson: Lesson, progress: CourseProgress) -> bool:
    if STAGE_RANK[lesson.stage] > STAGE_RANK[progress.through]:
        return False
    if lesson.elective and not progress.include_electives:
        return False
    if lesson.track in {"common", "learning", "deployment", "cross", "ros2", "isaac", "vla", "dexterity"}:
        return True
    if not progress.robots:
        return lesson.stage != "hardware"
    selected = set(progress.robots)
    return lesson.track in selected or set(lesson.track.split("-")) <= selected


def mark_complete(progress: CourseProgress, lesson: Lesson, run_dir: Path) -> None:
    try:
        recorded_dir = str(run_dir.relative_to(ROOT))
    except ValueError:
        recorded_dir = str(run_dir)
    progress.completed[lesson.id] = {
        "completed_at": datetime.now(UTC).isoformat(),
        "verification": lesson.verification,
        "run_dir": recorded_dir,
    }
