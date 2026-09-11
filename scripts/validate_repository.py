from __future__ import annotations

import re
from urllib.parse import unquote

from pai_lab.assets import check_sources
from pai_lab.catalog import ROOT, load_catalog, validate_catalog
from pai_lab.lessons import check_lesson, implementation_status
from pai_lab.lessons.runner import LESSON_SPECS

LINK = re.compile(r"!?\[[^]]*]\(([^)]+)\)")


def validate_links() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", ".venv", ".local"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in LINK.findall(text):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            relative = unquote(target.split("#", 1)[0])
            if relative and not (path.parent / relative).resolve().exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link {target}")
    return errors


def main() -> int:
    lessons = load_catalog()
    errors = validate_catalog() + check_sources() + validate_links()
    for lesson in lessons:
        errors.extend(check_lesson(lesson.id))
        if lesson.implementation != implementation_status(lesson.id):
            errors.append(
                f"{lesson.id}: catalog says {lesson.implementation}, runner says "
                f"{implementation_status(lesson.id)}"
            )
    operations = [spec.operation for spec in LESSON_SPECS.values()]
    if len(operations) != len(set(operations)):
        errors.append("implemented lessons must not reuse a generic operation")
    generic = {"summary.json", "trace.csv", "lesson-report.md"}
    for lesson_id, spec in LESSON_SPECS.items():
        if spec.artifact in generic:
            errors.append(f"{lesson_id}: semantic artifact is generic")
        if spec.operation in {"baseline", "sine", "generic"}:
            errors.append(f"{lesson_id}: generic fallback operation is forbidden")
        lesson = next(item for item in lessons if item.id == lesson_id)
        if spec.artifact not in lesson.expected_artifacts:
            errors.append(f"{lesson_id}: catalog omits semantic artifact {spec.artifact}")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(lessons)} catalog lessons, bilingual contracts, sources, and links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
