"""Wuji Hand 2 plugin metadata."""

from __future__ import annotations


def plugin() -> dict[str, str]:
    return {"name": "wuji", "access": "public", "mode": "read-only-first"}
