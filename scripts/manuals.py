"""Local-only manual library; optional dependencies: uv sync --extra manuals.

Content-addressed versions are immutable. No vendor code or hardware SDK is imported.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "assets/manuals.json"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch(url: str) -> bytes:
    if urlparse(url).scheme != "https":
        raise ValueError("Only HTTPS sources are supported")
    request = Request(url, headers={"User-Agent": "Mozilla/5.0 (manual-library)"})
    with urlopen(request, timeout=60) as response:
        if urlparse(response.url).scheme != "https":
            raise ValueError("Non-HTTPS redirect")
        return response.read()


def fetch_document(entry: dict) -> tuple[bytes, dict[str, bytes]]:
    """Fetch ordinary originals or safely extract the Sharpa application data."""
    data = fetch(entry["source"])
    if entry["id"] != "sharpa-manual":
        return data, {}
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(data, "html.parser")
    script = soup.find("script", src=True)
    if script is None:
        raise ValueError("Sharpa application bundle not found")
    bundle = fetch(urljoin(entry["source"], script["src"]))
    sections = extract_sharpa_sections(bundle.decode())
    from html import escape as html_escape

    def img(item: dict) -> str:
        # This application uses root-looking assets under its GitHub Pages prefix.
        source = urljoin(entry["source"], item["src"].lstrip("/"))
        return '<img src="' + html_escape(source, quote=True) + '">'

    def block(item: dict) -> str:
        kind = item["type"]
        text = html_escape(item.get("text", ""))
        if kind == "heading":
            return '<h2 id="' + html_escape(item["id"]) + '">' + text + "</h2>"
        if kind in {"paragraph", "callout"}:
            return "<p>" + text + "</p>"
        if kind in {"math", "code"}:
            return "<pre>" + html_escape(item["tex" if kind == "math" else "code"]) + "</pre>"
        if kind == "list":
            return (
                "<ul>"
                + "".join("<li>" + html_escape(i["text"]) + "</li>" for i in item["items"])
                + "</ul>"
            )
        if kind == "imageGrid":
            return "".join(img(i) for i in item["images"])
        if kind == "table":
            return (
                "<table>"
                + "".join(
                    "<tr>"
                    + "".join(
                        "<td>"
                        + html_escape(cell["text"])
                        + "".join(img(i) for i in cell.get("images", []))
                        + "</td>"
                        for cell in row
                    )
                    + "</tr>"
                    for row in item["rows"]
                )
                + "</table>"
            )
        raise ValueError(f"Unrecognized Sharpa section block: {kind}")

    result = (
        "<html><body><h1>Sharpa Wave: extracted section bodies from official application bundle</h1>"
        + "".join(
            "<h1>"
            + html_escape(section["title"])
            + "</h1>"
            + "".join(block(b) for b in section["blocks"])
            for section in sections
        )
        + "</body></html>"
    ).encode()
    return result, {
        "source-app.html": data,
        "source-bundle.js": bundle,
        "source-sections.json": json.dumps(sections, indent=2).encode(),
    }


def extract_sharpa_sections(bundle: str) -> list[dict]:
    # Decode string literals as data; never eval/execute a vendor script.
    literals = re.findall(r"JSON\.parse\('((?:\\.|[^'\\])*)'\)", bundle)
    for literal in literals:
        decoded = literal.replace("\\'", "'").replace("\\\\", "\\")
        try:
            value = json.loads(decoded)
        except json.JSONDecodeError:
            continue
        if (
            isinstance(value, list)
            and value
            and isinstance(value[0], dict)
            and "blocks" in value[0]
        ):
            return value
    raise ValueError("Actual Sharpa section bodies not found; refuse an empty app shell")


def validate(data: bytes, fmt: str) -> None:
    if fmt == "pdf":
        from io import BytesIO

        from pypdf import PdfReader

        if not data.startswith(b"%PDF-"):
            raise ValueError("Expected PDF bytes, possibly an HTML error page")
        if not PdfReader(BytesIO(data), strict=True).pages:
            raise ValueError("Empty PDF")
    elif fmt == "html":
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(data, "html.parser")
        if len(soup.get_text(strip=True)) < 120 and not soup.find("img"):
            raise ValueError("Empty/dynamic HTML shell: supply extracted section bodies")
        if re.search(
            r"^(access denied|403 forbidden|404 not found)",
            soup.get_text(strip=True),
            re.IGNORECASE,
        ):
            raise ValueError("HTML error page")
    else:
        raise ValueError(f"Unsupported format: {fmt}")


def local_path(root: Path, relative: str) -> Path:
    target = (root / relative).resolve()
    if not target.is_relative_to((root / ".local/manuals").resolve()):
        raise ValueError("Manual path must stay under .local/manuals")
    return target


def offline_html(data: bytes, url: str, directory: Path, title: str) -> bytes:
    """Self-contained, script-free reading copy; original HTML is retained separately."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(data, "html.parser")
    body = (
        soup.select_one("article")
        or soup.select_one('[role="main"]')
        or soup.find("main")
        or soup.body
        or soup
    )
    for item in body.select(
        "script, style, nav, header, footer, form, iframe, video, audio, a.headerlink"
    ):
        item.decompose()
    for item in body.find_all(True):
        for attr in list(item.attrs):
            if attr.startswith("on") or attr in {"style", "srcset"}:
                del item[attr]
    for img in body.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if not src:
            raise ValueError("Image without source")
        source = urljoin(url, src)
        image = fetch(source)
        suffix = Path(urlparse(source).path).suffix.lower()
        if suffix not in {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}:
            suffix = ".png"
        name = f"images/{digest(image)}{suffix}"
        path = directory / name
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(image)
        img.attrs = {"src": name, "alt": img.get("alt", "")}
    for link in body.find_all("a", href=True):
        link["href"] = urljoin(url, link["href"])
    css = "body{max-width:1000px;margin:32px auto;font:16px/1.6 sans-serif;padding:20px}img{max-width:100%;height:auto}table{border-collapse:collapse;max-width:100%;overflow-wrap:anywhere}td,th{border:1px solid #ccc;padding:6px}pre{white-space:pre-wrap;overflow-wrap:anywhere}"
    result = f'<!doctype html><html><head><meta charset="utf-8"><title>{escape(title)}</title><style>{css}</style></head><body><h1>{escape(title)}</h1><p>OFFLINE READING CONVERSION - not a vendor-issued document. Source: <a href="{escape(url)}">{escape(url)}</a></p>{body}</body></html>'.encode()
    validate(result, "html")
    return result


