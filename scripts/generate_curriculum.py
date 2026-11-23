"""Refresh only catalog metadata, indexes and navigation; never overwrite authored bodies or tests."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def language_switch(text: str, path: Path, relative: Path) -> str:
    """Prepend paired, branch-relative links without touching the authored body."""
    links = []
    for language, label in (("ko", "한국어"), ("en", "ENGLISH")):
        target = ROOT / "docs" / language / relative
        if not target.is_file():
            raise FileNotFoundError(f"Missing translation: {target}")
        href = Path(os.path.relpath(target, path.parent)).as_posix()
        links.append(f'<a href="{href}" lang="{language}">{label}</a>')
    opening, closing = "<!-- pal:language:start -->", "<!-- pal:language:end -->"
    text = re.sub(
        re.escape(opening) + r".*?" + re.escape(closing) + r"\n*",
        "",
        text,
        flags=re.DOTALL,
    )
    return (
        opening
        + '\n<p align="right">\n  '
        + " | ".join(links)
        + "\n</p>\n"
        + closing
        + "\n\n"
        + text
    )


def readme_switch(text: str) -> str:
    """README language choice stays at the repository entrance."""
    opening, closing = "<!-- pal:language:start -->", "<!-- pal:language:end -->"
    text = re.sub(
        re.escape(opening) + r".*?" + re.escape(closing) + r"\n*", "", text, flags=re.DOTALL
    )
    return (
        opening + '\n<p align="right">\n  '
        '<a href="README.ko.md" lang="ko">한국어</a> | '
        '<a href="README.md" lang="en">ENGLISH</a>\n</p>\n' + closing + "\n\n" + text
    )


def learning_goal(text: str) -> str:
    """Use the authored first paragraph, never substitute catalog titles."""
    match = re.search(
        r"^## Learning goals\s*\n(.*?)(?=\n\s*\n|\n## |\Z)", text, re.MULTILINE | re.DOTALL
    )
    if not match or not match[1].strip():
        raise ValueError("Lesson needs a Learning goals first paragraph")
    return " ".join(match[1].split()).replace("|", "\\|")


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
            "| # | Lesson | Stage | Track | Verification |",
            "|---:|---|---|---|---|",
        ]
        summaries = [
            "| Lesson | Learning goal | Prerequisites | Platforms / capabilities | Implementation |",
            "|---|---|---|---|---|",
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
            summaries.append(
                f"| [{lesson['id']}](lessons/{lesson['id']}.md) | {learning_goal(text)} | "
                f"{', '.join(lesson['prerequisites']) or '—'} | "
                f"{', '.join(lesson['platforms'])}; {', '.join(lesson['capabilities'])} | "
                f"`{lesson['implementation']}` |"
            )
        index = ROOT / "docs" / language / "index.md"
        text = index.read_text()
        # Migrate the legacy table once; all other authored text survives.
        if "<!-- pal:catalog:start -->" not in text:
            text = re.sub(
                r"^\| # \| Lesson \| Stage \| Track \| Verification \|\n(?:\|.*\n)+",
                "",
                text,
                flags=re.MULTILINE,
            )
        index.write_text(managed(text, "catalog", "\n".join(rows)))
        overview = ROOT / "docs" / language / "lessons.md"
        if overview.exists():
            overview.write_text(managed(overview.read_text(), "goals", "\n".join(summaries)))
    rows = ["| # | ID / alias | English | 한국어 |", "|---:|---|---|---|"]
    for lesson in lessons:
        rows.append(
            f"| {lesson['order']} | {lesson['id']} / {', '.join(lesson['aliases'])} | [{lesson['title']}](docs/en/lessons/{lesson['id']}.md) | [{lesson['title_ko']}](docs/ko/lessons/{lesson['id']}.md) |"
        )
    for filename in ("README.md", "README.ko.md"):
        readme = ROOT / filename
        if readme.exists():
            readme.write_text(managed(readme.read_text(), "toc", "\n".join(rows)))
    # Include indexes and reader guides as well as every lesson pair.
    for language in ("en", "ko"):
        for path in (ROOT / "docs" / language).rglob("*.md"):
            relative = path.relative_to(ROOT / "docs" / language)
            path.write_text(language_switch(path.read_text(), path, relative))
    for filename in ("README.md", "README.ko.md"):
        path = ROOT / filename
        if path.exists():
            path.write_text(readme_switch(path.read_text()))
    print(
        f"refreshed {len(lessons)} metadata/navigation pairs; authored bodies, entrypoints and tests preserved"
    )


if __name__ == "__main__":
    main()
