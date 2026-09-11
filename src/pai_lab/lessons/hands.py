"""Measured hand poses, contact forces, cross-hand retargeting and G1 replay."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import mujoco
import numpy as np
from scipy.optimize import least_squares

from pai_lab.catalog import ROOT
from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import inventory, load


def tips(model: Any, data: Any) -> np.ndarray:
    ids = [i for i in range(model.nsite) if "tip" in model.site(i).name]
    return np.asarray(data.site_xpos[ids]).copy()


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    model, data, receipt = load("g1" if identifier == "core-g1-01" else "wuji")
    info = {"source": receipt, **inventory(model)}
    if identifier == "core-g1-01":
        home = data.qpos.copy()
        # Prescribed model joint motion, not a learned walking policy.
        ids = np.flatnonzero(model.jnt_type == int(mujoco.mjtJoint.mjJNT_HINGE))
        addresses = model.jnt_qposadr[ids]
        states, rows = [], []
        for i, phase in enumerate(np.linspace(0.0, 2 * np.pi, samples)):
            data.qpos[:] = home
            data.qpos[addresses] += 0.08 * variant * np.sin(phase)
            data.qpos[addresses] = np.clip(
                data.qpos[addresses], model.jnt_range[ids, 0], model.jnt_range[ids, 1]
            )
            mujoco.mj_forward(model, data)
            states.append(data.qpos.copy())
            rows.append(
                (float(i) * 0.02, float(home[addresses[0]]), float(data.qpos[addresses[0]]))
            )
        np.savez(output / "motion.npz", qpos=states, dt=0.02, joint_names=info["joint_names"])
        saved = np.load(output / "motion.npz")
        replay = []
        for q in saved["qpos"]:
            data.qpos[:] = q
            mujoco.mj_forward(model, data)
            replay.append(data.qpos.copy())
        error = float(np.max(np.abs(np.array(replay) - np.array(states))))
        info.update(
            motion_source="prescribed bounded joint cycle evaluated on real G1 model",
            replay_max_error=error,
            loop_error=float(np.linalg.norm(states[0] - states[-1])),
        )
        return Experiment(
            rows,
            error,
            info,
            {"replay_exact": error == 0.0, "closed_cycle": info["loop_error"] < 1e-12},
            model,
            data,
            ["motion.npz"],
        )
    if identifier == "core-wuji-01":
        synergy = np.array(
            [0.3 if "abd" in model.joint(i).name else 0.6 for i in range(model.njnt)]
        )
        poses, rows = {}, []
        for i, (name, amplitude) in enumerate((("open", 0.0), ("half", 0.5), ("closed", 1.0))):
            data.qpos[:] = np.clip(
                synergy * amplitude * variant, model.jnt_range[:, 0], model.jnt_range[:, 1]
            )
            mujoco.mj_forward(model, data)
            poses[name] = {"qpos": data.qpos.tolist(), "tips_m": tips(model, data).tolist()}
            magnitude = float(np.linalg.norm(data.qpos))
            rows.append((float(i), magnitude, magnitude))
        info.update(poses=poses, synergy=synergy.tolist())
        return Experiment(
            rows,
            float(len(poses)),
            info,
            {"twenty_joints": model.njnt == 20, "five_tips": len(tips(model, data)) == 5},
            model,
            data,
        )
    if identifier == "core-wuji-02":
        spec = mujoco.MjSpec.from_file(
            str(ROOT / ".cache/assets/wuji-description/hand2/hand2_beta2/body/mjcf/right.xml")
        )
        tip = tips(model, data)[1]
        spec.worldbody.add_geom(
            name="stimulus",
            type=mujoco.mjtGeom.mjGEOM_SPHERE,
            size=[0.012 * variant, 0, 0],
            pos=tip,
            rgba=[0.9, 0.3, 0.1, 1],
        )
        model = spec.compile()
        data = mujoco.MjData(model)
        data.ctrl[:] = 0.0
        rows, contacts = [], []
        for _ in range(samples):
            mujoco.mj_step(model, data)
            force_sum = 0.0
            contact_rows = []
            for i in range(data.ncon):
                c = data.contact[i]
                if "stimulus" in {model.geom(int(c.geom1)).name, model.geom(int(c.geom2)).name}:
                    force = np.zeros(6)
                    mujoco.mj_contactForce(model, data, i, force)
                    force_sum += abs(force[0])
                    contact_rows.append(
                        {"position_world_m": c.pos.tolist(), "force_contact_N": force.tolist()}
                    )
            rows.append((float(data.time), 0.0, float(force_sum)))
            contacts.append(contact_rows)
        info.update(
            contacts=contacts,
            observation_type="virtual contact-force samples, not physical tactile sensor calibration",
        )
        return Experiment(
            rows,
            float(np.mean([r[2] for r in rows])),
            info,
            {"real_contact_force": max(r[2] for r in rows) > 0},
            model,
            data,
        )
    other, other_data, other_receipt = load("sharpa")
    info["comparison_model"] = {"source": other_receipt, **inventory(other)}
    if identifier == "core-dexterity-01":
        rows = [
            (float(i), float(a), float(b))
            for i, (a, b) in enumerate(
                zip(
                    (model.njnt, model.nu, len(tips(model, data))),
                    (other.njnt, other.nu, len(tips(other, other_data))),
                )
            )
        ]
        info["comparison_dimensions"] = ["joint_count", "actuator_count", "tip_count"]
        return Experiment(
            rows,
            float(min(model.njnt, other.njnt) / max(model.njnt, other.njnt)),
            info,
            {
                "two_models": receipt["model"] != other_receipt["model"],
                "five_tips_each": len(tips(model, data)) == len(tips(other, other_data)) == 5,
            },
            other,
            other_data,
        )
    if identifier == "core-dexterity-02":
        source_home = tips(model, data)
        target_home = tips(other, other_data)
        q0 = other_data.qpos.copy()
        rows, demonstrations = [], []
        for i, amplitude in enumerate(np.linspace(0, 0.5 * variant, min(samples, 32))):
            data.qpos[:] = np.clip(amplitude, model.jnt_range[:, 0], model.jnt_range[:, 1])
            mujoco.mj_forward(model, data)
            # Align hand axes using the rest-pose tip point clouds.
            u, _, vt = np.linalg.svd(
                (source_home - source_home.mean(0)).T @ (target_home - target_home.mean(0))
            )
            rotation = u @ np.diag([1, 1, np.linalg.det(u @ vt)]) @ vt
            target = target_home + (tips(model, data) - source_home) @ rotation

            def residual(q: np.ndarray, target: np.ndarray = target) -> np.ndarray:
                other_data.qpos[:] = q
                mujoco.mj_forward(other, other_data)
                return np.concatenate(
                    [(tips(other, other_data) - target).ravel(), 0.002 * (q - q0)]
                )

            initial_error = float(np.linalg.norm(residual(q0)))
            fit = least_squares(
                residual,
                np.clip(
                    other_data.qpos, other.jnt_range[:, 0] + 1e-6, other.jnt_range[:, 1] - 1e-6
                ),
                bounds=(other.jnt_range[:, 0] + 1e-7, other.jnt_range[:, 1] - 1e-7),
                max_nfev=25,
            )
            final = float(np.linalg.norm(residual(fit.x)))
            rows.append((float(i), initial_error, final))
            demonstrations.append(
                {
                    "source_qpos": data.qpos.tolist(),
                    "target_qpos": fit.x.tolist(),
                    "tip_error_m": final,
                }
            )
        np.savez(output / "retargeted-motion.npz", qpos=[d["target_qpos"] for d in demonstrations])
        info.update(
            demonstrations=demonstrations,
            objective="aligned fingertip displacement plus joint regularization",
        )
        return Experiment(
            rows,
            float(np.mean([r[2] for r in rows])),
            info,
            {
                "improves_mean_tip_error": bool(
                    np.mean([r[2] for r in rows]) <= np.mean([r[1] for r in rows]) + 1e-6
                )
            },
            other,
            other_data,
            ["retargeted-motion.npz"],
        )
    raise ValueError(identifier)
