"""Open a Chrome lesson using the live tab language, then saved/conversation language."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS_URL = "https://github.com/terryum/tutorial-robotics/blob/main/docs/"


def open_lesson(
    lesson: str, language: str, state_file: Path, *, force_language: bool = False
) -> dict:
    if language not in {"ko", "en"}:
        raise ValueError("Language must be ko or en")
    catalog = json.loads((ROOT / "curriculum/catalog.json").read_text())["lessons"]
    if lesson not in {item["id"] for item in catalog}:
        raise ValueError("Use a canonical lesson ID from the catalog")
    try:
        state = json.loads(state_file.read_text())
    except (OSError, ValueError):
        state = {}
    if not isinstance(state, dict) or state.get("browser") != "chrome":
        state = {}
    fresh_session = state.get("language") not in {"ko", "en"}
    fallback = language
    if not force_language and state.get("language") in {"ko", "en"}:
        fallback = state["language"]
    tab_id = state.get("tab_id")
    preferred_tab = str(tab_id) if type(tab_id) is int and tab_id > 0 else ""
    result = subprocess.run(
        [
            "osascript",
            str(ROOT / "scripts/open-lesson-chrome.applescript"),
            fallback,
            lesson,
            preferred_tab,
            "force" if force_language or fresh_session else "preserve",
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    receipt = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    selected_language = receipt.get("language")
    if selected_language not in {"ko", "en"}:
        raise ValueError("Browser did not report a supported language")
    expected_url = f"{DOCS_URL}{selected_language}/lessons/{lesson}.md"
    if receipt.get("url") != expected_url or f"{lesson}.md" not in receipt.get("title", ""):
        raise ValueError("Browser did not verify the requested lesson")
    actual_tab = int(receipt["tab_id"])
    if actual_tab <= 0:
        raise ValueError("Browser returned an invalid tab ID")
    saved = {
        "browser": "chrome",
        "tab_id": actual_tab,
        "lesson": lesson,
        "language": selected_language,
        "url": expected_url,
    }
    state_file.parent.mkdir(parents=True, exist_ok=True)
    temporary = state_file.with_name(f".{state_file.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(saved, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(state_file)
    return {**saved, "reused": receipt.get("reused") == "true", "title": receipt["title"]}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lesson", help="Canonical lesson ID, e.g. core-00")
    parser.add_argument(
        "--language",
        choices=("ko", "en"),
        required=True,
        help="Conversation language used for a fresh session",
    )
    parser.add_argument(
        "--force-language",
        action="store_true",
        help="Only for an explicit language change requested in chat",
    )
    parser.add_argument(
        "--state-file",
        type=Path,
        default=Path(os.environ.get("PAL_LOCAL_DIR", ROOT / ".local")) / "browser.json",
    )
    args = parser.parse_args()
    print(
        json.dumps(
            open_lesson(
                args.lesson, args.language, args.state_file, force_language=args.force_language
            ),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
