"""Named curricula independent of legacy catalog ordering and stage filtering."""

from __future__ import annotations

import json
from typing import Any

from pai_lab.catalog import ROOT, load_catalog


def load_paths() -> dict[str, Any]:
    return dict(json.loads((ROOT / "curriculum/paths.json").read_text())["paths"])


def path_lessons(name: str) -> tuple[str, ...]:
    paths = load_paths()
    if name not in paths:
        raise ValueError(f"unknown course path: {name}")
    return tuple(paths[name]["required"])


def validate_paths() -> list[str]:
    catalog = {lesson.id: lesson for lesson in load_catalog()}
    errors = []
    for name in load_paths():
        required = path_lessons(name)
        if not required or len(set(required)) != len(required):
            errors.append(f"{name}: empty or duplicate required lessons")
        for index, identifier in enumerate(required):
            if identifier not in catalog:
                errors.append(f"{name}: unknown lesson {identifier}")
            elif not set(catalog[identifier].prerequisites) <= set(required[:index]):
                errors.append(f"{name}: prerequisites must precede {identifier}")
    return errors


def selected_lessons() -> tuple[Any, ...]:
    from pai_lab.progress import load_progress, select_lesson

    progress = load_progress()
    catalog = load_catalog()
    if progress.path:
        by_id = {lesson.id: lesson for lesson in catalog}
        return tuple(by_id[identifier] for identifier in path_lessons(progress.path))
    return tuple(lesson for lesson in catalog if select_lesson(lesson, progress))
