"""Sanitized, read-only preflight checks for supported public robots."""

from __future__ import annotations

import json
import math
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
    read_rate = float(snapshot.get("get_rate_hz", 0.0))
    if not math.isfinite(read_rate) or not 0 <= read_rate <= release["read_rate_hz_maximum"]:
        errors.append("get-rate-limit")
    publish_rate = float(snapshot.get("publish_rate_hz", 0.0))
    if (
        not math.isfinite(publish_rate)
        or not 0 <= publish_rate <= release["publish_rate_hz_maximum"]
    ):
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
    if snapshot.get("network_ok") is not True:
        errors.append("disconnected-device")
    if snapshot.get("enabled") is not False:
        errors.append("device-must-be-disabled")
    if snapshot.get("error") is not False:
        errors.append("device-error")
    if snapshot.get("estop_ready") is not True:
        errors.append("estop-not-ready")
    try:
        timestamp = float(snapshot.get("timestamp", 0))
        stale_after = float(snapshot.get("stale_after_s", 0))
        age = time.time() - timestamp
        if (
            not math.isfinite(timestamp)
            or not math.isfinite(stale_after)
            or not 0 < stale_after <= 1
            or not 0 <= age <= stale_after
        ):
            errors.append("stale-state")
        previous = snapshot.get("previous_timestamp")
        if previous is not None and not timestamp > float(previous):
            errors.append("stalled-state")
        if snapshot.get("command_authority_count") != 0:
            errors.append("command-authority-active")
        positions = [float(item) for item in snapshot.get("positions_rad", [])]
        limits = snapshot.get("position_limits_rad", [])
        if (
            not positions
            or len(positions) != len(limits)
            or any(
                len(limit) != 2
                or not all(math.isfinite(float(v)) for v in limit)
                or not math.isfinite(position)
                or not float(limit[0]) < float(limit[1])
                or not float(limit[0]) <= position <= float(limit[1])
                for position, limit in zip(positions, limits, strict=True)
            )
        ):
            errors.append("limit-violation")
        if robot in {"fr3", "enlight"} and (
            len(positions) != 7 or snapshot.get("joint_group") != "arm"
        ):
            errors.append("invalid-joint-group")
    except (TypeError, ValueError, OverflowError):
        errors.append("malformed-state")
    if robot == "wuji":
        try:
            wuji_errors = _check_wuji(snapshot)
        except (TypeError, ValueError, OverflowError):
            wuji_errors = ["malformed-state"]
        errors.extend(
            error for error in wuji_errors if error != "wrong-model: expected Wuji Hand 2 Beta 2"
        )
    return {
        "valid_until_s": timestamp + stale_after if not errors else 0.0,
        "robot": robot,
        "ready": not errors,
        "read_only": True,
        "errors": errors,
        "model": snapshot.get("model", "unknown"),
        "firmware": snapshot.get("firmware", "unknown"),
        "sdk": snapshot.get("sdk", "unknown"),
        "serial_stored": False,
    }
