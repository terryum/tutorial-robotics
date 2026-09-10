"""Read-only host and capability detection."""

from __future__ import annotations

import importlib.util
import json
import platform
import shutil
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class HostProfile:
    """Non-secret facts used to select lessons."""

    system: str
    machine: str
    python: str
    platform_id: str
    capabilities: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _has_module(name: str) -> bool:
    return importlib.util.find_spec(name) is not None


def detect_host() -> HostProfile:
    """Detect only local, read-only properties; never probe a robot network."""

    system = platform.system()
    machine = platform.machine().lower()
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    capabilities = {"python"}
    if sys.version_info[:2] == (3, 12):
        capabilities.add("python-3.12")
    if _has_module("numpy"):
        capabilities.add("numpy")
    if _has_module("mujoco"):
        capabilities.add("mujoco")
    if _has_module("torch"):
        capabilities.add("small-ml")
    if system == "Darwin" and machine in {"arm64", "aarch64"}:
        platform_id = "macos-arm64"
    elif system == "Linux" and machine in {"x86_64", "amd64"}:
        platform_id = "ubuntu-24.04-x86_64"
        capabilities.add("linux-x86_64")
    elif system == "Linux":
        platform_id = f"linux-{machine}"
    else:
        platform_id = f"{system.lower()}-{machine}"
    if shutil.which("ros2"):
        capabilities.add("ros2-jazzy")
    if shutil.which("nvidia-smi"):
        capabilities.add("nvidia-cuda")
    return HostProfile(
        system=system,
        machine=machine,
        python=version,
        platform_id=platform_id,
        capabilities=tuple(sorted(capabilities)),
    )


def write_profile(path: Path) -> HostProfile:
    profile = detect_host()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return profile
