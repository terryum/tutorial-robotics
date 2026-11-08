"""Replaceable width-based gripper boundary; no vendor/device implementation."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class GripperState:
    width_m: float
    moving: bool
    fault: bool
    timestamp_s: float


class Gripper(Protocol):
    def state(self) -> GripperState: ...
    def command(
        self, *, width_m: float, speed_m_s: float, force_limit_n: float, timeout_s: float
    ) -> None: ...
    def stop(self) -> None: ...
