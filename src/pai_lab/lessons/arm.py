"""Named-joint arm tasks shared by trajectory, demonstration and policy lessons."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import load


class Arm:
    def __init__(self, name: str, output: Path, seed: int = 7):
        self.runtime_version = mujoco.__version__
        self.name = name
        self.model, self.data, self.source = load(name, output)
        names = [f"fr3_joint{i}" if name == "fr3" else f"joint{i}" for i in range(1, 8)]
        self.joints = [self.model.joint(n).id for n in names]
        self.qadr = self.model.jnt_qposadr[self.joints]
        self.vadr = self.model.jnt_dofadr[self.joints]
        self.actuators = [
            next(i for i in range(self.model.nu) if self.model.actuator_trnid[i, 0] == j)
            for j in self.joints
        ]
        self.site = self.model.site("attachment_site").id
        self.home = self.data.qpos[self.qadr].copy()
        self.bounds = self.model.jnt_range[self.joints].copy()
        self.rng = np.random.default_rng(seed)
        self.target = self.tcp().copy()
        self.steps = 0
        self.hold = 0

    def tcp(self) -> np.ndarray:
        return np.asarray(self.data.site_xpos[self.site]).copy()

    def reset(self) -> np.ndarray:
        mujoco.mj_resetDataKeyframe(self.model, self.data, 0)
        mujoco.mj_forward(self.model, self.data)
        self.target = self.tcp() + self.rng.uniform(-0.035, 0.035, 3)
        self.steps = self.hold = 0
        return self.observation()

    def observation(self) -> np.ndarray:
        return np.concatenate(
            [
                self.data.qpos[self.qadr] - self.home,
                self.data.qvel[self.vadr] * 0.1,
                (self.target - self.tcp()) * 10,
            ]
        )

    def jacobian(self) -> np.ndarray:
        jac = np.zeros((3, self.model.nv))
        mujoco.mj_jacSite(self.model, self.data, jac, None, self.site)
        return jac[:, self.vadr]

    def expert(self) -> np.ndarray:
        jac = self.jacobian()
        delta = jac.T @ np.linalg.solve(jac @ jac.T + 0.001 * np.eye(3), self.target - self.tcp())
        return np.arctanh(np.clip(delta / 0.03, -0.9, 0.9))

    def command(self, target: np.ndarray) -> None:
        target = np.clip(target, self.bounds[:, 0], self.bounds[:, 1])
        for _ in range(10):
            if self.name == "enlight":
                inertia = np.zeros((self.model.nv, self.model.nv))
                mujoco.mj_fullM(self.model, self.data, inertia)
                acceleration = (
                    120 * (target - self.data.qpos[self.qadr]) - 22 * self.data.qvel[self.vadr]
                )
                torque = (
                    self.data.qfrc_bias[self.vadr]
                    + inertia[np.ix_(self.vadr, self.vadr)] @ acceleration
                )
                limits = self.model.actuator_ctrlrange[self.actuators]
                self.data.ctrl[self.actuators] = np.clip(torque, limits[:, 0], limits[:, 1])
            else:
                self.data.ctrl[self.actuators] = target
            mujoco.mj_step(self.model, self.data)

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool]:
        self.command(self.data.qpos[self.qadr] + 0.03 * np.tanh(action))
        error = float(np.linalg.norm(self.target - self.tcp()))
        self.steps += 1
        self.hold = self.hold + 1 if error <= 0.01 else 0
        return (
            self.observation(),
            -error - 0.001 * float(np.sum(action**2)),
            self.hold >= 10,
            self.steps >= 160,
        )


def evaluate(env: Any, weights: np.ndarray, seed: int = 10007) -> dict[str, Any]:
    """Independent targets; ten consecutive control steps within 10 mm, 16/20 gate."""
    env.rng = np.random.default_rng(seed)
    episodes = []
    for episode in range(20):
        observation = env.reset()
        distances = []
        for _ in range(160):
            action = np.append(np.clip(observation, -5, 5), 1) @ weights
            observation, _, success, truncated = env.step(action)
            distances.append(float(np.linalg.norm(env.target - env.tcp())))
            if success or truncated:
                break
        episodes.append(
            {
                "episode": episode,
                "target_m": env.target.tolist(),
                "errors_m": distances,
                "success": bool(success),
            }
        )
    successes = sum(e["success"] for e in episodes)
    return {
        "seed": seed,
        "episodes": episodes,
        "successes": successes,
        "performance_verified": successes >= 16,
        "tolerance_m": 0.01,
        "hold_steps": 10,
        "required_successes": 16,
        "hardware_tolerance": False,
    }


def demonstrations(env: Any, episodes: int = 30) -> list[dict[str, Any]]:
    records = []
    for episode in range(episodes):
        observation = env.reset()
        for step in range(160):
            action = env.expert()
            following, _, success, truncated = env.step(action)
            records.append(
                {
                    "episode": episode,
                    "step": step,
                    "observation": observation.tolist(),
                    "action": action.tolist(),
                    "next_observation": following.tolist(),
                    "split": "train" if episode < 20 else "validation" if episode < 25 else "test",
                }
            )
            observation = following
            if success or truncated:
                break
    return records


def trajectory(name: str, output: Path, seed: int, samples: int, variant: float) -> Experiment:
    env = Arm(name, output, seed)
    origin = env.tcp()
    rows, states, velocities, targets, joint_errors, contacts, tcp_targets = (
        [],
        [],
        [],
        [],
        [],
        [],
        [],
    )
    # First half exercises a named joint, second half tracks a Cartesian circle using damped IK.
    contact_force_norms = []
    count = max(160, samples * 4)
    for i in range(count):
        phase = i / (count - 1)
        if phase < 0.5:
            q = env.home.copy()
            q[0] += 0.06 * variant * np.sin(4 * np.pi * phase)
            target = origin.copy()
        else:
            angle = 4 * np.pi * (phase - 0.5)
            target = origin + 0.012 * variant * np.array([np.sin(angle), 1 - np.cos(angle), 0])
            jac = env.jacobian()
            dq = jac.T @ np.linalg.solve(jac @ jac.T + 0.001 * np.eye(3), target - env.tcp())
            q = env.data.qpos[env.qadr] + np.clip(dq, -0.02, 0.02)
        env.command(q)
        joint_errors.append(float(np.linalg.norm(q - env.data.qpos[env.qadr])))
        targets.append(q.tolist())
        tcp_targets.append(target.tolist())
        rows.append((float(env.data.time), 0.0, float(np.linalg.norm(target - env.tcp()))))
        states.append(env.data.qpos.tolist())
        velocities.append(env.data.qvel.tolist())
        contacts.append(int(env.data.ncon))
        normal_force = 0.0
        for contact_index in range(env.data.ncon):
            force = np.zeros(6)
            mujoco.mj_contactForce(env.model, env.data, contact_index, force)
            normal_force += abs(float(force[0]))
        contact_force_norms.append(normal_force)
    tcp_rmse = float(np.sqrt(np.mean(np.square([r[2] for r in rows[count // 2 :]]))))
    payload = {
        "source": env.source,
        "engine": "MuJoCo",
        "joint_names": [env.model.joint(j).name for j in env.joints],
        "joint_targets_rad": targets,
        "joint_errors_rad": joint_errors,
        "tcp_targets_m": tcp_targets,
        "qpos": states,
        "qvel": velocities,
        "time_s": [r[0] for r in rows],
        "tcp_rmse_m": tcp_rmse,
        "control_dt_s": 10 * float(env.model.opt.timestep),
        "contact_counts": contacts,
        "contact_force_norms_N": contact_force_norms,
        "frame": "world",
        "initial_q_rad": env.home.tolist(),
    }
    return Experiment(
        rows,
        tcp_rmse,
        payload,
        {
            "finite": bool(np.isfinite(states).all()),
            "tcp_tracking": tcp_rmse < 0.02,
            "joint_motion": float(np.ptp(np.array(states)[:, env.qadr[0]])) > 0.01,
        },
        env.model,
        env.data,
    )


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    name = "enlight" if "enlight" in identifier else "fr3"
    if identifier in {"core-fr3-09", "core-enlight-03"}:
        return trajectory(name, output, seed, samples, variant)
    from pai_lab.training import train

    algorithm = "ppo" if identifier == "core-enlight-05" else "bc"
    env = Arm(name, output, seed)
    result = train(
        env,
        output,
        algorithm=algorithm,
        seed=seed,
        epochs=max(4, min(32, samples // 4)),
        learning_rate=0.01 * variant,
    )
    if result["status"] == "interrupted":
        raise KeyboardInterrupt("training checkpoint saved at update boundary")
    from pai_lab.local import write_json

    write_json(
        output / "candidate.json",
        {
            "model": name,
            "source": env.source,
            "algorithm": algorithm,
            "candidate_ready": result["performance_verified"],
            "hardware_compatible": False,
            "policy": "policy.npz",
            "evaluation": "evaluation.json",
            "cross_model_transfer": False,
        },
    )
    return Experiment(
        result["rows"],
        float(result["evaluation"]["successes"]),
        result,
        {"finite_policy": result["finite_policy"], "independent_evaluation": True},
        env.model,
        env.data,
        ["policy.npz", "evaluation.json", "training-contract.json", "candidate.json"]
        + (["demonstrations.json"] if algorithm == "bc" else []),
    )
