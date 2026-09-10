"""Replay the semantic Wuji Hand 2 gesture sequence in MuJoCo."""

from __future__ import annotations

import argparse
import time

import mujoco.viewer
from mujoco_ros2_core import MujocoPositionActuatorBackend, validate_trajectory

from wuji_hand2_motion.gestures import GESTURE_NAMES, gesture_trajectory
from wuji_hand2_motion.model import joint_names, model_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    parser.add_argument("--sequence", default=",".join(GESTURE_NAMES))
    args = parser.parse_args()
    sequence = tuple(item.strip() for item in args.sequence.split(",") if item.strip())
    trajectory = gesture_trajectory(args.side, sequence)
    backend = MujocoPositionActuatorBackend(model_path(args.side), joint_names(args.side))
    report = validate_trajectory(
        trajectory,
        known_joints=set(backend.joint_names),
        position_limits=backend.position_limits,
        max_velocity=3.0,
    )
    if not report.is_valid:
        raise SystemExit("; ".join(report.errors))

    with mujoco.viewer.launch_passive(backend.model, backend.data) as viewer:
        viewer.cam.lookat[:] = (0.0, 0.0, -0.08)
        viewer.cam.distance = 0.45
        viewer.cam.azimuth = 135
        viewer.cam.elevation = -20
        for row in trajectory.positions:
            if not viewer.is_running():
                break
            started = time.monotonic()
            backend.set_joint_targets(dict(zip(trajectory.joint_names, row)))
            backend.step()
            viewer.sync()
            remaining = backend.control_dt - (time.monotonic() - started)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
