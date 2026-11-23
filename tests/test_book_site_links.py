import importlib.util

from pai_lab.catalog import ROOT


def test_site_rewrites_existing_repository_sources_only(tmp_path):
    spec = importlib.util.spec_from_file_location("book_hooks", ROOT / "scripts/mkdocs_hooks.py")
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    source = tmp_path / "docs/en/lesson.md"
    source.parent.mkdir(parents=True)
    source.write_text("authored source sentinel")
    (source.parent / "next.md").write_text("next")
    code = tmp_path / "src/example.py"
    code.parent.mkdir()
    code.write_text("example")
    text = (
        "[source](../../src/example.py#L1) [next](next.md) "
        "[missing](../../src/absent.py) [web](https://example.com/page) "
        "[anchor](#local)"
    )
    rendered = hook.render_source_links(text, source, tmp_path)
    assert (
        "[source](https://github.com/terryum/tutorial-robotics/blob/main/src/example.py#L1)"
        in rendered
    )
    assert "[next](next.md)" in rendered
    assert "[missing](../../src/absent.py)" in rendered
    assert "[web](https://example.com/page)" in rendered
    assert "[anchor](#local)" in rendered
    assert source.read_text() == "authored source sentinel"


def test_raw_html_language_switch_round_trips_rendered_directories(tmp_path):
    spec = importlib.util.spec_from_file_location("book_hooks", ROOT / "scripts/mkdocs_hooks.py")
    hook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hook)
    for language in ("en", "ko"):
        page = tmp_path / f"docs/{language}/lessons/one.md"
        page.parent.mkdir(parents=True)
        page.write_text("one")
        (tmp_path / f"docs/{language}/index.md").write_text("map")
    lesson = tmp_path / "docs/ko/lessons/one.md"
    text = '<a href="../../en/lessons/one.md" lang="en">ENGLISH</a>'
    assert "../../../en/lessons/one/" in hook.render_language_links(text, lesson, tmp_path)
    index = tmp_path / "docs/en/index.md"
    text = '<a href="../ko/index.md" lang="ko">한국어</a>'
    assert 'href="../ko/"' in hook.render_language_links(text, index, tmp_path)
