"""Optional real ACT comparison on the pinned public ALOHA model.

No private embodiment imports. This small known joint-target task measures
training mechanics and saved-policy rollout, not manipulation performance.
"""

from __future__ import annotations

import hashlib
import time
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from pai_lab.lessons.models import load
from pai_lab.local import write_json


def run(output: Path, *, steps: int, samples: int, seed: int, device: str) -> dict[str, Any]:
    import torch
    from lerobot.configs.types import FeatureType, PolicyFeature
    from lerobot.datasets.lerobot_dataset import LeRobotDataset
    from lerobot.policies.act.configuration_act import ACTConfig
    from lerobot.policies.act.modeling_act import ACTPolicy

    output.mkdir(parents=True, exist_ok=False)
    if device == "cuda" and not torch.cuda.is_available():
        raise ImportError("CUDA unavailable")
    model, data, source = load("aloha")
    model.opt.timestep = 0.002
    joints = model.actuator_trnid[:, 0].astype(int)
    addresses = model.jnt_qposadr[joints]
    names = [model.joint(int(j)).name for j in joints]
    units = ["m" if model.jnt_type[j] == mujoco.mjtJoint.mjJNT_SLIDE else "rad" for j in joints]
    home = data.qpos.copy()
    initial_ctrl = data.ctrl.copy()
    features = {
        "observation.state": {"dtype": "float32", "shape": (14,), "names": names},
        "action": {"dtype": "float32", "shape": (14,), "names": names},
        "observation.images.sim": {
            "dtype": "image",
            "shape": (64, 64, 3),
            "names": ["height", "width", "channels"],
        },
    }
    dataset = LeRobotDataset.create(
        "local/aloha-act-comparison",
        fps=50,
        features=features,
        root=output / "dataset",
        use_videos=False,
        video_backend="pyav",
    )

    def pixels(renderer: Any) -> np.ndarray:
        camera = mujoco.MjvCamera()
        mujoco.mjv_defaultFreeCamera(model, camera)
        renderer.update_scene(data, camera=camera)
        return np.asarray(renderer.render()).copy()

    with mujoco.Renderer(model, height=64, width=64) as renderer:
        for episode in range(3):
            mujoco.mj_resetData(model, data)
            data.qpos[:] = home
            data.ctrl[:] = initial_ctrl
            mujoco.mj_forward(model, data)
            for i in range(samples):
                target = home[addresses].copy()
                target[[0, 7]] += 0.01 * (episode + 1) * (i + 1) / samples
                dataset.add_frame(
                    {
                        "observation.state": data.qpos[addresses].astype(np.float32),
                        "observation.images.sim": pixels(renderer),
                        "action": target.astype(np.float32),
                        "task": "small bimanual joint target",
                    }
                )
                data.ctrl[:] = target
                for _ in range(10):
                    mujoco.mj_step(model, data)
                mujoco.mj_forward(model, data)
            dataset.save_episode()
    dataset.finalize()
    train_data = LeRobotDataset(
        "local/aloha-act-comparison",
        root=output / "dataset",
        episodes=[0, 1],
        delta_timestamps={"action": [i / 50 for i in range(16)]},
        video_backend="pyav",
    )
    torch.manual_seed(seed)
    config = ACTConfig(
        input_features={
            "observation.state": PolicyFeature(type=FeatureType.STATE, shape=(14,)),
            "observation.images.sim": PolicyFeature(type=FeatureType.VISUAL, shape=(3, 64, 64)),
        },
        output_features={"action": PolicyFeature(type=FeatureType.ACTION, shape=(14,))},
        device=device,
        chunk_size=16,
        n_action_steps=16,
        pretrained_backbone_weights=None,
        dim_model=32,
        n_heads=4,
        dim_feedforward=64,
        n_encoder_layers=1,
        n_decoder_layers=1,
        n_vae_encoder_layers=1,
        latent_dim=8,
        dropout=0.0,
    )
    policy = ACTPolicy(config).to(device)
    optimizer = torch.optim.AdamW(policy.parameters(), lr=1e-4)
    original = [p.detach().clone() for p in policy.parameters()]
    loader = torch.utils.data.DataLoader(train_data, batch_size=2, shuffle=True)
    iterator = iter(loader)
    if device == "cuda":
        torch.cuda.reset_peak_memory_stats()
    started = time.perf_counter()
    losses = []
    for i in range(steps):
        try:
            batch = next(iterator)
        except StopIteration:
            iterator = iter(loader)
            batch = next(iterator)
        batch = {
            key: value.to(device) for key, value in batch.items() if isinstance(value, torch.Tensor)
        }
        loss, _ = policy(batch)
        if not torch.isfinite(loss):
            raise RuntimeError("non-finite ALOHA loss")
        optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        optimizer.step()
        losses.append(float(loss.detach()))
    if device == "cuda":
        torch.cuda.synchronize()
    elapsed = time.perf_counter() - started
    delta = sum(
        float((p.detach() - q).abs().sum())
        for p, q in zip(policy.parameters(), original, strict=True)
    )
    if not delta > 0:
        raise RuntimeError("ALOHA parameters unchanged")
    policy.save_pretrained(output / "checkpoint")
    reloaded = ACTPolicy.from_pretrained(output / "checkpoint", local_files_only=True).to(device)
    with torch.no_grad():
        reload_error = float(
            (policy.predict_action_chunk(batch) - reloaded.predict_action_chunk(batch)).abs().max()
        )
    if reload_error > 1e-6:
        raise RuntimeError("ALOHA reload mismatch")
    mujoco.mj_resetData(model, data)
    data.qpos[:] = home
    data.ctrl[:] = initial_ctrl
    mujoco.mj_forward(model, data)
    reloaded.reset()
    target = home[addresses].copy()
    target[[0, 7]] += 0.03
    with mujoco.Renderer(model, height=64, width=64) as renderer:
        for _ in range(samples):
            obs = {
                "observation.state": torch.from_numpy(data.qpos[addresses].astype(np.float32))
                .unsqueeze(0)
                .to(device),
                "observation.images.sim": torch.from_numpy(pixels(renderer))
                .permute(2, 0, 1)
                .float()
                .unsqueeze(0)
                .to(device)
                / 255,
            }
            with torch.no_grad():
                action = reloaded.select_action(obs).cpu().numpy()[0]
            if not np.isfinite(action).all():
                raise RuntimeError("non-finite ALOHA action")
            data.ctrl[:] = np.clip(action, model.jnt_range[joints, 0], model.jnt_range[joints, 1])
            for _ in range(10):
                mujoco.mj_step(model, data)
            mujoco.mj_forward(model, data)
    error = np.abs(data.qpos[addresses] - target)
    report = {
        "model": source,
        "joint_order": names,
        "units_by_joint": units,
        "device": device,
        "steps": steps,
        "losses": losses,
        "parameter_l1_change": delta,
        "reload_error": reload_error,
        "steps_per_second": steps / elapsed,
        "peak_cuda_memory_bytes": torch.cuda.max_memory_allocated() if device == "cuda" else None,
        "joint_errors": error.tolist(),
        "episode_count": 1,
        "success_count": int(np.all(error < 0.02)),
        "checkpoint_hashes": {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in (output / "checkpoint").iterdir()
            if p.is_file()
        },
        "performance_verified": False,
        "comparison_limit": "Different tasks, units and morphology; compare mechanics, not rank robots.",
    }
    write_json(output / "training-results.json", report)
    return report
