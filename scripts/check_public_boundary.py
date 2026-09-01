from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "START_HERE.md",
    Path(__file__).resolve(),
}
BLOCKED = re.compile(r"friday|flexiv|cosmax|pai_private_lab|tutorial-robotics-private", re.IGNORECASE)


def main() -> int:
    failures: list[str] = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if (
            not path.is_file()
            or path in ALLOWED
            or any(part in {".git", ".venv", "deps", "assets"} for part in relative.parts)
        ):
            continue
        if path.suffix.lower() not in {".md", ".py", ".toml", ".yaml", ".yml", ".json", ".txt"}:
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
            if BLOCKED.search(line):
                failures.append(f"{path.relative_to(ROOT)}:{line_number}")
    if failures:
        print("private-boundary violations:")
        print("\n".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
