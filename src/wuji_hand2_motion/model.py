"""Pinned Wuji Hand 2 model contract."""

from __future__ import annotations

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DESCRIPTION_ROOT = (
    PROJECT_ROOT / ".cache/assets/wuji-description/hand2/hand2_beta2/body"
)
HAND_SIDES = ("left", "right")
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


def validate_side(side: str) -> str:
    normalized = side.lower()
    if normalized not in HAND_SIDES:
        raise ValueError(f"side must be one of {HAND_SIDES}, got {side!r}")
    return normalized


def prefix(side: str) -> str:
    return "l" if validate_side(side) == "left" else "r"


def joint_names(side: str) -> tuple[str, ...]:
    value = prefix(side)
    return tuple(f"{value}_{suffix}" for suffix in JOINT_SUFFIXES)


def model_path(side: str) -> Path:
    normalized = validate_side(side)
    candidates = (
        DESCRIPTION_ROOT / "mjcf" / f"{normalized}.xml",
        DESCRIPTION_ROOT / "mjcf" / f"wujihand2-beta2-{normalized}.xml",
    )
    path = next((candidate for candidate in candidates if candidate.is_file()), candidates[0])
    if not path.is_file():
        raise FileNotFoundError(
            f"missing pinned Wuji Hand 2 Beta 2 MJCF: {path}; "
            "run `pal assets fetch wuji-description-beta2`"
        )
    return path
