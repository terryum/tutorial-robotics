"""Open the saved verified lesson result in its own Chrome window on macOS."""

from __future__ import annotations

import json
import subprocess

from pai_lab.catalog import ROOT
from pai_lab.local import local_root, write_json
from pai_lab.session import resume


def main() -> None:
    state = resume()
    if not state["resume_available"] or state["resume_phase"] != "awaiting_comprehension":
        raise SystemExit("No verified results are awaiting a comprehension answer.")
    results = state["saved_state"]["presentation"]
    receipt = local_root() / "results-window.json"
    try:
        prior = json.loads(receipt.read_text())
    except (OSError, ValueError):
        prior = {}
    if not isinstance(prior, dict) or prior.get("browser") != "chrome":
        prior = {}
    process = subprocess.run(
        [
            "osascript",
            str(ROOT / "scripts/open-results-chrome.applescript"),
            results["page_url"],
            results["title"],
            str(prior.get("window_id", "")),
            prior.get("url", ""),
        ],
        capture_output=True,
        check=False,
        text=True,
        timeout=30,
    )
    if process.returncode:
        raise SystemExit(process.stderr.strip())
    window = {
        "browser": "chrome",
        "window_id": int(process.stdout),
        "url": results["page_url"],
        "title": results["title"],
    }
    write_json(receipt, window)
    print(json.dumps(window, ensure_ascii=False))


if __name__ == "__main__":
    main()
