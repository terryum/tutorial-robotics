"""Auditable setup planning with deliberately narrow apply behavior."""

from __future__ import annotations

import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

from pai_lab.catalog import ROOT, Stage
from pai_lab.host import detect_host


@dataclass(frozen=True)
class SetupPlan:
    schema_version: int
    stage: Stage
    robots: tuple[str, ...]
    platform: str
    python_extras: tuple[str, ...]
    manual_requirements: tuple[str, ...]
    prohibited_automation: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def create_plan(stage: Stage, robots: tuple[str, ...]) -> SetupPlan:
    profile = detect_host()
    extras: list[str] = []
    manual: list[str] = []
    if stage in {"sim", "hardware"}:
        extras.append("ros")
        manual.extend(("Ubuntu 24.04", "ROS 2 Jazzy"))
    if stage == "sim":
        manual.extend(("NVIDIA driver/CUDA for GPU lessons", "Isaac Sim for Isaac lessons"))
    if stage == "hardware":
        extras.append("hardware")
        manual.extend(("isolated robot network", "vendor SDK", "physical E-stop check"))
    return SetupPlan(
        schema_version=1,
        stage=stage,
        robots=robots,
        platform=profile.platform_id,
        python_extras=tuple(extras),
        manual_requirements=tuple(manual),
        prohibited_automation=("sudo", "GPU driver", "CUDA", "ROS distribution", "Isaac Sim", "firmware", "large models"),
    )


def write_plan(plan: SetupPlan, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_plan(path: Path) -> int:
    """Install only declared Python extras into an active project virtualenv."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1:
        raise ValueError("unsupported setup plan schema")
    if sys.prefix == sys.base_prefix:
        raise RuntimeError("activate the project virtual environment before setup apply")
    extras = tuple(str(item) for item in raw.get("python_extras", []))
    target = ".[" + ",".join(extras) + "]" if extras else "."
    return subprocess.run(
        [sys.executable, "-m", "pip", "install", "--editable", target],
        check=False,
        cwd=ROOT,
    ).returncode


def verify_setup(stage: Stage, robots: tuple[str, ...]) -> dict[str, object]:
    profile = detect_host()
    required = {"python-3.12"}
    if stage in {"sim", "hardware"}:
        required.add("ros2-jazzy")
    if stage == "hardware":
        required.update(("robot-runtime", "isolated-network"))
    missing = sorted(required - set(profile.capabilities))
    return {
        "stage": stage,
        "robots": robots,
        "ready": not missing,
        "missing_capabilities": missing,
        "host": profile.to_dict(),
    }
