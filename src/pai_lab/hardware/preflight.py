"""Sanitized, read-only preflight checks for supported public robots."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

from pai_lab.catalog import ROOT

SUPPORTED = ("fr3", "wuji", "enlight")
WUJI_RELEASE = ROOT / "assets" / "wuji-hand2-beta2-release.json"
EXPECTED_MODELS = {
    "fr3": {"franka-fr3", "fr3"},
    "wuji": {"wujihand2-beta2-left", "wujihand2-beta2-right"},
    "enlight": {"flexiv-enlight-l", "flexiv-enlight-ll"},
}


def _check_wuji(snapshot: dict[str, Any]) -> list[str]:
    release = json.loads(WUJI_RELEASE.read_text(encoding="utf-8"))
    errors: list[str] = []
    if snapshot.get("model") not in {"wujihand2-beta2-left", "wujihand2-beta2-right"}:
        errors.append("wrong-model: expected Wuji Hand 2 Beta 2")
    voltage = float(snapshot.get("voltage_v", 0.0))
    limits = release["power_voltage_v"]
    if not limits["minimum"] <= voltage <= limits["maximum"]:
        errors.append("power-out-of-range")
    if snapshot.get("firmware") != release["firmware"]:
        errors.append("firmware-mismatch")
    if snapshot.get("sdk") != release["sdk"]:
        errors.append("sdk-mismatch")
    if float(snapshot.get("get_rate_hz", 0.0)) > release["read_rate_hz_maximum"]:
        errors.append("get-rate-limit")
    if float(snapshot.get("publish_rate_hz", 0.0)) > release["publish_rate_hz_maximum"]:
        errors.append("publish-rate-limit")
    return errors


def preflight(robot: str, snapshot_path: Path, *, read_only: bool) -> dict[str, object]:
    """Evaluate an externally captured snapshot; never open a command channel."""

    if not read_only:
        raise PermissionError("hardware preflight must be explicitly read-only")
    if robot not in SUPPORTED:
        raise ValueError(f"unsupported robot: {robot}")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if snapshot.get("model") not in EXPECTED_MODELS[robot]:
        errors.append(f"wrong-model: expected {robot}")
    if not snapshot.get("network_ok"):
        errors.append("disconnected-device")
    if snapshot.get("enabled"):
        errors.append("device-must-be-disabled")
    if snapshot.get("error"):
        errors.append("device-error")
    if not snapshot.get("estop_ready"):
        errors.append("estop-not-ready")
    age = time.time() - float(snapshot.get("timestamp", 0.0))
    if age > float(snapshot.get("stale_after_s", 1.0)):
        errors.append("stale-state")
    if int(snapshot.get("command_authority_count", 0)) != 0:
        errors.append("command-authority-active")
    positions = [float(item) for item in snapshot.get("positions_rad", [])]
    limits = snapshot.get("position_limits_rad", [])
    if len(positions) != len(limits) or any(
        not float(limit[0]) <= position <= float(limit[1])
        for position, limit in zip(positions, limits, strict=True)
    ):
        errors.append("limit-violation")
    if robot == "wuji":
        errors.extend(
            error
            for error in _check_wuji(snapshot)
            if error != "wrong-model: expected Wuji Hand 2 Beta 2"
        )
    return {
        "robot": robot,
        "ready": not errors,
        "read_only": True,
        "errors": errors,
        "model": snapshot.get("model", "unknown"),
        "firmware": snapshot.get("firmware", "unknown"),
        "sdk": snapshot.get("sdk", "unknown"),
        "serial_stored": False,
    }
