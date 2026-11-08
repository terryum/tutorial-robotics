"""Verify complete downloaded manufacturer USD assets, rejecting Git LFS pointer stubs."""

import hashlib
import json
from pathlib import Path

from pai_lab.catalog import ROOT


def verified_asset(name: str, cache: Path | None = None) -> Path:
    entry = json.loads((ROOT / "assets/isaac-assets.json").read_text())["assets"][name]
    base = cache or ROOT / ".cache/assets" / entry["bundle"]
    for relative, expected in entry["files"].items():
        path = base / relative
        if not path.is_file():
            raise FileNotFoundError(
                f"missing Isaac asset: {relative}; fetch {entry['bundle']} with Git LFS"
            )
        data = path.read_bytes()
        if data.startswith(b"version https://git-lfs.github.com/spec/v1"):
            raise ValueError("Git LFS pointer is not a usable Isaac asset")
        if hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise ValueError(f"Isaac asset checksum mismatch: {relative}")
    return base / str(entry["root"])
