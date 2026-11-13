"""Portable bimanual input contract and latched command sink (SI, xyz+xyzw).

Raw device clocks are evidence, never compared across hosts. receive_time_ns is
assigned by the local collector using the same monotonic clock as poll().
"""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

STALE_AFTER_NS = 100_000_000


@dataclass(frozen=True)
class HandInput:
    side: str
    pose: tuple[float, ...]
    joint_names: tuple[str, ...]
    joints: tuple[float, ...]
    tracked: bool
    pose_source: str
    finger_source: str

    def validate(self, side: str) -> None:
        if type(self.tracked) is not bool:
            raise ValueError("boolean tracking status required")
        if any(not isinstance(n, str) or not n for n in self.joint_names):
            raise ValueError("nonempty joint names required")
        if self.side != side:
            raise ValueError("left/right identity mismatch")
        if len(self.pose) != 7 or not all(math.isfinite(x) for x in self.pose + self.joints):
            raise ValueError("finite xyz+xyzw pose and joint values required")
        if abs(sum(x * x for x in self.pose[3:]) - 1) > 1e-5:
            raise ValueError("unit xyzw quaternion required")
        if len(self.joint_names) != len(self.joints) or len(set(self.joint_names)) != len(
            self.joints
        ):
            raise ValueError("unique named hand joints required")
        if not self.pose_source or not self.finger_source:
            raise ValueError("explicit input sources required")


@dataclass(frozen=True)
class BimanualFrame:
    sequence: int
    session: str
    receive_time_ns: int
    calibration_id: str
    left: HandInput
    right: HandInput
    raw: dict[str, Any]
    clutch: bool
    deadman: bool
    schema_version: int = 2
    frame_id: str = "world"
    units: str = "m-rad"
    quaternion_order: str = "xyzw"

    def validate(self) -> None:
        if self.schema_version != 2 or self.units != "m-rad" or self.quaternion_order != "xyzw":
            raise ValueError("unsupported input convention")
        if not self.session or not self.calibration_id or self.frame_id != "world":
            raise ValueError("session and calibrated world frame required")
        if type(self.clutch) is not bool or type(self.deadman) is not bool:
            raise ValueError("boolean clutch/deadman required")
        if type(self.sequence) is not int or type(self.receive_time_ns) is not int:
            raise ValueError("integer sequence and receive time required")
        if self.sequence < 0 or self.receive_time_ns < 0:
            raise ValueError("nonnegative sequence and local receive time required")
        self.left.validate("left")
        self.right.validate("right")
        # Reject NaN even in the preserved raw device record.
        import json

        json.dumps(self.raw, allow_nan=False)

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> BimanualFrame:
        value = dict(value)
        for side in ("left", "right"):
            hand = dict(value[side])
            for key in ("pose", "joint_names", "joints"):
                hand[key] = tuple(hand[key])
            value[side] = HandInput(**hand)
        frame = cls(**value)
        frame.validate()
        return frame


class CommandSink:
    """No hardware API. poll must run independently of blocking device readers."""

    def __init__(self, calibration_id: str):
        self.calibration_id = calibration_id
        self.session: str | None = None
        self.sequence = -1
        self.last: BimanualFrame | None = None
        self.armed = False
        self.released = False
        self.reason = "local-rearm-required"
        self.last_poll_ns = -1
        self.sources: tuple[str, ...] | None = None

    def hold(self, reason: str) -> None:
        self.armed = self.released = False
        self.last = None
        self.reason = reason

    def poll(self, now_ns: int) -> bool:
        if now_ns < self.last_poll_ns:
            self.hold("clock-rollback")
        self.last_poll_ns = now_ns
        if self.last is not None and now_ns - self.last.receive_time_ns >= STALE_AFTER_NS:
            self.hold("stale")
        return self.armed and self.last is not None and self.last.clutch and self.last.deadman

    def accept(self, frame: BimanualFrame, now_ns: int) -> bool:
        self.poll(now_ns)
        try:
            frame.validate()
        except (ValueError, TypeError):
            self.hold("invalid-frame")
            return False
        if self.session != frame.session:
            self.hold("reconnected")
            self.session, self.sequence = frame.session, -1
        reason = (
            "calibration-mismatch"
            if frame.calibration_id != self.calibration_id
            else "stale"
            if not 0 <= now_ns - frame.receive_time_ns < STALE_AFTER_NS
            else "sequence-rollback"
            if frame.sequence <= self.sequence
            else "tracking-loss"
            if not frame.left.tracked or not frame.right.tracked
            else ""
        )
        if reason:
            self.hold(reason)
            return False
        self.sequence = frame.sequence
        sources = (
            frame.left.pose_source,
            frame.left.finger_source,
            frame.right.pose_source,
            frame.right.finger_source,
        )
        if self.sources is not None and sources != self.sources:
            self.hold("source-changed")
        self.sources = sources
        if not frame.clutch or not frame.deadman:
            self.hold("switch-released")
            self.released = not frame.clutch and not frame.deadman
        elif not self.armed:
            self.released = False
        self.last = frame
        return self.poll(now_ns)

    def rearm_local(self, now_ns: int) -> bool:
        self.poll(now_ns)
        if not self.released or self.last is None:
            return False
        self.armed, self.released = True, False
        self.reason = "waiting-for-fresh-press"
        return True


def transform_pose(
    pose: tuple[float, ...], world_from_device: Any, tracker_from_wrist: Any
) -> tuple[float, ...]:
    """Compose world_from_device @ device_from_tracker @ tracker_from_wrist."""
    import numpy as np
    from scipy.spatial.transform import Rotation

    HandInput("left", pose, (), (), True, "transform", "none").validate("left")

    def matrix(value: Any) -> Any:
        value = np.asarray(value, dtype=float)
        if value.shape != (4, 4) or not np.isfinite(value).all():
            raise ValueError("finite SE3 transform required")
        if (
            not np.allclose(value[3], [0, 0, 0, 1])
            or not np.allclose(value[:3, :3].T @ value[:3, :3], np.eye(3))
            or not np.isclose(np.linalg.det(value[:3, :3]), 1)
        ):
            raise ValueError("rigid right-handed transform required")
        return value

    local = np.eye(4)
    local[:3, :3] = Rotation.from_quat(pose[3:]).as_matrix()
    local[:3, 3] = pose[:3]
    result = matrix(world_from_device) @ local @ matrix(tracker_from_wrist)
    return tuple(
        float(x) for x in np.r_[result[:3, 3], Rotation.from_matrix(result[:3, :3]).as_quat()]
    )
