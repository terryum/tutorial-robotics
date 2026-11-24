"""Validate the connected bilingual book and optional built-site language navigation."""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


class Languages(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = {}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and attributes.get("lang") in {"en", "ko"}:
            self.links[attributes["lang"]] = attributes.get("href", "")


def built_page(site: Path, docs: Path, source: Path, flat: bool) -> Path:
    output = site / source.relative_to(docs).with_suffix(".html")
    if flat or source.name == "index.md":
        return output
    return output.with_suffix("") / "index.html"


def validate(site: Path | None = None) -> list[str]:
    errors = []
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text())["lessons"]
    spec = json.loads((ROOT / "curriculum/book-spec.json").read_text())
    ids = {row["id"] for row in catalog}
    if len(spec["lessons"]) != len(ids) or {row["id"] for row in spec["lessons"]} != ids:
        errors.append("Book manifest must cover every catalog ID exactly once")
    for language in ("en", "ko"):
        base = ROOT / "docs" / language
        chapters = {path.stem for path in (base / "concepts").glob("*.md")}
        if len(chapters) != 11:
            errors.append(f"{language}: expected eleven concept chapters")
        for row in spec["lessons"]:
            path = base / "lessons" / f"{row['id']}.md"
            text = path.read_text()
            if not any(
                f"../concepts/{concept}.md" in text for concept in row["prerequisite_concepts"]
            ):
                errors.append(f"{language}/{row['id']}: missing prerequisite-concept link")
            if not re.search(r"^### ", text, re.MULTILINE):
                errors.append(f"{language}/{row['id']}: missing authored explanation subsections")
    docs = ROOT / "docs"
    homes = {"en": docs / "index.md", "ko": docs / "ko/home.md"}
    flat = site is not None and (site / "ko/home.html").is_file()
    for path in (homes["en"], *(docs / "en").rglob("*.md"), *(docs / "ko").rglob("*.md")):
        if path in homes.values():
            translations = homes
        else:
            relative = path.relative_to(docs).parts[1:]
            translations = {
                language: docs.joinpath(language, *relative) for language in ("en", "ko")
            }

        links = Languages()
        links.feed(path.read_text())
        if set(links.links) != {"en", "ko"}:
            errors.append(f"{path.relative_to(ROOT)}: missing paired language choice")
            continue
        for language, href in links.links.items():
            if (path.parent / unquote(href)).resolve() != translations[language]:
                errors.append(f"{path.relative_to(ROOT)}: language switch changes page identity")
        if site:
            output = built_page(site, docs, path, flat)
            parser = Languages()
            parser.feed(output.read_text())
            if set(parser.links) != {"en", "ko"}:
                errors.append(f"{output}: missing rendered language choice")
            for language, href in parser.links.items():
                destination = (output.parent / unquote(urlsplit(href).path)).resolve()
                if destination.is_dir():
                    destination /= "index.html"
                if (
                    destination != built_page(site, docs, translations[language], flat)
                    or not destination.is_file()
                ):
                    errors.append(f"{output}: broken rendered language switch {href}")
    for filename in ("README.md", "README.ko.md"):
        links = Languages()
        links.feed((ROOT / filename).read_text())
        if links.links != {"ko": "README.ko.md", "en": "README.md"}:
            errors.append(f"{filename}: README choice must go to corresponding README")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    errors = validate(args.site.resolve() if args.site else None)
    if errors:
        print("\n".join(errors))
        return 1
    print(
        "passed: complete bilingual catalog, eleven concept pairs, README and page-identity navigation"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
