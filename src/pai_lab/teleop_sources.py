"""Explicit source selection over read-only device envelopes; no vendor imports."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import pairwise
from typing import Any

from pai_lab.teleop import STALE_AFTER_NS, BimanualFrame, HandInput, transform_pose


@dataclass(frozen=True)
class DeviceSample:
    source: str
    side: str
    receive_time_ns: int
    device_time: int
    device_clock: str
    frame_id: str
    tracked: bool
    pose: tuple[float, ...]
    joint_names: tuple[str, ...] = ()
    joints: tuple[float, ...] = ()


class InputMux:
    def __init__(
        self, *, mode: str, calibration_id: str, transforms: dict[str, Any], mounts: dict[str, Any]
    ):
        if mode not in {"integrated", "quest-only"} or not calibration_id:
            raise ValueError("explicit integrated/quest-only mode and calibration required")
        self.mode, self.calibration_id = mode, calibration_id
        self.transforms, self.mounts = transforms, mounts

    def combine(
        self,
        samples: list[DeviceSample],
        *,
        quest_switches: dict[str, Any],
        session: str,
        sequence: int,
        now_ns: int,
    ) -> BimanualFrame:
        from dataclasses import asdict

        indexed = {(s.source, s.side): s for s in samples}
        if len(indexed) != len(samples):
            raise ValueError("duplicate source/side")
        pose_source = "vive" if self.mode == "integrated" else "quest"
        finger_source = "manus" if self.mode == "integrated" else "quest"
        hands = []
        selected = []
        for side in ("left", "right"):
            pose = indexed[pose_source, side]
            fingers = indexed[finger_source, side]
            selected.extend([pose, fingers])
            for sample in (pose, fingers):
                if not 0 <= now_ns - sample.receive_time_ns < STALE_AFTER_NS:
                    raise ValueError("stale device sample")
                if not sample.device_clock or not sample.frame_id:
                    raise ValueError("raw clock/frame required")
            hands.append(
                HandInput(
                    side,
                    transform_pose(pose.pose, self.transforms[pose.frame_id], self.mounts[side]),
                    fingers.joint_names,
                    fingers.joints,
                    pose.tracked and fingers.tracked,
                    pose_source,
                    finger_source,
                )
            )
        switch_time = quest_switches["receive_time_ns"]
        if not 0 <= now_ns - switch_time < STALE_AFTER_NS:
            raise ValueError("stale Quest switches")
        result = BimanualFrame(
            sequence,
            session,
            min(switch_time, *(s.receive_time_ns for s in selected)),
            self.calibration_id,
            hands[0],
            hands[1],
            {"devices": [asdict(s) for s in samples], "quest": quest_switches, "mode": self.mode},
            quest_switches["clutch"],
            quest_switches["deadman"],
        )
        result.validate()
        return result


def rate_report(samples: list[DeviceSample], duration_ns: int = 60_000_000_000) -> dict[str, Any]:
    if len(samples) < 2:
        raise ValueError("at least two input samples required")
    times = [s.receive_time_ns for s in samples]
    gaps = [b - a for a, b in pairwise(times)]
    if min(gaps) <= 0 or len({(s.source, s.side) for s in samples}) != 1:
        raise ValueError("one ordered device stream required")
    elapsed = times[-1] - times[0]
    return {
        "duration_ns": elapsed,
        "full_60s": elapsed >= duration_ns,
        "rate_hz": (len(samples) - 1) * 1e9 / elapsed,
        "maximum_gap_ns": max(gaps),
        "tracking_valid_ratio": sum(s.tracked for s in samples) / len(samples),
    }
