"""Profile-scoped setup planning and read-only verification."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Literal, cast

from pai_lab.bundle import validate_bundle
from pai_lab.catalog import ROOT, Stage
from pai_lab.host import detect_host

SetupProfile = Literal["core", "ros", "gpu", "isaac", "runtime-offline", "hardware"]
SETUP_PROFILES: tuple[SetupProfile, ...] = (
    "core",
    "ros",
    "gpu",
    "isaac",
    "runtime-offline",
    "hardware",
)
STAGE_PROFILE: dict[Stage, SetupProfile] = {"core": "core", "sim": "ros", "hardware": "hardware"}

PROFILE_REQUIREMENTS: dict[SetupProfile, tuple[str, ...]] = {
    "core": ("python-3.12", "numpy", "mujoco"),
    "ros": ("ubuntu-24.04-x86_64", "ros2-jazzy", "ros2-rmw"),
    "gpu": ("ubuntu-24.04-x86_64", "nvidia-cuda"),
    "isaac": ("ubuntu-24.04-x86_64", "nvidia-cuda", "isaac-sim"),
    "runtime-offline": ("python-3.12",),
    "hardware": ("robot-runtime", "isolated-network"),
}


@dataclass(frozen=True)
class SetupPlan:
    schema_version: int
    profile: SetupProfile
    stage: Stage | None
    robots: tuple[str, ...]
    platform: str
    required_capabilities: tuple[str, ...]
    python_extras: tuple[str, ...]
    manual_requirements: tuple[str, ...]
    prohibited_automation: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def normalize_profile(profile: str | None, stage: Stage | None) -> SetupProfile:
    if profile and stage:
        raise ValueError("choose --profile or legacy --stage, not both")
    if stage:
        return STAGE_PROFILE[stage]
    if profile in SETUP_PROFILES:
        return cast(SetupProfile, profile)
    raise ValueError("a setup profile is required")


def create_plan(
    profile: SetupProfile,
    robots: tuple[str, ...] = (),
    *,
    legacy_stage: Stage | None = None,
) -> SetupPlan:
    host = detect_host()
    extras: tuple[str, ...] = ()
    manual: list[str] = []
    if profile == "ros":
        extras = ("ros",)
        manual.extend(("Ubuntu 24.04", "ROS 2 Jazzy and one explicit RMW implementation"))
    elif profile == "gpu":
        manual.append("NVIDIA driver/CUDA with a successful framework tensor operation")
    elif profile == "isaac":
        manual.extend(("verified GPU profile", "Isaac Sim installation and EULA acceptance"))
    elif profile == "hardware":
        extras = ("hardware",)
        manual.extend(("isolated robot network", "vendor SDK", "physical E-stop check"))
    elif profile == "runtime-offline":
        manual.append("candidate bundle copied from a development host")
    return SetupPlan(
        schema_version=2,
        profile=profile,
        stage=legacy_stage,
        robots=robots,
        platform=host.platform_id,
        required_capabilities=PROFILE_REQUIREMENTS[profile],
        python_extras=extras,
        manual_requirements=tuple(manual),
        prohibited_automation=(
            "sudo",
            "GPU driver",
            "CUDA",
            "ROS distribution",
            "Isaac Sim",
            "firmware",
            "large models",
        ),
    )


def write_plan(plan: SetupPlan, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(plan.to_dict(), indent=2, sort_keys=True) + "\n", encoding="utf-8")


def apply_plan(path: Path) -> int:
    """Install only declared Python extras into an active project virtualenv."""

    raw = json.loads(path.read_text(encoding="utf-8"))
    if raw.get("schema_version") not in {1, 2}:
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


def _verify_runtime_offline() -> tuple[bool, dict[str, object]]:
    manifest = ROOT / "examples/sim-deploy-01/sample_candidate/manifest.json"
    errors = validate_bundle(manifest)
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest() if manifest.is_file() else ""
    evidence = {
        "bundle_manifest": str(manifest.relative_to(ROOT)),
        "bundle_manifest_sha256": digest,
        "deterministic_vector": not errors,
        "rollback_declared": False,
        "command_publishers": 0,
        "errors": errors,
    }
    if manifest.is_file():
        raw = json.loads(manifest.read_text(encoding="utf-8"))
        evidence["rollback_declared"] = bool(raw.get("rollback"))
    return not errors and bool(evidence["rollback_declared"]), evidence


def verify_setup(profile: SetupProfile, robots: tuple[str, ...] = ()) -> dict[str, object]:
    host = detect_host()
    if profile == "runtime-offline":
        ready, evidence = _verify_runtime_offline()
        return {
            "profile": profile,
            "robots": robots,
            "ready": ready,
            "missing_capabilities": [] if ready else ["validated-candidate-bundle"],
            "evidence": evidence,
            "host": host.to_dict(),
        }
    states = host.capability_status
    required = PROFILE_REQUIREMENTS[profile]
    missing = [item for item in required if item not in states or states[item].state != "available"]
    return {
        "profile": profile,
        "robots": robots,
        "ready": not missing,
        "missing_capabilities": missing,
        "capability_status": {
            item: asdict(states[item]) if item in states else {"state": "unverified", "evidence": "requires an approved verification receipt"}
            for item in required
        },
        "host": host.to_dict(),
    }
