"""Optional public plugin discovery.

No particular plugin is required. An empty plugin set is a valid installation.
"""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import Any


def discover_robot_plugins() -> dict[str, Any]:
    return {entry.name: entry.load() for entry in entry_points(group="pai_lab.robot_plugins")}

