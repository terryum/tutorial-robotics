import importlib.util
import json
import shutil

from pai_lab.catalog import ROOT


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
