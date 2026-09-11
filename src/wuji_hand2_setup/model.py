"""Pinned Wuji Hand 2 model paths and naming."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal
from xml.etree import ElementTree

HandSide = Literal["left", "right"]
HAND_SIDES: tuple[HandSide, ...] = ("left", "right")
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DESCRIPTION_ROOT = PROJECT_ROOT / ".cache/assets/wuji-description/hand2/hand2_beta2/body"
MODEL_RELEASE = "v2026.8.19"
MODEL_COMMIT = "c003186833616b23c06784ebefe442474cc5f4b5"
ROS_DESCRIPTION_PACKAGE = "wuji_hand2_beta2_description"
USD_FILENAME = "wujihand2_beta2.usd"

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


def model_id(side: str, *, with_mount: bool = False) -> str:
    suffix = "-with-mount" if with_mount else ""
    return f"wujihand2-beta2-{validate_side(side)}{suffix}"


def model_variants() -> tuple[str, ...]:
    return tuple(
        model_id(side, with_mount=with_mount) for side in HAND_SIDES for with_mount in (False, True)
    )


def fingertip_sensor_frames(side: str) -> tuple[str, ...]:
    prefix = side_prefix(side)
    return tuple(
        f"{prefix}_{finger}_tip_sensor_frame"
        for finger in ("thumb", "index", "middle", "ring", "pinky")
    )


def model_path(side: str, *, with_mount: bool = False) -> Path:
    normalized = validate_side(side)
    mount = "_with_mount" if with_mount else ""
    id_suffix = "-with-mount" if with_mount else ""
    candidates = (
        DESCRIPTION_ROOT / "mjcf" / f"{normalized}{mount}.xml",
        DESCRIPTION_ROOT / "mjcf" / f"wujihand2-beta2-{normalized}{id_suffix}.xml",
    )
    path = next((candidate for candidate in candidates if candidate.is_file()), candidates[0])
    if not path.is_file():
        raise FileNotFoundError(
            f"Wuji Hand 2 Beta 2 MJCF is missing: {path}. "
            "Run `pal assets fetch wuji-description-beta2`."
        )
    return path


def ros_urdf_path(side: str, *, with_mount: bool = False) -> Path:
    normalized = validate_side(side)
    suffix = "-with-mount" if with_mount else ""
    path = DESCRIPTION_ROOT / "urdf" / f"{normalized}{suffix}-ros.urdf"
    if not path.is_file():
        raise FileNotFoundError(
            f"Wuji Hand 2 Beta 2 ROS URDF is missing: {path}. "
            "Run `pal assets fetch wuji-description-beta2`."
        )
    return path


@dataclass(frozen=True)
class ModelInventory:
    joints: int
    fingertip_sites: int
    fingertip_sensor_frames: int
    collision_geoms: int
    total_explicit_mass_kg: float


def inspect_model_xml(path: Path) -> ModelInventory:
    """Inspect the Beta 2 structural contract without importing MuJoCo."""

    root = ElementTree.parse(path).getroot()
    joints = root.findall(".//joint")
    sites = [item for item in root.findall(".//site") if item.get("name", "").endswith("_tip")]
    frames = [
        item
        for item in root.findall(".//body")
        if item.get("name", "").endswith("_tip_sensor_frame")
    ]
    geoms = root.findall(".//geom")
    masses = [float(item.get("mass", "0")) for item in root.findall(".//inertial")]
    return ModelInventory(
        joints=len(joints),
        fingertip_sites=len(sites),
        fingertip_sensor_frames=len(frames),
        collision_geoms=len(geoms),
        total_explicit_mass_kg=sum(masses),
    )


def validate_beta2_inventory(inventory: ModelInventory) -> list[str]:
    errors: list[str] = []
    if inventory.joints != 20:
        errors.append(f"expected 20 joints, got {inventory.joints}")
    if inventory.fingertip_sites != 5:
        errors.append(f"expected 5 fingertip sites, got {inventory.fingertip_sites}")
    if inventory.fingertip_sensor_frames != 5:
        errors.append(
            f"expected 5 fingertip sensor frames, got {inventory.fingertip_sensor_frames}"
        )
    if inventory.collision_geoms <= 0:
        errors.append("expected at least one collision geom")
    if inventory.total_explicit_mass_kg <= 0.0:
        errors.append("expected positive explicit mass")
    return errors
