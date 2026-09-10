"""Wuji Hand 2 wrapper around the shared native-actuator backend."""

from __future__ import annotations

from pathlib import Path

try:
    from mujoco_ros2_core import MujocoPositionActuatorBackend
except ModuleNotFoundError:
    class MujocoPositionActuatorBackend:  # type: ignore[no-redef]
        """Import-safe sentinel when the ROS extra is unavailable."""

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            raise RuntimeError(
                "mujoco-ros2-core is unavailable; install the `ros` extra for this backend"
            )

from wuji_hand2_setup.model import joint_names, model_path, validate_side


class WujiHand2MujocoBackend(MujocoPositionActuatorBackend):
    """Simulate one Wuji Hand 2 side through all 20 native actuators."""

    def __init__(
        self,
        side: str = "right",
        *,
        path: str | Path | None = None,
        frame_skip: int = 10,
    ) -> None:
        self.side = validate_side(side)
        super().__init__(
            path or model_path(self.side),
            joint_names(self.side),
            frame_skip=frame_skip,
        )
