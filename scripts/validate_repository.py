from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

from pai_lab.tutorials import ROOT, discover, validate_graph


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
    tutorials = discover()
    ids = [tutorial.tutorial_id for tutorial in tutorials]
    errors = validate_graph() + validate_links()
    duplicates = sorted({tutorial_id for tutorial_id in ids if ids.count(tutorial_id) > 1})
    errors.extend(f"duplicate tutorial id: {tutorial_id}" for tutorial_id in duplicates)
    for tutorial in tutorials:
        if not tutorial.mode:
            errors.append(f"{tutorial.path.relative_to(ROOT)}: missing mode")
        if not tutorial.requirements:
            errors.append(f"{tutorial.path.relative_to(ROOT)}: missing requires")
    if errors:
        print("\n".join(errors))
        return 1
    print(f"validated {len(tutorials)} tutorials and Markdown links")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
