"""Keep GitHub-relative source links valid when the same Markdown becomes a site."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path
from urllib.parse import quote, unquote

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"(?P<opening>!?\[[^\]]*\]\()(?P<href>[^)\s]+)(?P<closing>\))")


def render_source_links(markdown: str, source: Path, root: Path = ROOT) -> str:
    def replace(match: re.Match[str]) -> str:
        href = match["href"]
        if href.startswith(("#", "http:", "https:", "mailto:")):
            return match[0]
        path, separator, anchor = href.partition("#")
        target = (source.parent / unquote(path)).resolve()
        if not target.is_file() or not target.is_relative_to(root):
            return match[0]
        if target.is_relative_to(root / "docs"):
            return match[0]
        url = "https://github.com/terryum/tutorial-robotics/blob/main/" + quote(
            target.relative_to(root).as_posix(), safe="/"
        )
        return match["opening"] + url + (separator + anchor if separator else "") + match["closing"]

    return LINK.sub(replace, markdown)


def on_page_markdown(markdown, page, **kwargs):
    source = Path(page.file.abs_src_path)
    return render_language_links(render_source_links(markdown, source), source)


def render_language_links(markdown: str, source: Path, root: Path = ROOT) -> str:
    """Raw HTML anchors bypass MkDocs' Markdown-link conversion."""

    def url(path: Path) -> str:
        relative = path.relative_to(root / "docs")
        return (
            relative.parent if relative.name == "index.md" else relative.with_suffix("")
        ).as_posix()

    def replace(match: re.Match[str]) -> str:
        target = (source.parent / match["href"]).resolve()
        if not target.is_file() or not target.is_relative_to(root / "docs"):
            return match[0]
        href = posixpath.relpath(url(target), url(source)).rstrip("/") + "/"
        return match["opening"] + href + match["closing"]

    return re.sub(
        r'(?P<opening><a\s+href=")(?P<href>[^"]+)(?P<closing>"\s+lang="(?:en|ko)">)',
        replace,
        markdown,
    )
