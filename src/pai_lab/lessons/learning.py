"""Minimal NumPy PPO, measured MuJoCo demonstrations, BC, and ACT/VLA contracts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from pai_lab.catalog import ROOT
from pai_lab.lessons.experiment import Experiment, render
from pai_lab.lessons.models import load
from pai_lab.lessons.physics import pendulum
from pai_lab.local import write_json
from pai_lab.progress import load_progress


def previous_run(identifier: str) -> Path:
    entry = load_progress().completed.get(identifier)
    if not entry:
        raise FileNotFoundError(f"finish {identifier} to provide its actual data/policy artifact")
    path = Path(entry["run_dir"])
    return path if path.is_absolute() else ROOT / path


class Reach:
    """Bounded 7-action FR3 reach task; world-frame target and 17-value observation."""

    def __init__(self, seed: int):
        self.model, self.data, self.source = load("fr3")
        self.home = self.data.qpos.copy()
        self.rng = np.random.default_rng(seed)
        self.target = self.data.site_xpos[0].copy()
        self.steps = 0

    def observation(self) -> np.ndarray:
        return np.concatenate(
            [
                self.data.qpos - self.home,
                self.data.qvel * 0.1,
                (self.target - self.data.site_xpos[0]) * 10.0,
            ]
        )

    def reset(self) -> np.ndarray:
        mujoco.mj_resetDataKeyframe(self.model, self.data, 0)
        mujoco.mj_forward(self.model, self.data)
        self.target = self.data.site_xpos[0] + self.rng.uniform(-0.035, 0.035, 3)
        self.steps = 0
        return self.observation()

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool]:
        self.data.ctrl[:] = np.clip(
            self.data.qpos + 0.03 * np.tanh(action),
            self.model.jnt_range[:, 0],
            self.model.jnt_range[:, 1],
        )
        for _ in range(10):
            mujoco.mj_step(self.model, self.data)
        distance = float(np.linalg.norm(self.target - self.data.site_xpos[0]))
        self.steps += 1
        return (
            self.observation(),
            -distance - 0.001 * float(np.sum(action**2)),
            distance < 0.008,
            self.steps >= 64,
        )


class Pendulum:
    def __init__(self, seed: int):
        self.model, self.data = pendulum()
        self.rng = np.random.default_rng(seed)
        self.steps = 0

    def observation(self) -> np.ndarray:
        return np.array([self.data.qpos[0], self.data.qvel[0] * 0.2])

    def reset(self) -> np.ndarray:
        mujoco.mj_resetData(self.model, self.data)
        self.data.qpos[0] = self.rng.uniform(-0.6, 0.6)
        self.steps = 0
        mujoco.mj_forward(self.model, self.data)
        return self.observation()

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool]:
        self.data.ctrl[:] = 3 * np.tanh(action)
        for _ in range(10):
            mujoco.mj_step(self.model, self.data)
        self.steps += 1
        q, v = self.data.qpos[0], self.data.qvel[0]
        return (
            self.observation(),
            -float(q * q + 0.05 * v * v + 0.001 * np.sum(action**2)),
            False,
            self.steps >= 64,
        )


def generalized_advantage(
    rewards: np.ndarray,
    values: np.ndarray,
    following_values: np.ndarray,
    terminal: np.ndarray,
    boundary: np.ndarray,
    gamma: float = 0.99,
    lam: float = 0.95,
) -> np.ndarray:
    result = np.zeros(len(rewards))
    carry = 0.0
    for i in range(len(rewards) - 1, -1, -1):
        delta = rewards[i] + gamma * following_values[i] * (1 - terminal[i]) - values[i]
        carry = delta + gamma * lam * (1 - boundary[i]) * carry
        result[i] = carry
    return result


def ppo(environment: Any, output: Path, seed: int, samples: int, variant: float) -> Experiment:
    rng = np.random.default_rng(seed)
    observation = environment.reset()
    action_dim = environment.model.nu
    dimension = len(observation) + 1
    weights = rng.normal(0.0, 0.01, (dimension, action_dim))
    initial = weights.copy()
    value_weights = np.zeros(dimension)
    sigma = 0.3
    rows, diagnostics = [], []
    updates = max(4, min(32, samples // 8))
    rollout_length = 128
    for update in range(updates):
        xs, action_samples, means, rewards, values, next_values, terminals, boundaries = (
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
        )
        for _ in range(rollout_length):
            x = np.append(np.clip(observation, -5, 5), 1.0)
            mean = x @ weights
            action = mean + rng.normal(0, sigma, action_dim)
            following, reward, terminated, truncated = environment.step(action)
            xs.append(x)
            action_samples.append(action)
            means.append(mean)
            rewards.append(reward)
            values.append(float(x @ value_weights))
            next_values.append(float(np.append(np.clip(following, -5, 5), 1.0) @ value_weights))
            terminals.append(terminated)
            boundaries.append(terminated or truncated)
            observation = environment.reset() if terminated or truncated else following
        x = np.asarray(xs)
        actions = np.asarray(action_samples)
        old_mean = np.asarray(means)
        advantages = generalized_advantage(
            np.array(rewards),
            np.array(values),
            np.array(next_values),
            np.array(terminals),
            np.array(boundaries),
        )
        returns = advantages + np.array(values)
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        old_logp = -0.5 * np.sum(((actions - old_mean) / sigma) ** 2, axis=1)
        for _ in range(4):
            mean = x @ weights
            logp = -0.5 * np.sum(((actions - mean) / sigma) ** 2, axis=1)
            ratio = np.exp(np.clip(logp - old_logp, -20, 20))
            unclipped = ratio * advantages
            clipped = np.clip(ratio, 0.8, 1.2) * advantages
            active = ((advantages >= 0) & (ratio <= 1.2)) | ((advantages < 0) & (ratio >= 0.8))
            gradient = (
                x.T
                @ ((active * advantages * ratio)[:, None] * (actions - mean) / sigma**2)
                / rollout_length
            )
            gradient /= max(1.0, np.linalg.norm(gradient))
            weights += 0.01 * variant * gradient
        value_weights = np.linalg.solve(x.T @ x + 0.01 * np.eye(dimension), x.T @ returns)
        objective = float(np.minimum(unclipped, clipped).mean())
        diagnostics.append(
            {
                "objective": objective,
                "clip_fraction": float(np.mean(np.abs(ratio - 1) > 0.2)),
                "advantage_std": float(advantages.std()),
                "reward": float(np.mean(rewards)),
            }
        )
        rows.append((float(update), 0.0, float(np.mean(rewards))))
    np.savez(output / "policy.npz", weights=weights, sigma=sigma, value_weights=value_weights)
    reloaded = np.load(output / "policy.npz")
    change = float(np.linalg.norm(weights - initial))
    write_json(
        output / "policy-contract.json",
        {
            "algorithm": "linear-gaussian-PPO",
            "observation_dim": dimension - 1,
            "action_dim": action_dim,
            "action_transform": "tanh",
            "training_scope": "optimizer-smoke",
            "performance_verified": False,
            "seed": seed,
        },
    )
    return Experiment(
        rows,
        rows[-1][2] - rows[0][2],
        {
            "updates": diagnostics,
            "parameter_delta": change,
            "rollout_length": rollout_length,
            "algorithm": "PPO with GAE and clipped surrogate",
            "performance_verified": False,
            "reload_max_error": float(np.max(np.abs(x @ weights - x @ reloaded["weights"]))),
            "source": getattr(environment, "source", "repository pendulum"),
        },
        {
            "parameters_updated": change > 1e-8,
            "reload_exact": bool(np.array_equal(weights, reloaded["weights"])),
            "finite_policy": bool(np.isfinite(weights).all()),
        },
        environment.model,
        environment.data,
        ["policy.npz", "policy-contract.json"],
    )


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    observation: Any
    action: Any
    if identifier == "core-fr3-07":
        from pai_lab.lessons.physics import jacobian

        env = Reach(seed)
        observation = env.reset()
        transitions, rows = [], []
        initial = float(np.linalg.norm(env.target - env.data.site_xpos[0]))
        for i in range(samples):
            error = env.target - env.data.site_xpos[0]
            jac = jacobian(env.model, env.data)
            command = jac.T @ np.linalg.solve(jac @ jac.T + 0.001 * np.eye(3), error)
            action = np.arctanh(np.clip(command / 0.03 * variant, -0.9, 0.9))
            following, reward, terminated, truncated = env.step(action)
            transitions.append(
                {
                    "observation": observation.tolist(),
                    "action": action.tolist(),
                    "reward": reward,
                    "next_observation": following.tolist(),
                    "terminated": terminated,
                    "truncated": truncated,
                }
            )
            rows.append(
                (
                    float(env.data.time),
                    0.0,
                    float(np.linalg.norm(env.target - env.data.site_xpos[0])),
                )
            )
            observation = following
            if terminated or truncated:
                break
        write_json(output / "transitions.json", transitions)
        return Experiment(
            rows,
            rows[-1][2],
            {
                "source": env.source,
                "initial_distance_m": initial,
                "terminal_distance_m": rows[-1][2],
                "transitions": transitions,
                "observation_dimension": len(observation),
                "action_dimension": env.model.nu,
            },
            {"distance_reduced": rows[-1][2] < initial, "bounded_episode": len(rows) <= 64},
            env.model,
            env.data,
            ["transitions.json"],
        )
    if identifier in {"core-rl-01", "core-fr3-08"}:
        environment = Reach(seed) if identifier == "core-fr3-08" else Pendulum(seed)
        return ppo(environment, output, seed, samples, variant)
    if identifier == "core-data-01":
        model, data = pendulum()
        rng = np.random.default_rng(seed)
        records: list[dict[str, Any]] = []
        rows = []
        for episode in range(8):
            mujoco.mj_resetData(model, data)
            data.qpos[0] = rng.uniform(-0.6, 0.6)
            mujoco.mj_forward(model, data)
            for step in range(samples):
                observation = [float(data.qpos[0]), float(data.qvel[0])]
                action = float(
                    np.clip(-2.0 * variant * observation[0] - 0.6 * observation[1], -3, 3)
                )
                data.ctrl[0] = action
                for _ in range(10):
                    mujoco.mj_step(model, data)
                record = {
                    "episode": episode,
                    "step": step,
                    "time_s": float(data.time),
                    "observation": observation,
                    "action": [action],
                    "next_observation": [float(data.qpos[0]), float(data.qvel[0])],
                    "terminated": False,
                    "truncated": step == samples - 1,
                }
                records.append(record)
                rows.append((float(len(rows)), observation[0], float(data.qpos[0])))
        (output / "episode.jsonl").write_text("".join(json.dumps(r) + "\n" for r in records))
        return Experiment(
            rows,
            float(len(records)),
            {
                "episodes": 8,
                "transitions": len(records),
                "observation_units": ["rad", "rad/s"],
                "action_units": ["Nm"],
                "dt_s": 0.02,
                "controller": "clipped PD",
            },
            {
                "nonempty": len(records) == 8 * samples,
                "state_changes": any(r["observation"] != r["next_observation"] for r in records),
            },
            model,
            data,
            ["episode.jsonl"],
        )
    if identifier == "core-il-01":
        source = previous_run("core-data-01") / "episode.jsonl"
        records = [json.loads(line) for line in source.read_text().splitlines()]
        training = [r for r in records if r["episode"] < 6]
        heldout = [r for r in records if r["episode"] >= 6]
        x = np.array([r["observation"] + [1.0] for r in training])
        y = np.array([r["action"] for r in training])
        xv = np.array([r["observation"] + [1.0] for r in heldout])
        yv = np.array([r["action"] for r in heldout])
        weights = np.zeros((3, 1))
        rows = []
        for i in range(max(64, samples * 4)):
            loss = float(np.mean((x @ weights - y) ** 2))
            rows.append((float(i), 0.0, loss))
            weights -= 0.15 * variant * (2 * x.T @ (x @ weights - y) / len(x))
        np.savez(output / "policy.npz", weights=weights)
        error = float(np.mean((xv @ weights - yv) ** 2))
        reload_error = float(
            np.max(np.abs(xv @ weights - xv @ np.load(output / "policy.npz")["weights"]))
        )
        model, data = pendulum()
        return Experiment(
            rows,
            rows[0][2] - rows[-1][2],
            {
                "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "training_rows": len(x),
                "heldout_rows": len(xv),
                "heldout_mse": error,
                "weights": weights.tolist(),
                "reload_max_error": reload_error,
            },
            {
                "loss_decreased": rows[-1][2] < rows[0][2],
                "heldout_mse_below_0_1": error < 0.1,
                "reload_exact": reload_error == 0,
            },
            model,
            data,
            ["policy.npz"],
        )
    if identifier == "core-aloha-01":
        model, data, receipt = load("aloha")
        horizon = 16
        home = data.ctrl.copy()
        chunks, observations, rows = [], [], []
        for i in range(samples):
            chunk = np.tile(home, (horizon, 1))
            chunk[:, 0] += 0.05 * variant * np.sin(i * 0.05)
            observations.append(data.qpos[model.jnt_qposadr[model.actuator_trnid[:, 0]]].copy())
            chunks.append(chunk)
            data.ctrl[:] = chunk[0]
            for _ in range(10):
                mujoco.mj_step(model, data)
            rows.append((float(data.time), float(chunk[0, 0]), float(data.qpos[0])))
        np.savez(output / "act-batch.npz", observations=observations, actions=chunks)
        camera = render(output / "observation.png", model, data)
        return Experiment(
            rows,
            float(model.nu),
            {
                "source": receipt,
                "observation_shape": list(np.shape(observations)),
                "action_shape": list(np.shape(chunks)),
                "image_shape": camera["shape"],
                "chunk_horizon": horizon,
                "contract_only": True,
                "ACT_trained": False,
            },
            {
                "dual_arm_14_actions": model.nu == 14,
                "finite_states": bool(np.isfinite(observations).all()),
                "camera_nonempty": camera["std"] > 1,
            },
            model,
            data,
            ["act-batch.npz", "observation.png"],
        )
    if identifier == "core-vla-01":
        request = {
            "version": 1,
            "instruction": "reach the target",
            "observation": [0.0] * 7,
            "image": {"encoding": "fixture", "sha256": hashlib.sha256(b"mock-image").hexdigest()},
            "timestamp_s": 0.0,
            "timeout_s": 0.1,
        }
        wire = json.dumps(request).encode()
        decoded = json.loads(wire)
        response: dict[str, Any] = {
            "actions": [[float(x) * variant for x in decoded["observation"]]],
            "units": "rad",
            "command_sink": True,
            "mock": True,
        }
        rows = [(float(i), 0.0, float(x)) for i, x in enumerate(response["actions"][0])]
        return Experiment(
            rows,
            float(len(request) + len(response)),
            {"request": request, "response": response},
            {
                "schema_roundtrip": decoded == request,
                "bounded_actions": max(abs(r[2]) for r in rows) <= 1.0,
                "sink_only": response["command_sink"],
            },
        )
    raise ValueError(identifier)
