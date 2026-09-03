from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TUTORIALS = ROOT / "tutorials"


def field(text: str, name: str) -> str:
    match = re.search(rf"^{re.escape(name)}:\s*[\"']?([^\n\"']*)", text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def list_field(text: str, name: str) -> str:
    return field(text, name).strip("[]")


def sort_key(row: tuple[str, ...]) -> tuple[int, str]:
    match = re.match(r"T(\d+)(.*)", row[0])
    return (int(match.group(1)), match.group(2)) if match else (9999, row[0])


existing_status: dict[str, tuple[str, str]] = {}
progress_path = ROOT / "state" / "PROGRESS.md"
if progress_path.exists():
    for line in progress_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*(T\w+)\s*\|.*?\|\s*([^| ]+)\s*\|\s*([^|]*)\|", line)
        if match:
            existing_status[match.group(1)] = (match.group(2), match.group(3).strip())

rows: list[tuple[str, str, str, str, str, str, Path]] = []
for path in sorted(TUTORIALS.glob("*/*.md")):
    text = path.read_text(encoding="utf-8")
    tutorial_id = field(text, "id")
    if not tutorial_id:
        continue
    rows.append(
        (
            tutorial_id,
            path.parent.name,
            field(text, "title"),
            list_field(text, "prerequisites"),
            field(text, "mode") or "development",
            list_field(text, "requires"),
            path,
        )
    )
rows.sort(key=sort_key)

index = [
    "# Public Tutorial Index",
    "",
    "This registry is closed over public tutorials: every prerequisite is available in this repository.",
    "",
    "| ID | Robot/group | Mode | Requires | Title | Prerequisites |",
    "|---|---|---|---|---|---|",
]
for tutorial_id, robot, title, prerequisites, mode, requires, path in rows:
    link = path.relative_to(TUTORIALS).as_posix()
    index.append(
        f"| [{tutorial_id}]({link}) | `{robot}` | `{mode}` | "
        f"{requires or '—'} | {title} | {prerequisites or '—'} |"
    )
(TUTORIALS / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")

progress = [
    "# Tutorial Progress",
    "",
    "Shared public completion state. Machine-local readiness belongs in `.local/`.",
    "",
    "| ID | Robot/group | Status | Evidence/notes |",
    "|---|---|---|---|",
]
for tutorial_id, robot, _title, _prerequisites, _mode, _requires, _path in rows:
    status, note = existing_status.get(tutorial_id, ("pending", "—"))
    progress.append(f"| {tutorial_id} | `{robot}` | {status} | {note or '—'} |")
(ROOT / "state" / "PROGRESS.md").write_text("\n".join(progress) + "\n", encoding="utf-8")

with (ROOT / "migration" / "tutorial-id-map.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(("legacy_id", "public_path"))
    for tutorial_id, _robot, _title, _prerequisites, _mode, _requires, path in rows:
        writer.writerow((tutorial_id, path.relative_to(ROOT).as_posix()))
