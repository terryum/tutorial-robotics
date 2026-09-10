"""Public Flexiv Enlight plugin metadata."""

from __future__ import annotations


def plugin() -> dict[str, str]:
    return {"name": "enlight", "access": "public", "mode": "read-only-first"}
