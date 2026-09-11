"""Manifest-based, on-demand public asset cache."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT

MANIFEST = ROOT / "assets" / "sources.json"
CACHE = ROOT / ".cache" / "assets"


def bundles() -> dict[str, dict[str, Any]]:
    raw = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return dict(raw["bundles"])


def fetch_bundle(name: str, cache: Path = CACHE) -> dict[str, str]:
    """Fetch a pinned Git source without modifying its checkout."""

    try:
        bundle = bundles()[name]
    except KeyError as error:
        raise ValueError(f"unknown asset bundle: {name}") from error
    if bundle["kind"] == "manual":
        raise RuntimeError(
            f"manual download required; redistribution is not established: {bundle['url']}"
        )
    destination = cache / str(bundle["destination"])
    revision = str(bundle["revision"])
    cache.mkdir(parents=True, exist_ok=True)
    if (destination / ".git").is_dir():
        dirty = subprocess.run(
            ["git", "-C", str(destination), "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        if dirty:
            raise RuntimeError("vendor cache contains changes; preserve it and use a fresh cache")
    if not (destination / ".git").is_dir():
        subprocess.run(
            [
                "git",
                "clone",
                "--filter=blob:none",
                "--no-checkout",
                str(bundle["url"]),
                str(destination),
            ],
            check=True,
        )
    if bundle.get("sparse_paths"):
        subprocess.run(
            ["git", "-C", str(destination), "sparse-checkout", "set", *bundle["sparse_paths"]],
            check=True,
        )
    subprocess.run(["git", "-C", str(destination), "fetch", "origin", revision], check=True)
    subprocess.run(["git", "-C", str(destination), "checkout", "--detach", revision], check=True)
    actual = subprocess.run(
        ["git", "-C", str(destination), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if len(revision) == 40 and actual != revision:
        raise RuntimeError(f"asset revision mismatch: expected {revision}, got {actual}")
    receipt = {
        "name": name,
        "path": str(destination),
        "revision": actual,
        "license": str(bundle["license"]),
    }
    (cache / f"{name}-receipt.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return receipt


def check_sources() -> list[str]:
    errors: list[str] = []
    for name, bundle in bundles().items():
        for field in ("kind", "url", "revision", "release", "license", "destination"):
            if not bundle.get(field):
                errors.append(f"{name}: missing {field}")
        revision = str(bundle.get("revision", ""))
        if bundle.get("kind") == "git" and revision in {"main", "master", "latest"}:
            errors.append(f"{name}: mutable revision {revision}")
    return errors
