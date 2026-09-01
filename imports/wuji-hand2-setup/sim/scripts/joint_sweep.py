"""Sweep one Wuji Hand 2 joint through a small native-actuator motion."""

from __future__ import annotations

import argparse
import math
import time

import mujoco.viewer

from wuji_hand2_setup import WujiHand2MujocoBackend, joint_names


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    parser.add_argument("--joint")
    parser.add_argument("--duration", type=float, default=20.0)
    parser.add_argument("--amplitude", type=float, default=0.35)
    args = parser.parse_args()

    backend = WujiHand2MujocoBackend(args.side)
    joint = args.joint or joint_names(args.side)[4]
    if joint not in backend.controlled_joints:
        raise SystemExit(f"unknown {args.side} joint: {joint}")
    home = float(backend.home[backend.controlled_joints.index(joint)])

    with mujoco.viewer.launch_passive(backend.model, backend.data) as viewer:
        viewer.cam.lookat[:] = (0.0, 0.0, -0.08)
        viewer.cam.distance = 0.45
        viewer.cam.azimuth = 135
        viewer.cam.elevation = -20
        started = time.monotonic()
        while viewer.is_running() and time.monotonic() - started < args.duration:
            loop_started = time.monotonic()
            elapsed = loop_started - started
            target = home + args.amplitude * math.sin(2.0 * math.pi * 0.2 * elapsed)
            backend.set_joint_targets({joint: target})
            backend.step()
            viewer.sync()
            remaining = backend.control_dt - (time.monotonic() - loop_started)
            if remaining > 0:
                time.sleep(remaining)


if __name__ == "__main__":
    main()
