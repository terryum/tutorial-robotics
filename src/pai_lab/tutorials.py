"""Tutorial discovery without private-repository dependencies."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[2]
TUTORIAL_ROOT = ROOT / "tutorials"
FRONTMATTER = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


@dataclass(frozen=True)
class Tutorial:
    tutorial_id: str
    title: str
    robot: str
    prerequisites: tuple[str, ...]
    path: Path


def _field(block: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*[\"']?([^\n\"']*)", block, re.MULTILINE)
    return match.group(1).strip() if match else ""


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
        raw = _field(block, "prerequisites").strip("[]")
        prerequisites = tuple(item.strip() for item in raw.split(",") if item.strip())
        tutorials.append(Tutorial(tutorial_id, title, path.parent.name, prerequisites, path))
    return tuple(tutorials)


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

