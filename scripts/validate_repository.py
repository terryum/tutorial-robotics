from __future__ import annotations

import re
from urllib.parse import unquote

from pai_lab.assets import check_sources
from pai_lab.catalog import ROOT, load_catalog, validate_catalog
from pai_lab.lessons import check_lesson

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
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(lessons)} catalog lessons, bilingual contracts, sources, and links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
