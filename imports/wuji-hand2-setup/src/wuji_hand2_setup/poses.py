"""Small simulation-only verification poses."""

from __future__ import annotations

from collections.abc import Mapping

from wuji_hand2_setup.model import joint_names, side_prefix, validate_side


def verification_pose(side: str, name: str) -> Mapping[str, float]:
    validate_side(side)
    names = joint_names(side)
    if name == "open":
        return dict.fromkeys(names, 0.0)
    if name != "fist":
        raise ValueError("verification pose must be 'open' or 'fist'")

    prefix = side_prefix(side)
    pose = dict.fromkeys(names, 0.0)
    pose[f"{prefix}_thumb_cmc_flex"] = 0.45
    pose[f"{prefix}_thumb_cmc_abd"] = -0.65
    pose[f"{prefix}_thumb_mcp"] = 0.75
    pose[f"{prefix}_thumb_ip"] = 0.65
    for finger in ("index_finger", "middle_finger", "ring_finger", "pinky"):
        pose[f"{prefix}_{finger}_mcp_flex"] = 0.85
        pose[f"{prefix}_{finger}_pip"] = 1.25
        pose[f"{prefix}_{finger}_dip"] = 0.85
    return pose
