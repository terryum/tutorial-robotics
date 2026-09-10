"""Read-only host and capability detection with explicit evidence states."""

from __future__ import annotations

import importlib
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal

CapabilityState = Literal["available", "unavailable", "unverified"]


@dataclass(frozen=True)
class CapabilityEvidence:
    """Why a capability received its state."""

    state: CapabilityState
    evidence: str


@dataclass(frozen=True)
class HostProfile:
    """Non-secret facts used to select lessons."""

    system: str
    machine: str
    python: str
    platform_id: str
    capabilities: tuple[str, ...]
    capability_status: dict[str, CapabilityEvidence]
    os_release: dict[str, str]

    def to_dict(self) -> dict[str, object]:
        result = asdict(self)
        result["capability_status"] = {
            key: asdict(value) for key, value in self.capability_status.items()
        }
        return result


def _has_module(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ModuleNotFoundError):
        return False


def _os_release(path: Path = Path("/etc/os-release")) -> dict[str, str]:
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" not in line or line.startswith("#"):
            continue
        key, value = line.split("=", 1)
        values[key] = value.strip().strip('"')
    return values


def _command_ok(command: list[str], timeout: float = 5.0) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return False, type(error).__name__
    output = (result.stdout or result.stderr).strip().splitlines()
    return result.returncode == 0, output[0][:160] if output else f"exit={result.returncode}"


def _cuda_compute() -> tuple[CapabilityState, str]:
    if not shutil.which("nvidia-smi"):
        return "unavailable", "nvidia-smi not found"
    driver_ok, driver = _command_ok(
        ["nvidia-smi", "--query-gpu=name,driver_version", "--format=csv,noheader"]
    )
    if not driver_ok:
        return "unverified", f"driver probe failed: {driver}"
    if not _has_module("torch"):
        return "unverified", f"GPU visible ({driver}); torch compute probe unavailable"
    try:
        torch = importlib.import_module("torch")

        if not torch.cuda.is_available():
            return "unverified", f"GPU visible ({driver}); torch reports CUDA unavailable"
        value = float((torch.ones(4, device="cuda") * 2).sum().cpu())
        if value != 8.0:
            return "unverified", "CUDA arithmetic returned an unexpected value"
    except (RuntimeError, AssertionError, OSError) as error:
        return "unverified", f"CUDA arithmetic failed: {type(error).__name__}"
    return "available", f"torch CUDA arithmetic passed; {driver}"


def detect_host() -> HostProfile:
    """Detect local properties without inferring capabilities from executable names alone."""

    system = platform.system()
    machine = platform.machine().lower()
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    release = _os_release() if system == "Linux" else {}
    status: dict[str, CapabilityEvidence] = {}

    def record(name: str, state: CapabilityState, evidence: str) -> None:
        status[name] = CapabilityEvidence(state, evidence)

    record("python", "available", sys.executable)
    record("python-3.12", "available" if sys.version_info[:2] == (3, 12) else "unavailable", version)
    for module in ("numpy", "mujoco"):
        found = _has_module(module)
        record(module, "available" if found else "unavailable", f"import {module}")
    record("small-ml", "available" if _has_module("torch") else "unavailable", "import torch")

    if system == "Darwin" and machine in {"arm64", "aarch64"}:
        platform_id = "macos-arm64"
        record("macos-arm64", "available", platform.platform())
    elif system == "Linux" and machine in {"x86_64", "amd64"}:
        platform_id = f"linux-{machine}"
        record("linux-x86_64", "available", platform.machine())
        if release.get("ID") == "ubuntu" and release.get("VERSION_ID") == "24.04":
            platform_id = "ubuntu-24.04-x86_64"
            record("ubuntu-24.04-x86_64", "available", release.get("PRETTY_NAME", "Ubuntu 24.04"))
        else:
            record("ubuntu-24.04-x86_64", "unavailable", f"ID={release.get('ID', 'unknown')} VERSION_ID={release.get('VERSION_ID', 'unknown')}")
    elif system == "Linux":
        platform_id = f"linux-{machine}"
    else:
        platform_id = f"{system.lower()}-{machine}"

    ros_executable = shutil.which("ros2")
    ros_distro = os.environ.get("ROS_DISTRO", "")
    if ros_executable and ros_distro == "jazzy":
        record("ros2-jazzy", "available", f"ROS_DISTRO=jazzy; {ros_executable}")
    elif ros_executable:
        record("ros2-jazzy", "unverified", f"ros2 found but ROS_DISTRO={ros_distro or 'unset'}")
    else:
        record("ros2-jazzy", "unavailable", "ros2 not found")
    rmw = os.environ.get("RMW_IMPLEMENTATION", "")
    if ros_executable and ros_distro == "jazzy" and rmw:
        record("ros2-rmw", "available", rmw)
    elif ros_executable and ros_distro == "jazzy":
        record("ros2-rmw", "unverified", "RMW_IMPLEMENTATION is unset")
    else:
        record("ros2-rmw", "unavailable", "ROS 2 Jazzy is unavailable")

    cuda_state, cuda_evidence = _cuda_compute()
    record("nvidia-cuda", cuda_state, cuda_evidence)
    isaac_module = _has_module("isaacsim") or _has_module("omni.isaac.core")
    isaac_root = os.environ.get("ISAAC_SIM_PATH")
    if isaac_module:
        record("isaac-sim", "available", "Isaac Python module importable")
    elif isaac_root and Path(isaac_root).is_dir():
        record("isaac-sim", "unverified", "ISAAC_SIM_PATH exists; launch not verified")
    else:
        record("isaac-sim", "unavailable", "Isaac module/path not found")

    available = tuple(sorted(key for key, value in status.items() if value.state == "available"))
    return HostProfile(system, machine, version, platform_id, available, status, release)


def write_profile(path: Path) -> HostProfile:
    profile = detect_host()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(profile.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return profile
