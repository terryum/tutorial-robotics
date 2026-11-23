"""Verify the imported Harness and redistribution notices without a source checkout."""

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    manifest = json.loads((ROOT / "third_party/codex-harness/manifest.json").read_text())
    failures = []
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != entry["sha256"]:
            failures.append(entry["path"])
    if failures:
        print(
            "Harness import drift; review provenance and required change notices: "
            + ", ".join(failures)
        )
        return 1
    print(f"passed: {len(manifest['files'])} pinned Harness files and license/NOTICE hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
