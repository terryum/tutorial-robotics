from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("manuals", ROOT / "scripts/manuals.py")
manuals = importlib.util.module_from_spec(spec)
spec.loader.exec_module(manuals)


def test_html_error_cannot_be_imported_as_pdf():
    # The signature guard runs before the optional PDF parser is needed.
    pytest.importorskip("pypdf")
    with pytest.raises(ValueError, match="Expected PDF"):
        manuals.validate(b"<html>404 Not Found</html>", "pdf")


def test_import_reuse_changed_version_and_corruption(tmp_path):
    pytest.importorskip("pypdf")
    from io import BytesIO

    from pypdf import PdfWriter

    def pdf(width):
        buf = BytesIO()
        writer = PdfWriter()
        writer.add_blank_page(width=width, height=200)
        writer.write(buf)
        return buf.getvalue()

    entry = {
        "id": "test-manual",
        "device": "fr3",
        "format": "pdf",
        "source": "user-provided:test",
        "versions": [],
    }
    original = pdf(200)
    first = manuals.acquire(entry, original, tmp_path)
    assert (tmp_path / first["path"]).read_bytes() == original
    assert manuals.acquire(entry, original, tmp_path) == first
    assert len(entry["versions"]) == 1
    second = manuals.acquire(entry, pdf(300), tmp_path)
    assert first["path"] != second["path"]
    assert len(entry["versions"]) == 2
    (tmp_path / first["path"]).write_bytes(b"<html>error</html>")
    assert manuals.verify_version(first, tmp_path)
    with pytest.raises(ValueError, match="damaged"):
        manuals.acquire(entry, original, tmp_path)


def test_path_escape_blocked(tmp_path):
    with pytest.raises(ValueError):
        manuals.local_path(tmp_path, "../outside.pdf")


def test_offline_html_images_and_dynamic_shell(tmp_path, monkeypatch):
    pytest.importorskip("bs4")
    with pytest.raises(ValueError, match="shell"):
        manuals.validate(b'<html><div id="root"></div></html>', "html")
    monkeypatch.setattr(manuals, "fetch", lambda url: b"fake-image-for-link-test")
    html = b'<html><body><article><h1>Manual</h1><p>Body instruction.</p><img src="image.png"><script>connect()</script></article></body></html>'
    reading = manuals.offline_html(html, "https://example.com/manual/", tmp_path, "Manual")
    assert b"<script" not in reading
    assert b'src="images/' in reading
    assert len(list((tmp_path / "images").glob("*"))) == 1


def test_dynamic_section_extraction_never_executes_javascript():
    import json

    sections = [
        {
            "id": "one",
            "title": "Manual",
            "blocks": [{"type": "paragraph", "text": "Actual content"}],
        }
    ]
    literal = json.dumps(sections).replace("\\", "\\\\").replace("'", "\\'")
    assert (
        manuals.extract_sharpa_sections(
            "throw Error('must not execute'); JSON.parse('" + literal + "')"
        )
        == sections
    )
    with pytest.raises(ValueError, match="bodies"):
        manuals.extract_sharpa_sections('document.body.innerHTML = "Loading"')


def test_web_import_preserves_body_images_and_code_lines(tmp_path, monkeypatch):
    pytest.importorskip("bs4")
    pytest.importorskip("reportlab")
    pytest.importorskip("pypdf")
    from io import BytesIO

    from PIL import Image
    from pypdf import PdfReader

    buf = BytesIO()
    Image.new("RGB", (8, 8), "blue").save(buf, format="PNG")
    monkeypatch.setattr(manuals, "fetch", lambda url: buf.getvalue())
    original = b'<html><body><h1>Installation</h1><p>Review all installation instructions before using the device. This offline test includes real image bytes and a table.</p><pre>first_line()\nsecond_line()\ndef callback():\n    nested_call()</pre><table><tr><th>Unit</th><th>Value</th></tr><tr><td>A</td><td>0.1</td></tr></table><img src="plot.png"></body></html>'
    entry = {
        "id": "web",
        "device": "g1",
        "title": "Web test",
        "source": "https://example.com/manual",
        "format": "html",
        "versions": [],
    }
    result = manuals.acquire(entry, original, tmp_path)
    assert not manuals.verify_version(result, tmp_path)
    assert (tmp_path / result["path"]).read_bytes() == original
    pdf = PdfReader(tmp_path / result["derived"][1]["path"])
    text = "\n".join(p.extract_text() for p in pdf.pages)
    assert "first_line()\nsecond_line()" in text
    assert "def callback():\n    nested_call()" in text
    assert sum(len(p.images) for p in pdf.pages) == 1


def test_merged_table_cells_keep_column_context():
    bs4 = pytest.importorskip("bs4")
    table = bs4.BeautifulSoup(
        '<table><tr><th>Group</th><th>Parameter</th><th>Value</th></tr>'
        '<tr><td rowspan="2">Power</td><td>Voltage</td><td>12 V</td></tr>'
        '<tr><td>Current</td><td>20 A</td></tr>'
        '<tr><td colspan="2">Note</td><td>Check revision</td></tr></table>',
        "html.parser",
    ).table
    assert manuals.table_grid(table) == [
        ["Group", "Parameter", "Value"],
        ["Power", "Voltage", "12 V"],
        ["Power", "Current", "20 A"],
        ["Note", "Note", "Check revision"],
    ]
