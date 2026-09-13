import importlib.util
import json
import shutil
from html.parser import HTMLParser

from pai_lab.catalog import ROOT


class LanguageLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and attrs.get("lang") in {"ko", "en"}:
            self.links[attrs["lang"]] = attrs["href"]


def test_generator_preserves_authored_bodies_entrypoints_and_tests(tmp_path):
    spec = importlib.util.spec_from_file_location(
        "curriculum_generator", ROOT / "scripts/generate_curriculum.py"
    )
    generator = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator)
    shutil.copytree(ROOT / "docs", tmp_path / "docs")
    shutil.copytree(ROOT / "curriculum", tmp_path / "curriculum")
    shutil.copyfile(ROOT / "README.md", tmp_path / "README.md")
    test = tmp_path / "tests/lessons/test_core_00.py"
    test.parent.mkdir(parents=True)
    test.write_text("# authored test sentinel\n")
    entry = tmp_path / "examples/core-00/run.py"
    entry.parent.mkdir(parents=True)
    entry.write_text("# authored entry sentinel\n")
    doc = tmp_path / "docs/en/lessons/core-00.md"
    doc.write_text(doc.read_text().replace("## Action", "Authored body sentinel.\n\n## Action"))
    generator.ROOT = tmp_path
    generator.main()
    first = doc.read_bytes()
    generator.main()
    assert doc.read_bytes() == first
    assert "Authored body sentinel." in doc.read_text()
    assert test.read_text() == "# authored test sentinel\n"
    assert entry.read_text() == "# authored entry sentinel\n"
    catalog = sorted(
        json.loads((tmp_path / "curriculum/catalog.json").read_text())["lessons"],
        key=lambda row: row["order"],
    )
    for i, lesson in enumerate(catalog[:-1]):
        for lang in ("en", "ko"):
            page = (tmp_path / f"docs/{lang}/lessons/{lesson['id']}.md").read_text()
            assert f"(./{catalog[i + 1]['id']}.md)" in page.split("## Next lesson")[1]
    for language in ("ko", "en"):
        for path in (tmp_path / "docs" / language).rglob("*.md"):
            relative = path.relative_to(tmp_path / "docs" / language)
            page = path.read_text()
            parser = LanguageLinks()
            parser.feed(page.split("<!-- pal:language:end -->")[0])
            assert set(parser.links) == {"ko", "en"}
            for target_language, href in parser.links.items():
                # Switching preserves chapter/guide identity and round-trips locally.
                target = (path.parent / href).resolve()
                assert target == tmp_path / "docs" / target_language / relative
                assert target.is_file()
            assert page.count("<!-- pal:language:start -->") == 1
            assert page.index('<p align="right">') < page.index("# ")
