"""Train and evaluate a Wuji Hand 2 PPO baseline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Protocol

import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
import torch

from wuji_hand2_motion.envs import WujiHand2CubeYawEnv, WujiHand2JointReachEnv


PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Policy(Protocol):
    def predict(self, observation, deterministic=True): ...


def make_env(task: str, side: str):
    if task == "joint-reach":
        return WujiHand2JointReachEnv(side)
    return WujiHand2CubeYawEnv(side)


def resolve_device(requested: str) -> str:
    if requested == "auto":
        return "mps" if torch.backends.mps.is_available() else "cpu"
    if requested == "mps" and not torch.backends.mps.is_available():
        raise SystemExit("MPS is unavailable; use --device cpu")
    return requested


def evaluate(task: str, side: str, policy: Policy | None, episodes: int, seed: int):
    env = make_env(task, side)
    rng = np.random.default_rng(seed)
    returns: list[float] = []
    errors: list[float] = []
    drops: list[float] = []
    for episode in range(episodes):
        observation, _ = env.reset(seed=seed + episode)
        total = 0.0
        while True:
            if policy is None:
                action = rng.uniform(-1.0, 1.0, size=env.action_space.shape)
            else:
                action, _ = policy.predict(observation, deterministic=True)
            observation, reward, terminated, truncated, info = env.step(action)
            total += reward
            if terminated or truncated:
                returns.append(total)
                key = "joint_error_rmse" if task == "joint-reach" else "yaw_error_rad"
                errors.append(float(info[key]))
                drops.append(float(info.get("is_dropped", 0.0)))
                break
    env.close()
    return {
        "mean_return": float(np.mean(returns)),
        "mean_error": float(np.mean(errors)),
        "drop_rate": float(np.mean(drops)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("joint-reach", "cube-yaw"), required=True)
    parser.add_argument("--side", choices=("left", "right"), default="right")
    parser.add_argument("--timesteps", type=int)
    parser.add_argument("--eval-episodes", type=int, default=20)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--device", choices=("cpu", "mps", "auto"), default="cpu")
    args = parser.parse_args()
    timesteps = args.timesteps or (20_000 if args.task == "joint-reach" else 500_000)
    device = resolve_device(args.device)
    checkpoint_dir = PROJECT_ROOT / "checkpoints"
    run_dir = PROJECT_ROOT / "runs"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    run_dir.mkdir(parents=True, exist_ok=True)
    stem = f"wuji_hand2_{args.side}_{args.task.replace('-', '_')}_ppo"

    before = evaluate(args.task, args.side, None, args.eval_episodes, args.seed)
    training_env = Monitor(make_env(args.task, args.side))
    model = PPO(
        "MlpPolicy",
        training_env,
        device=device,
        seed=args.seed,
        policy_kwargs={"net_arch": [256, 256]},
        n_steps=512 if args.task == "joint-reach" else 2048,
        batch_size=64 if args.task == "joint-reach" else 256,
        n_epochs=5 if args.task == "joint-reach" else 10,
        learning_rate=3e-4,
        gamma=0.99,
        gae_lambda=0.95,
        ent_coef=0.001 if args.task == "cube-yaw" else 0.0,
        verbose=1,
        tensorboard_log=str(run_dir),
    )
    model.learn(total_timesteps=timesteps, progress_bar=False)
    checkpoint = checkpoint_dir / stem
    model.save(checkpoint)
    training_env.close()
    after = evaluate(args.task, args.side, model, args.eval_episodes, args.seed)
    metrics = {
        "task": args.task,
        "side": args.side,
        "timesteps": timesteps,
        "seed": args.seed,
        "device": device,
        "random": before,
        "trained": after,
    }
    metrics_path = checkpoint_dir / f"{stem}_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))
    print(f"checkpoint: {checkpoint.with_suffix('.zip')}")


if __name__ == "__main__":
    main()
