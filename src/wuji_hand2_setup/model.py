"""Pinned Wuji Hand 2 model paths and naming."""

from __future__ import annotations

from pathlib import Path
from typing import Literal


HandSide = Literal["left", "right"]
HAND_SIDES: tuple[HandSide, ...] = ("left", "right")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DESCRIPTION_ROOT = (
    PROJECT_ROOT / "assets/vendor/wuji-description/hand2/hand2_beta1/body"
)

JOINT_SUFFIXES = (
    "thumb_cmc_flex",
    "thumb_cmc_abd",
    "thumb_mcp",
    "thumb_ip",
    "index_finger_mcp_flex",
    "index_finger_mcp_abd",
    "index_finger_pip",
    "index_finger_dip",
    "middle_finger_mcp_flex",
    "middle_finger_mcp_abd",
    "middle_finger_pip",
    "middle_finger_dip",
    "ring_finger_mcp_flex",
    "ring_finger_mcp_abd",
    "ring_finger_pip",
    "ring_finger_dip",
    "pinky_mcp_flex",
    "pinky_mcp_abd",
    "pinky_pip",
    "pinky_dip",
)


def validate_side(side: str) -> HandSide:
    normalized = side.lower()
    if normalized not in HAND_SIDES:
        raise ValueError(f"side must be one of {HAND_SIDES}, got {side!r}")
    return normalized  # type: ignore[return-value]


def side_prefix(side: str) -> str:
    return "l" if validate_side(side) == "left" else "r"


def joint_names(side: str) -> tuple[str, ...]:
    prefix = side_prefix(side)
    return tuple(f"{prefix}_{suffix}" for suffix in JOINT_SUFFIXES)


def model_path(side: str) -> Path:
    path = DESCRIPTION_ROOT / "mjcf" / f"{validate_side(side)}.xml"
    if not path.is_file():
        raise FileNotFoundError(
            f"Wuji Hand 2 MJCF is missing: {path}. Initialize Git submodules."
        )
    return path


def ros_urdf_path(side: str) -> Path:
    path = DESCRIPTION_ROOT / "urdf" / f"{validate_side(side)}-ros.urdf"
    if not path.is_file():
        raise FileNotFoundError(
            f"Wuji Hand 2 ROS URDF is missing: {path}. Initialize Git submodules."
        )
    return path