def table_grid(table) -> list[list[str]]:
    """Expand merged cells so PDF page breaks preserve each row's column context."""
    cells: dict[tuple[int, int], str] = {}
    rows = table.find_all("tr")
    for r, row in enumerate(rows):
        column = 0
        for cell in row.find_all(["td", "th"], recursive=False):
            while (r, column) in cells:
                column += 1
            text = cell.get_text(" ", strip=True)
            height = max(1, int(cell.get("rowspan", 1)))
            width = max(1, int(cell.get("colspan", 1)))
            for dr in range(height):
                for dc in range(width):
                    cells[r + dr, column + dc] = text
            column += width
    if not cells:
        return []
    columns = max(c for _, c in cells) + 1
    return [[cells.get((r, c), "") for c in range(columns)] for r in range(len(rows))]


def reading_pdf(html: Path, target: Path) -> None:
    """Reflow HTML into a labelled reading PDF, including every body image/table."""
    from bs4 import BeautifulSoup, NavigableString, Tag
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.platypus import (
        Image,
        KeepTogether,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    styles = getSampleStyleSheet()
    font = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")
    if font.exists():
        pdfmetrics.registerFont(TTFont("ManualUnicode", str(font)))
        for style in styles.byName.values():
            style.fontName = "ManualUnicode"
    styles["BodyText"].fontSize = 9
    styles["BodyText"].leading = 13
    styles["BodyText"].wordWrap = "CJK"
    story = []

    def paragraph(text: str, style: str = "BodyText", *, code: bool = False) -> None:
        if text.strip():
            text = re.sub(r"[\ue000-\uf8ff]", "", text)
            markup = escape(text.expandtabs(4) if code else text)
            if code:
                markup = re.sub(r"(?m)^ +", lambda m: "&nbsp;" * len(m[0]), markup)
            story.append(Paragraph(markup.replace("\n", "<br/>"), styles[style]))
            story.append(Spacer(1, 5))

    def walk(node: Tag) -> None:
        for child in node.children:
            if isinstance(child, NavigableString):
                paragraph(str(child))
                continue
            if not isinstance(child, Tag):
                continue
            if child.name == "img":
                p = html.parent / child["src"]
                if p.suffix == ".svg":
                    from svglib.svglib import svg2rlg

                    drawing = svg2rlg(str(p))
                    if drawing is None:
                        raise ValueError("Invalid SVG")
                    scale = min(480 / drawing.width, 660 / drawing.height, 1)
                    drawing.scale(scale, scale)
                    drawing.width *= scale
                    drawing.height *= scale
                    story.append(drawing)
                    continue
                img = Image(str(p))
                scale = min(480 / img.imageWidth, 660 / img.imageHeight, 1)
                img.drawWidth = img.imageWidth * scale
                img.drawHeight = img.imageHeight * scale
                story.append(KeepTogether([img, Spacer(1, 6)]))
            elif child.name == "table":
                rows = [
                    [Paragraph(escape(cell), styles["BodyText"]) for cell in row]
                    for row in table_grid(child)
                ]
                rows = [r for r in rows if r]
                if rows:
                    n = max(map(len, rows))
                    rows = [r + [""] * (n - len(r)) for r in rows]
                    table = Table(rows, colWidths=[480 / n] * n, repeatRows=1, splitInRow=1)
                    table.setStyle(
                        TableStyle(
                            [
                                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                                ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                            ]
                        )
                    )
                    story.extend([table, Spacer(1, 8)])
                    for cell in child.find_all(["td", "th"]):
                        if cell.find("img"):
                            walk(cell)
            elif child.name in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                paragraph(child.get_text(" ", strip=True), "Heading2")
            elif child.name == "pre":
                paragraph(child.get_text("", strip=False), code=True)
            elif child.name in {"p", "li", "blockquote"} and not child.find(
                ["img", "table", "ul", "ol"]
            ):
                paragraph(child.get_text(" ", strip=True))
            else:
                walk(child)

    soup = BeautifulSoup(html.read_text(), "html.parser")
    walk(soup.body)

    def footer(canvas, doc):
        canvas.setFont("Helvetica", 7)
        canvas.drawString(
            40,
            22,
            "WEB READING CONVERSION | locally generated | vendor source linked on first page",
        )
        canvas.drawRightString(550, 22, str(doc.page))

    SimpleDocTemplate(
        str(target),
        pagesize=(595, 842),
        leftMargin=50,
        rightMargin=50,
        topMargin=40,
        bottomMargin=40,
        invariant=1,
    ).build(story, onFirstPage=footer, onLaterPages=footer)
    validate(target.read_bytes(), "pdf")


def acquire(
    entry: dict, data: bytes, root: Path = ROOT, *, source_parts: dict[str, bytes] | None = None
) -> dict:
    validate(data, entry["format"])
    sha = digest(data)
    versions = entry.setdefault("versions", [])
    for version in versions:
        if version["sha256"] == sha:
            errors = verify_version(version, root)
            if errors:
                raise ValueError("Existing version is damaged: " + "; ".join(errors))
            return version
    relative = f".local/manuals/{entry['device']}/{entry['id']}/{sha[:16]}"
    destination = local_path(root, relative)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as scratch:
        stage = Path(scratch)
        original = stage / f"original.{entry['format']}"
        original.write_bytes(data)
        for name, payload in (source_parts or {}).items():
            if Path(name).name != name:
                raise ValueError("Source part must be a filename")
            (stage / name).write_bytes(payload)
        if entry["format"] == "html":
            html = stage / "reading.html"
            html.write_bytes(offline_html(data, entry["source"], stage, entry["title"]))
            reading_pdf(html, stage / "reading.pdf")
        files = {
            f"{relative}/{p.relative_to(stage)}": digest(p.read_bytes())
            for p in sorted(stage.rglob("*"))
            if p.is_file()
        }
        if destination.exists():
            raise ValueError("Unregistered destination exists; inspect before importing")
        stage.rename(destination)
    version = {
        "sha256": sha,
        "path": f"{relative}/original.{entry['format']}",
        "collected_at": datetime.now(UTC).isoformat(),
        "files": files,
    }
    if entry["format"] == "html":
        version["derived"] = [
            {
                "path": f"{relative}/reading.{fmt}",
                "format": fmt,
                "derived_from_sha256": sha,
                "conversion": "script-free HTML + ReportLab reflow",
            }
            for fmt in ["html", "pdf"]
        ]
    if source_parts and "source-bundle.js" in source_parts:
        version["extracted_from_sha256"] = digest(source_parts["source-bundle.js"])
    versions.append(version)
    entry["status"] = "acquired"
    return version


def verify_version(version: dict, root: Path = ROOT) -> list[str]:
    errors = []
    for relative, expected in version["files"].items():
        path = local_path(root, relative)
        if not path.is_file():
            errors.append(f"missing: {relative}")
            continue
        if digest(path.read_bytes()) != expected:
            errors.append(f"checksum: {relative}")
        try:
            if path.suffix == ".pdf":
                validate(path.read_bytes(), "pdf")
            if path.name == "reading.html":
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(path.read_text(), "html.parser")
                if soup.find(["script", "iframe", "link"]):
                    errors.append(f"active/external resource: {relative}")
                for img in soup.find_all("img"):
                    source = img.get("src", "")
                    resolved = (path.parent / source).resolve()
                    if (
                        urlparse(source).scheme
                        or not resolved.is_relative_to(path.parent)
                        or not resolved.is_file()
                    ):
                        errors.append(f"offline image: {relative}: {source}")
        except (ValueError, OSError) as exc:
            errors.append(f"format: {relative}: {exc}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["list", "import", "download", "verify"])
    parser.add_argument("id", nargs="?")
    parser.add_argument("--file", type=Path)
    args = parser.parse_args()
    catalog = json.loads(MANIFEST.read_text())
    entries = [e for e in catalog["documents"] if args.id is None or e["id"] == args.id]
    if not entries:
        parser.error("Unknown document ID")
    if args.command in {"import", "download"} and len(entries) != 1:
        parser.error("Select exactly one document ID")
    errors = []
    for entry in entries:
        if args.command == "list":
            print(f"{entry['id']}: {entry['status']} ({len(entry.get('versions', []))} versions)")
        elif args.command == "verify":
            if not entry.get("versions"):
                print(f"UNAVAILABLE {entry['id']}: {entry.get('acquisition', entry['source'])}")
            for version in entry.get("versions", []):
                errors.extend(verify_version(version))
        else:
            if args.command == "import" and args.file is None:
                parser.error("import requires --file")
            if args.command == "import":
                data, parts = args.file.read_bytes(), {}
            else:
                data, parts = fetch_document(entry)
            result = acquire(entry, data, source_parts=parts)
            MANIFEST.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n")
            print(result["path"])
    for error in errors:
        print(error)
    if args.command == "verify":
        print(
            f"Verified {sum(len(e.get('versions', [])) for e in entries)} acquired versions; {len(errors)} errors"
        )
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
