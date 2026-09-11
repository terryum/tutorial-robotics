"""Refresh only catalog metadata, indexes and navigation; never overwrite authored bodies or tests."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def metadata(lesson: dict) -> str:
    fields = {
        "Stage / track": f"{lesson['stage']} / {lesson['track']}",
        "Legacy alias": ", ".join(lesson["aliases"]) or "None",
        "Platforms": ", ".join(lesson["platforms"]),
        "Capabilities": ", ".join(lesson["capabilities"]),
        "Prerequisites": ", ".join(lesson["prerequisites"]) or "None",
        "Safety": lesson["safety_level"],
        "Verification": lesson["verification"],
        "Implementation": lesson["implementation"],
    }
    return "| Field | Value |\n|---|---|\n" + "\n".join(
        f"| {key} | `{value}` |" for key, value in fields.items()
    )


def managed(text: str, name: str, content: str) -> str:
    opening, closing = f"<!-- pal:{name}:start -->", f"<!-- pal:{name}:end -->"
    block = opening + "\n" + content + "\n" + closing
    pattern = re.compile(re.escape(opening) + r".*?" + re.escape(closing), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda match: block, text)
    if name == "metadata":
        table = re.compile(r"\| Field \| Value \|\n\|---\|---\|\n(?:\|.*\|\n)+")
        if table.search(text):
            return table.sub(lambda match: block + "\n", text, count=1)
        first, rest = text.split("\n", 1)
        return first + "\n\n" + block + "\n" + rest
    if "## Next lesson" in text:
        return text.split("## Next lesson", 1)[0] + block + "\n"
    return text.rstrip() + "\n\n" + block + "\n"


def main() -> None:
    lessons = sorted(
        json.loads((ROOT / "curriculum/catalog.json").read_text())["lessons"],
        key=lambda row: row["order"],
    )
    for language in ("en", "ko"):
        rows = [
            "# " + ("수업 목록" if language == "ko" else "Lesson index"),
            "",
            "| # | Lesson | Stage | Track | Verification |",
            "|---:|---|---|---|---|",
        ]
        for index, lesson in enumerate(lessons):
            path = ROOT / "docs" / language / "lessons" / f"{lesson['id']}.md"
            if not path.is_file():
                raise FileNotFoundError(f"Author {path} before refreshing catalog metadata")
            title = lesson["title_ko"] if language == "ko" else lesson["title"]
            text = managed(path.read_text(), "metadata", metadata(lesson))
            following = lessons[index + 1] if index + 1 < len(lessons) else None
            link = (
                f"[{following['id']}](./{following['id']}.md)"
                if following
                else ("과정 끝" if language == "ko" else "Course end")
            )
            text = managed(
                text,
                "navigation",
                "## Next lesson\n\n"
                + link
                + "\n\n"
                + (
                    "다음 항목은 목차 순서입니다. 실제 선택은 `pal course next --json`이 준비 상태로 결정합니다."
                    if language == "ko"
                    else "This is catalog order. Use `pal course next --json` to select an eligible lesson."
                ),
            )
            path.write_text(text)
            rows.append(
                f"| {lesson['order']} | [{lesson['id']}](lessons/{lesson['id']}.md) — {title} | `{lesson['stage']}` | `{lesson['track']}` | `{lesson['verification']}` |"
            )
        (ROOT / "docs" / language / "index.md").write_text("\n".join(rows) + "\n")
    readme = ROOT / "README.md"
    rows = ["| # | ID / alias | English | 한국어 |", "|---:|---|---|---|"]
    for lesson in lessons:
        rows.append(
            f"| {lesson['order']} | {lesson['id']} / {', '.join(lesson['aliases'])} | [{lesson['title']}](docs/en/lessons/{lesson['id']}.md) | [{lesson['title_ko']}](docs/ko/lessons/{lesson['id']}.md) |"
        )
    text = readme.read_text()
    opening, closing = "<!-- pal:toc:start -->", "<!-- pal:toc:end -->"
    block = opening + "\n" + "\n".join(rows) + "\n" + closing
    if opening in text:
        text = re.sub(
            re.escape(opening) + r".*?" + re.escape(closing),
            lambda match: block,
            text,
            flags=re.DOTALL,
        )
    else:
        text += "\n" + block + "\n"
    readme.write_text(text)
    print(
        f"refreshed {len(lessons)} metadata/navigation pairs; authored bodies, entrypoints and tests preserved"
    )


if __name__ == "__main__":
    main()
