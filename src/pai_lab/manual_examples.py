"""Offline contract exercises. No SDK, transport, hardware readiness or learner writes.

The envelope and freshness budgets are teaching conventions, not vendor wire formats.
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
G1_IDS = tuple(range(29))
G1_ABSENT_23 = {13, 14, 20, 21, 27, 28}
DEVICES = ("enlight", "fr3", "g1", "wuji", "sharpa", "aloha")


def finite(value: Any) -> bool:
    return type(value) in (int, float) and math.isfinite(value)


def vector(value: Any, size: int, name: str) -> None:
    if not isinstance(value, list) or len(value) != size or not all(map(finite, value)):
        raise ValueError(f"{name}: expected {size} finite values")


def g1_ids(dof: int, waist_locked: bool) -> tuple[int, ...]:
    if dof not in (23, 29) or type(waist_locked) is not bool:
        raise ValueError("Select 23/29 DoF and explicit waist lock state")
    absent = G1_ABSENT_23 if dof == 23 else ({13, 14} if waist_locked else set())
    return tuple(i for i in G1_IDS if i not in absent)


def fixture(
    device: str, *, side: str = "right", dof: int = 29, waist_locked: bool = False
) -> dict[str, Any]:
    if device not in DEVICES or side not in ("left", "right"):
        raise ValueError("Unknown device or side")
    locks = json.loads((ROOT / "assets/model-lock.json").read_text())["models"]
    refs = json.loads((ROOT / "assets/manual-code-refs.json").read_text())["sources"]
    repo = {
        "enlight": "flexiv_rdk",
        "fr3": "libfranka",
        "g1": "unitree_sdk2_python",
        "wuji": "wuji-sdk",
        "sharpa": "sharpa-wave-sdk",
        "aloha": "aloha",
    }[device]
    sdk = next(s["revision"] for s in refs if s["repository"].endswith("/" + repo))
    frame = {
        "enlight": "base",
        "fr3": "O",
        "g1": "pelvis",
        "wuji": side[0] + "_wrist",
        "sharpa": side + "_hand_C_MC",
        "aloha": "episode",
    }[device]
    count = {"enlight": 7, "fr3": 7, "g1": 29, "wuji": 20, "sharpa": 22, "aloha": 14}[device]
    ids = g1_ids(dof, waist_locked) if device == "g1" else tuple(range(count))
    packet: dict[str, Any] = {
        "schema_version": 1,
        "synthetic": True,
        "device": device,
        "side": side,
        "model_revision": locks[device]["revision"],
        "sdk_revision": sdk,
        "frame_id": frame,
        "clock": "synthetic-monotonic",
        "received_at_s": 10.0,
        "position_unit": "rad",
        "velocity_unit": "rad/s",
        "effort_unit": "A" if device == "wuji" else "N*m",
        "joints": [{"nid": i, "position": i / 100, "velocity": 0.0, "effort": 0.0} for i in ids],
    }
    if device == "g1":
        packet.update(
            dof=dof, waist_locked=waist_locked, motor_state=[{"q": i / 100} for i in G1_IDS]
        )
    if device in ("enlight", "fr3"):
        packet["sdk_state"] = {
            "q": [i / 100 for i in ids],
            "dq": [0.0] * count,
            "tau" if device == "enlight" else "tau_J": [0.0] * count,
        }
        packet["pose"] = {
            "parent": frame,
            "child": "tcp" if device == "enlight" else "EE",
            "translation_unit": "m",
            "translation": [0.0, 0.0, 0.5],
            "quaternion_order": "wxyz",
            "quaternion": [1.0, 0.0, 0.0, 0.0],
        }
    if device == "wuji":
        packet["header"] = {"timestamp_us": 10_000_000, "frame_id": frame}
        packet["firmware"] = "synthetic-format-v1"
        packet["tactile"] = {
            "format_version": 1,
            "digest": "synthetic-format",
            "point_unit": "normalized",
            "aggregate_unit": "N",
            "temperature_unit": "C",
            "frame_id": side[0] + "_thumb_tip_sensor_frame",
            "positions_unit": "m",
            "positions": [[0.0, 0.0, 0.0]],
            "points": [[0.0, 0.0, 0.2]],
            "aggregate_force": [0.0, 0.0, 0.5],
            "temperature": 25.0,
        }
    if device == "aloha":
        packet["episode"] = {
            "format": "synthetic-aloha-v1",
            "configuration": "stationary-bimanual",
            "camera_names": ["cam_high", "cam_low", "cam_left_wrist", "cam_right_wrist"],
            "joint_unit": "rad",
            "gripper_unit": "normalized",
            "timestamp_s": [9.98, 10.0],
            "qpos": [[0.0] * 14 for _ in range(2)],
            "action": [[0.0] * 14 for _ in range(2)],
            "cameras": {
                n: [9.981, 10.001]
                for n in ["cam_high", "cam_low", "cam_left_wrist", "cam_right_wrist"]
            },
        }
    return packet


def check(
    packet: dict[str, Any],
    expected: dict[str, Any],
    *,
    now_s: float = 10.05,
    max_age_s: float = 0.1,
    allow_partial: bool = False,
) -> dict[str, Any]:
    """Validate against an independently selected profile; partial Wuji frames stay incomplete."""
    for key in (
        "schema_version",
        "synthetic",
        "device",
        "side",
        "model_revision",
        "sdk_revision",
        "frame_id",
        "clock",
        "position_unit",
        "velocity_unit",
        "effort_unit",
    ):
        if packet.get(key) != expected[key]:
            raise ValueError(f"{key}: contract mismatch")
    if not all(map(finite, [now_s, max_age_s, packet.get("received_at_s")])) or max_age_s <= 0:
        raise ValueError("Invalid clock/freshness budget")
    age = now_s - packet["received_at_s"]
    if not 0 <= age <= max_age_s:
        raise ValueError("Stale or future reception timestamp")
    expected_ids = [j["nid"] for j in expected["joints"]]
    joints = packet.get("joints")
    if not isinstance(joints, list):
        raise TypeError("joints must be a list")
    indexed = {}
    for joint in joints:
        nid = joint.get("nid")
        if type(nid) is not int or nid not in expected_ids or nid in indexed:
            raise ValueError("Unknown or duplicate joint ID")
        vector([joint.get(k) for k in ("position", "velocity", "effort")], 3, "joint state")
        indexed[nid] = joint
    missing = [i for i in expected_ids if i not in indexed]
    if missing and not (allow_partial and packet["device"] == "wuji"):
        raise ValueError(f"Missing joints: {missing}")
    device = packet["device"]
    if device in ("enlight", "fr3"):
        state = packet.get("sdk_state", {})
        for field, joint_field in (
            ("q", "position"),
            ("dq", "velocity"),
            ("tau" if device == "enlight" else "tau_J", "effort"),
        ):
            vector(state.get(field), 7, field)
            if state[field] != [indexed[i][joint_field] for i in expected_ids]:
                raise ValueError("SDK array/order mismatch")
        pose = packet.get("pose", {})
        for key in ("parent", "child", "translation_unit", "quaternion_order"):
            if pose.get(key) != expected["pose"][key]:
                raise ValueError("Pose frame/unit mismatch")
        vector(pose.get("translation"), 3, "translation")
        vector(pose.get("quaternion"), 4, "quaternion")
        if abs(sum(x * x for x in pose["quaternion"]) - 1) > 1e-6:
            raise ValueError("Quaternion must have unit norm")
    elif device == "g1":
        if any(packet.get(k) != expected[k] for k in ("dof", "waist_locked")):
            raise ValueError("G1 configuration mismatch")
        motor = packet.get("motor_state", [])
        if len(motor) != 29:
            raise ValueError("The synthetic SDK envelope requires all 29 slots")
        for i in expected_ids:
            if not finite(motor[i].get("q")) or motor[i]["q"] != indexed[i]["position"]:
                raise ValueError("SDK slot must match ID, not compact-array offset")
    elif device == "wuji":
        if packet.get("firmware") != expected["firmware"]:
            raise ValueError("Firmware mismatch")
        header = packet.get("header", {})
        timestamp = header.get("timestamp_us")
        if type(timestamp) is not int or timestamp != round(packet["received_at_s"] * 1_000_000):
            raise ValueError("Synthetic timestamp_us unit mismatch")
        if header.get("frame_id") != expected["frame_id"]:
            raise ValueError("Wuji header frame mismatch")
        tactile = packet.get("tactile", {})
        for key in (
            "format_version",
            "digest",
            "point_unit",
            "aggregate_unit",
            "temperature_unit",
            "frame_id",
            "positions_unit",
        ):
            if tactile.get(key) != expected["tactile"][key]:
                raise ValueError(f"Tactile metadata mismatch: {key}")
        points, positions = tactile.get("points", []), tactile.get("positions", [])
        if not points or len(points) != len(positions):
            raise ValueError("Tactile geometry/count mismatch")
        for point, position in zip(points, positions, strict=True):
            vector(point, 3, "tactile point")
            vector(position, 3, "tactile position")
            if tactile["point_unit"] == "normalized" and not (
                -1 <= point[0] <= 1 and -1 <= point[1] <= 1 and 0 <= point[2] <= 1
            ):
                raise ValueError("Normalized force out of range")
        vector(tactile.get("aggregate_force"), 3, "aggregate force")
        if not finite(tactile.get("temperature")):
            raise ValueError("Invalid tactile temperature")
    elif device == "aloha":
        check_episode(packet["episode"], expected["episode"])
    return {
        "device": device,
        "complete": not missing,
        "missing_ids": missing,
        "ordered_positions": [
            indexed[i]["position"] if i in indexed else None for i in expected_ids
        ],
        "effort_unit": packet["effort_unit"],
        "hardware_evidence": False,
    }


def check_episode(episode: dict[str, Any], expected: dict[str, Any]) -> None:
    for key in ("format", "configuration", "camera_names", "joint_unit", "gripper_unit"):
        if episode.get(key) != expected[key]:
            raise ValueError(f"Episode {key} mismatch")
    ts = episode.get("timestamp_s", [])
    if not ts or not all(map(finite, ts)) or any(b <= a for a, b in itertools.pairwise(ts)):
        raise ValueError("Episode timestamps must increase")
    for key in ("qpos", "action"):
        rows = episode.get(key, [])
        if len(rows) != len(ts):
            raise ValueError("Episode row count mismatch")
        for row in rows:
            vector(row, 14, key)
            if any(not 0 <= row[i] <= 1 for i in (6, 13)):
                raise ValueError("Synthetic normalized gripper out of range")
    cameras = episode.get("cameras", {})
    if set(cameras) != set(expected["camera_names"]):
        raise ValueError("Camera set mismatch")
    for values in cameras.values():
        if len(values) != len(ts) or not all(map(finite, values)):
            raise ValueError("Camera length/timestamp mismatch")
        if any(b <= a for a, b in itertools.pairwise(values)):
            raise ValueError("Camera timestamps must increase")
        if any(abs(a - b) > 0.01 for a, b in zip(ts, values, strict=True)):
            raise ValueError("Camera misalignment exceeds synthetic 10 ms budget")


def inspect_hands() -> dict[str, Any]:
    """Check actual pinned left/right model inventories; no SDK-axis claim."""
    import mujoco

    from pai_lab.lessons.models import provenance

    result = {}
    for device, bundle, relative, count in (
        ("sharpa", "mujoco-menagerie", "sharpa_wave/scene_{side}.xml", 22),
        ("wuji", "wuji-description", "hand2/hand2_beta2/body/mjcf/{side}.xml", 20),
    ):
        provenance(device)
        inventories = []
        for side in ("left", "right"):
            model = mujoco.MjModel.from_xml_path(
                str(ROOT / ".cache/assets" / bundle / relative.format(side=side))
            )
            names = [
                mujoco.mj_id2name(model, mujoco.mjtObj.mjOBJ_JOINT, i) for i in range(model.njnt)
            ]
            prefix = side + "_" if device == "sharpa" else side[0] + "_"
            root = side + "_hand_C_MC" if device == "sharpa" else side[0] + "_wrist"
            if (
                model.njnt != count
                or model.nu != count
                or any(not n or not n.startswith(prefix) for n in names)
            ):
                raise ValueError("Hand model joint inventory mismatch")
            if mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_BODY, root) < 0:
                raise ValueError("Missing hand root frame")
            inventories.append({"side": side, "joints": names, "root_frame": root})
        result[device] = inventories
    return {"models": result, "sdk_axis_mapping_verified": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("device", choices=[*DEVICES, "all", "hands"])
    args = parser.parse_args()
    if args.device == "hands":
        print(json.dumps(inspect_hands(), indent=2))
        return
    output = []
    for device in DEVICES if args.device == "all" else (args.device,):
        expected = fixture(device)
        packet = copy.deepcopy(expected)
        packet["joints"].reverse()
        output.append(check(packet, expected))
    print(json.dumps({"synthetic_only": True, "results": output}, indent=2))


if __name__ == "__main__":
    main()
