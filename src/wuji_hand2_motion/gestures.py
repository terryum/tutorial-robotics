"""Semantic poses and minimum-jerk gesture trajectories."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from itertools import pairwise

import numpy as np

from wuji_hand2_motion.model import joint_names, prefix, validate_side


@dataclass(frozen=True)
class MotionTrajectory:
    """Dependency-light trajectory contract used by the core stage."""

    robot_id: str
    model_id: str
    joint_names: tuple[str, ...]
    time_from_start: np.ndarray
    positions: np.ndarray


GESTURE_NAMES = ("open", "relaxed", "fist", "pinch", "point", "spread")


def _finger_flex(pose: dict[str, float], side: str, finger: str, values) -> None:
    value = prefix(side)
    pose[f"{value}_{finger}_mcp_flex"] = values[0]
    pose[f"{value}_{finger}_pip"] = values[1]
    pose[f"{value}_{finger}_dip"] = values[2]


def gesture_pose(side: str, name: str) -> dict[str, float]:
    validate_side(side)
    if name not in GESTURE_NAMES:
        raise ValueError(f"unknown gesture {name!r}; choose from {GESTURE_NAMES}")
    value = prefix(side)
    pose = dict.fromkeys(joint_names(side), 0.0)
    fingers = ("index_finger", "middle_finger", "ring_finger", "pinky")

    if name == "open":
        return pose
    if name == "relaxed":
        pose[f"{value}_thumb_cmc_flex"] = 0.20
        pose[f"{value}_thumb_cmc_abd"] = -0.30
        pose[f"{value}_thumb_mcp"] = 0.25
        pose[f"{value}_thumb_ip"] = 0.20
        for finger in fingers:
            _finger_flex(pose, side, finger, (0.20, 0.35, 0.20))
        return pose
    if name == "fist":
        pose[f"{value}_thumb_cmc_flex"] = 0.45
        pose[f"{value}_thumb_cmc_abd"] = -0.65
        pose[f"{value}_thumb_mcp"] = 0.75
        pose[f"{value}_thumb_ip"] = 0.65
        for finger in fingers:
            _finger_flex(pose, side, finger, (0.85, 1.25, 0.85))
        return pose
    if name == "pinch":
        pose.update(gesture_pose(side, "relaxed"))
        pose[f"{value}_thumb_cmc_flex"] = 0.55
        pose[f"{value}_thumb_cmc_abd"] = -0.80
        pose[f"{value}_thumb_mcp"] = 0.75
        pose[f"{value}_thumb_ip"] = 0.65
        _finger_flex(pose, side, "index_finger", (0.55, 0.85, 0.60))
        return pose
    if name == "point":
        pose.update(gesture_pose(side, "fist"))
        _finger_flex(pose, side, "index_finger", (0.0, 0.0, 0.0))
        pose[f"{value}_thumb_cmc_abd"] = -0.25
        return pose

    pose[f"{value}_thumb_cmc_abd"] = -0.55
    pose[f"{value}_index_finger_mcp_abd"] = -0.35
    pose[f"{value}_middle_finger_mcp_abd"] = -0.10
    pose[f"{value}_ring_finger_mcp_abd"] = 0.15
    pose[f"{value}_pinky_mcp_abd"] = 0.35
    return pose


def gesture_trajectory(
    side: str,
    sequence: Sequence[str] = GESTURE_NAMES,
    *,
    transition_seconds: float = 1.5,
    rate_hz: float = 50.0,
) -> MotionTrajectory:
    if len(sequence) < 2:
        raise ValueError("gesture sequence must contain at least two poses")
    if transition_seconds <= 0.0 or rate_hz <= 0.0:
        raise ValueError("transition_seconds and rate_hz must be positive")

    names = joint_names(side)
    rows: list[np.ndarray] = []
    times: list[float] = []
    samples = max(2, round(transition_seconds * rate_hz) + 1)
    elapsed = 0.0
    for segment, (start_name, end_name) in enumerate(pairwise(sequence)):
        start = np.asarray([gesture_pose(side, start_name)[name] for name in names])
        end = np.asarray([gesture_pose(side, end_name)[name] for name in names])
        phase = np.linspace(0.0, 1.0, samples)
        blend = 10.0 * phase**3 - 15.0 * phase**4 + 6.0 * phase**5
        for index, weight in enumerate(blend):
            if segment and index == 0:
                continue
            rows.append(start + weight * (end - start))
            times.append(elapsed + index / rate_hz)
        elapsed += transition_seconds

    return MotionTrajectory(
        robot_id=f"wuji-hand2-{validate_side(side)}",
        model_id="wuji-description-v2026.8.19-beta2",
        joint_names=names,
        time_from_start=np.asarray(times),
        positions=np.asarray(rows),
    )
