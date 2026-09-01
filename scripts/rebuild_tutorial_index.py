from __future__ import annotations

from pathlib import Path
import csv
import re


ROOT = Path(__file__).resolve().parents[1]
TUTORIALS = ROOT / "tutorials"


def field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*[\"']?([^\n\"']*)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


rows: list[tuple[str, str, str, str, Path]] = []
for path in sorted(TUTORIALS.glob("*/*.md")):
    text = path.read_text(encoding="utf-8")
    tutorial_id = field(text, "id")
    if not tutorial_id:
        continue
    rows.append((tutorial_id, path.parent.name, field(text, "title"), field(text, "prerequisites"), path))

index = [
    "# Public Tutorial Index",
    "",
    "This registry is closed over public tutorials: every prerequisite is available in this repository.",
    "",
    "| ID | Robot/group | Title | Prerequisites |",
    "|---|---|---|---|",
]
for tutorial_id, robot, title, prerequisites, path in rows:
    link = path.relative_to(TUTORIALS).as_posix()
    index.append(f"| [{tutorial_id}]({link}) | `{robot}` | {title} | {prerequisites or '—'} |")
(TUTORIALS / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")

progress = [
    "# Tutorial Progress",
    "",
    "Shared public completion state. Machine-local readiness belongs in `.local/`.",
    "",
    "| ID | Robot/group | Status | Evidence/notes |",
    "|---|---|---|---|",
]
for tutorial_id, robot, _title, _prerequisites, _path in rows:
    progress.append(f"| {tutorial_id} | `{robot}` | pending | — |")
(ROOT / "state" / "PROGRESS.md").write_text("\n".join(progress) + "\n", encoding="utf-8")

with (ROOT / "migration" / "tutorial-id-map.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle)
    writer.writerow(("legacy_id", "public_path"))
    for tutorial_id, _robot, _title, _prerequisites, path in rows:
        writer.writerow((tutorial_id, path.relative_to(ROOT).as_posix()))

