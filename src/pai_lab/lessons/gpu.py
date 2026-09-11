"""MJLab training and evaluation using each pinned upstream's registered task."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.assets import bundles
from pai_lab.catalog import ROOT
from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.learning import previous_run
from pai_lab.local import local_root, write_json


def inputs(identifier: str) -> dict[str, Any]:
    path = local_root() / "stack-inputs" / f"{identifier}.json"
    if not path.exists():
        raise FileNotFoundError(f"prepare {path}; see setup/WS1_HANDOFF.md")
    return dict(json.loads(path.read_text()))


def pinned_source(bundle: str) -> Path:
    entry = bundles()[bundle]
    path = ROOT / ".cache/assets" / str(entry["destination"])
    if not path.exists():
        raise FileNotFoundError(f"pal assets fetch {bundle}")
    revision = subprocess.check_output(
        ["git", "-C", str(path), "rev-parse", "HEAD"], text=True
    ).strip()
    if revision != entry["revision"]:
        raise ValueError(f"{bundle}: revision differs from source manifest")
    return path


def environment(
    identifier: str, seed: int, output: Path, *, play: bool = False
) -> tuple[Any, Any, Any, str]:
    import torch

    if not torch.cuda.is_available():
        raise FileNotFoundError("CUDA arithmetic required; no CPU fallback for GPU lesson")
    os.environ["WANDB_MODE"] = "disabled"
    sys.dont_write_bytecode = True
    is_wuji = "wuji" in identifier
    source = pinned_source("wuji-mjlab" if is_wuji else "unitree-mjlab")
    if is_wuji:
        sys.path.insert(0, str(source / "src"))
        importlib.import_module("wuji_mjlab.tasks")
        from wuji_mjlab.utils.task_cfg_utils import prepare_task_cfgs

        task = "WujiHand_Reorient"
        env_cfg, agent_cfg = prepare_task_cfgs(task, [], play=play)
    else:
        sys.path.insert(0, str(source))
        importlib.import_module("src.tasks")
        from mjlab.tasks.registry import load_env_cfg, load_rl_cfg

        task = "Unitree-G1-Tracking-No-State-Estimation"
        env_cfg, agent_cfg = load_env_cfg(task, play=play), load_rl_cfg(task)
        settings = inputs("sim-g1-01")
        motion = Path(settings["motion_file"]).expanduser().resolve()
        if not motion.is_file():
            raise FileNotFoundError("prepared G1 reference motion file is missing")
        env_cfg.commands["motion"].motion_file = str(motion)
    env_cfg.scene.num_envs = 1 if play else 32
    env_cfg.seed, agent_cfg.seed = seed, seed
    agent_cfg.logger = "tensorboard"
    if hasattr(agent_cfg, "upload_model"):
        agent_cfg.upload_model = False
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import MjlabOnPolicyRunner, RslRlVecEnvWrapper
    from mjlab.tasks.registry import load_runner_cls

    raw_env = ManagerBasedRlEnv(cfg=env_cfg, device="cuda:0", render_mode="rgb_array")
    wrapped = RslRlVecEnvWrapper(raw_env, clip_actions=agent_cfg.clip_actions)
    runner_cls = load_runner_cls(task) or MjlabOnPolicyRunner
    runner = runner_cls(wrapped, asdict(agent_cfg), str(output / "training"), "cuda:0")
    return raw_env, wrapped, runner, task


def tensors(path: Path) -> dict[str, Any]:
    import torch

    raw = torch.load(path, map_location="cpu", weights_only=True)
    result = {}

    def collect(value: Any, prefix: str = "") -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                collect(item, prefix + "/" + str(key))
        elif torch.is_tensor(value) and value.is_floating_point():
            result[prefix] = value

    collect(raw)
    return result


def evaluate(
    raw: Any, wrapped: Any, runner: Any, samples: int, output: Path
) -> tuple[list[tuple[float, float, float]], float]:
    import torch
    from PIL import Image

    policy = runner.get_inference_policy(device="cuda:0")
    observation = wrapped.get_observations()
    rows = []
    actions = []
    with torch.inference_mode():
        for i in range(samples):
            action = policy(observation)
            observation, reward, _done, _extras = wrapped.step(action)
            rows.append((float(i), 0.0, float(reward.mean().cpu())))
            actions.append(action.cpu().numpy())
    pixels = raw.render()
    if pixels is None:
        raise RuntimeError("MJLab returned no rendered frame")
    pixels = np.asarray(pixels)
    Image.fromarray(pixels.astype(np.uint8)).save(output / "evaluation.png")
    np.savez(output / "evaluation-actions.npz", actions=np.array(actions))
    return rows, float(pixels.std())


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    raw, wrapped, runner, task = environment(identifier, seed, output)
    try:
        before, after = output / "initial.pt", output / "policy.pt"
        runner.save(str(before))
        runner.learn(
            num_learning_iterations=max(2, min(16, samples // 8)), init_at_random_ep_len=True
        )
        runner.save(str(after))
        old, new = tensors(before), tensors(after)
        changes = [
            float((new[k] - v).norm())
            for k, v in old.items()
            if k in new and new[k].shape == v.shape
        ]
        runner.load(str(after))
        rows, pixels_std = evaluate(raw, wrapped, runner, samples, output)
        delta = max(changes, default=0.0)
        payload = {
            "task": task,
            "parameter_delta": delta,
            "evaluation_rewards": [r[2] for r in rows],
            "policy_sha256": hashlib.sha256(after.read_bytes()).hexdigest(),
            "evaluation_frame_std": pixels_std,
            "performance_verified": False,
            "training_scope": "short optimizer and inference verification",
        }
        return Experiment(
            rows,
            float(np.mean([r[2] for r in rows])),
            payload,
            {
                "parameters_updated": delta > 0,
                "finite_rewards": bool(np.isfinite(rows).all()),
                "render_nonempty": pixels_std > 1.0,
            },
            files=["initial.pt", "policy.pt", "evaluation.png", "evaluation-actions.npz"],
        )
    finally:
        wrapped.close()


def candidate(
    identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0
) -> Experiment:
    if identifier == "sim-enlight-02":
        return enlight_contact(output, seed, samples, variant)
    source_run = previous_run("sim-wuji-01")
    checkpoint = source_run / "policy.pt"
    if not checkpoint.is_file():
        raise FileNotFoundError("Wuji training checkpoint is missing")
    raw, wrapped, runner, task = environment("sim-wuji-01", seed, output, play=True)
    try:
        runner.load(str(checkpoint))
        rows, pixels_std = evaluate(raw, wrapped, runner, samples, output)
        bundle = output / "candidate"
        bundle.mkdir()
        shutil.copyfile(checkpoint, bundle / "policy.pt")
        payload: dict[str, Any] = {
            "task": task,
            "policy_sha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
            "candidate_only": True,
            "hardware_compatible": False,
            "rollback": "command-sink",
            "mean_reward": float(np.mean([r[2] for r in rows])),
            "performance_verified": False,
        }
        write_json(bundle / "manifest.json", payload)
        return Experiment(
            rows,
            float(payload["mean_reward"]),
            payload,
            {
                "checkpoint_reloaded": True,
                "finite_rewards": bool(np.isfinite(rows).all()),
                "render_nonempty": pixels_std > 1.0,
            },
            files=["candidate"],
        )
    finally:
        wrapped.close()


def enlight_contact(output: Path, seed: int, samples: int, variant: float) -> Experiment:
    import mujoco
    import torch

    from pai_lab.lessons.models import load
    from pai_lab.lessons.physics import jacobian

    model, data, source = load("enlight", output)
    tip = data.site_xpos[0].copy()
    spec = mujoco.MjSpec.from_file(str(output / "enlight-draft.xml"))
    spec.body("link7").add_geom(
        name="probe",
        type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=[0.012, 0, 0],
        pos=[0, 0, 0.048],
        mass=0.01,
    )
    spec.worldbody.add_geom(
        name="table",
        type=mujoco.mjtGeom.mjGEOM_BOX,
        size=[0.1, 0.1, 0.01],
        pos=tip + [0, 0, -0.021],
    )
    model = spec.compile()
    data = mujoco.MjData(model)
    mujoco.mj_resetDataKeyframe(model, data, 0)
    mujoco.mj_forward(model, data)
    home = data.qpos.copy()
    rows, actions = [], []
    for i in range(samples):
        for _ in range(10):
            observation = np.concatenate(
                [
                    home - data.qpos,
                    data.qvel,
                    data.qfrc_bias,
                    jacobian(model, data).T @ np.array([0, 0, -2.0 * variant]),
                ]
            )
            x = torch.tensor(observation, device="cuda", dtype=torch.float64)
            torque = (80 * x[:7] - 12 * x[7:14] + x[14:21] + x[21:28]).cpu().numpy()
            data.ctrl[:] = np.clip(
                torque, model.actuator_ctrlrange[:, 0], model.actuator_ctrlrange[:, 1]
            )
            mujoco.mj_step(model, data)
        force = 0.0
        for j in range(data.ncon):
            c = data.contact[j]
            if {model.geom(int(c.geom1)).name, model.geom(int(c.geom2)).name} == {"probe", "table"}:
                vector = np.zeros(6)
                mujoco.mj_contactForce(model, data, j, vector)
                force += abs(vector[0])
        rows.append((float(data.time), 2.0 * variant, float(force)))
        actions.append(data.ctrl.copy())
    np.savez(output / "contact-actions.npz", actions=actions)
    payload: dict[str, Any] = {
        "source": source,
        "controller": "GPU PD + gravity + Jacobian force",
        "gains": {"kp": 80.0, "kd": 12.0},
        "candidate_only": True,
        "rollback": "command-sink",
        "hardware_compatible": False,
        "mean_normal_force_N": float(np.mean([r[2] for r in rows])),
    }
    write_json(output / "candidate-controller.json", payload)
    return Experiment(
        rows,
        float(payload["mean_normal_force_N"]),
        payload,
        {
            "contact_measured": max(r[2] for r in rows) > 0,
            "finite_control": bool(np.isfinite(actions).all()),
        },
        model,
        data,
        ["enlight-draft.xml", "contact-actions.npz", "candidate-controller.json"],
    )
