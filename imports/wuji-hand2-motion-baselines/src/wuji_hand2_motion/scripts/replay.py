"""Replay a trained Wuji Hand 2 PPO policy in the MuJoCo viewer."""

from __future__ import annotations

import argparse
from pathlib import Path
import time

import mujoco.viewer
from stable_baselines3 import PPO

from wuji_hand2_motion.scripts.train import PROJECT_ROOT, make_env, resolve_device


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("joint-reach", "cube-yaw"), required=True)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--duration", type=float, default=30.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("cpu", "mps", "auto"), default="cpu")
    args = parser.parse_args()
    stem = f"wuji_hand2_{args.side}_{args.task.replace('-', '_')}_ppo.zip"
    checkpoint = args.checkpoint or PROJECT_ROOT / "checkpoints" / stem
    env = make_env(args.task, args.side)
    model = PPO.load(checkpoint, device=resolve_device(args.device))
    observation, _ = env.reset(seed=args.seed)
    with mujoco.viewer.launch_passive(env.model, env.data) as viewer:
        viewer.cam.lookat[:] = (0.0, -0.04, -0.08)
        viewer.cam.distance = 0.45
        viewer.cam.azimuth = 135
        viewer.cam.elevation = -20
        started = time.monotonic()
        episode = 0
        while viewer.is_running() and time.monotonic() - started < args.duration:
            loop_started = time.monotonic()
            action, _ = model.predict(observation, deterministic=True)
            observation, _, terminated, truncated, _ = env.step(action)
            viewer.sync()
            if terminated or truncated:
                episode += 1
                observation, _ = env.reset(seed=args.seed + episode)
            remaining = env.control_dt - (time.monotonic() - loop_started)
            if remaining > 0:
                time.sleep(remaining)
    env.close()


if __name__ == "__main__":
    main()
