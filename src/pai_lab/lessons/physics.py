"""MuJoCo host, dynamics, kinematics, contact, and model experiments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from pai_lab.assets import check_sources
from pai_lab.catalog import ROOT
from pai_lab.host import detect_host
from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import enlight_fk, inventory, load, provenance

PENDULUM = """<mujoco model="teaching-pendulum">
<option timestep="0.002" integrator="RK4"><flag energy="enable"/></option>
<worldbody><light pos="0 -2 3"/><body name="bob" pos="0 0 1.2">
<joint name="hinge" axis="0 1 0" damping="0"/>
<geom type="capsule" fromto="0 0 0 0 0 -1" size="0.025" mass="1" rgba="0.2 0.5 0.9 1"/>
<site name="tip" pos="0 0 -1"/></body></worldbody>
<actuator><motor joint="hinge" gear="1" ctrllimited="true" ctrlrange="-3 3"/></actuator>
</mujoco>"""


def pendulum() -> tuple[Any, Any]:
    model = mujoco.MjModel.from_xml_string(PENDULUM)
    data = mujoco.MjData(model)
    data.qpos[0] = 0.35
    mujoco.mj_forward(model, data)
    return model, data


def jacobian(model: Any, data: Any, site: int = 0) -> np.ndarray:
    jac = np.zeros((3, model.nv))
    mujoco.mj_jacSite(model, data, jac, None, site)
    return jac


def inverse_kinematics(model: Any, data: Any, target: np.ndarray, steps: int = 100) -> list[float]:
    errors = []
    for _ in range(steps):
        mujoco.mj_forward(model, data)
        error = target - data.site_xpos[0]
        errors.append(float(np.linalg.norm(error)))
        jac = jacobian(model, data)
        dq = jac.T @ np.linalg.solve(jac @ jac.T + 1e-4 * np.eye(3), error)
        data.qpos[: model.nv] += np.clip(dq, -0.08, 0.08)
        data.qpos[: model.nv] = np.clip(
            data.qpos[: model.nv], model.jnt_range[:, 0], model.jnt_range[:, 1]
        )
    mujoco.mj_forward(model, data)
    return errors


def arm_control(
    model: Any, data: Any, count: int, gain: float, mode: str, damping: float | None = None
) -> tuple[list[tuple[float, float, float]], dict[str, Any]]:
    model.opt.disableflags |= int(mujoco.mjtDisableBit.mjDSBL_ACTUATION)
    kd = 2 * np.sqrt(gain) if damping is None else damping
    qhome = data.qpos.copy()
    target_q = qhome.copy()
    target_q[0] += 0.18
    target = data.site_xpos[0].copy() + np.array([0.03, 0.02, 0.01])
    initial = (
        float(np.linalg.norm(target - data.site_xpos[0]))
        if mode == "task"
        else float(np.linalg.norm(target_q - data.qpos))
    )
    rows, states, torques, velocities, control_rows = [], [], [], [], []
    for index in range(count):
        for _ in range(25):
            if mode == "task":
                jac = jacobian(model, data)
                mass = np.zeros((model.nv, model.nv))
                mujoco.mj_fullM(model, data, mass)
                inverse_mass = np.linalg.solve(mass, jac.T)
                operational_mass = np.linalg.inv(jac @ inverse_mass + 1e-4 * np.eye(3))
                force = operational_mass @ (
                    gain * (target - data.site_xpos[0]) - 2 * np.sqrt(gain) * (jac @ data.qvel)
                )
                torque = jac.T @ force + data.qfrc_bias - 2 * data.qvel
            else:
                torque = gain * (target_q - data.qpos) - kd * data.qvel
                if mode == "gravity":
                    torque += data.qfrc_bias
            data.qfrc_applied[:] = np.clip(
                torque, model.jnt_actfrcrange[:, 0], model.jnt_actfrcrange[:, 1]
            )
            # Control rows are pre-step values: every operand matches this torque.
            for j in range(model.nv):
                control_rows.append(
                    (
                        float(data.time),
                        model.joint(j).name,
                        float(target_q[j]),
                        float(data.qpos[j]),
                        float(data.qvel[j]),
                        float(torque[j]),
                        float(data.qfrc_applied[j]),
                    )
                )
            mujoco.mj_step(model, data)
        mujoco.mj_forward(model, data)
        error = (
            float(np.linalg.norm(target - data.site_xpos[0]))
            if mode == "task"
            else float(np.linalg.norm(target_q - data.qpos))
        )
        rows.append((float(data.time), 0.0, error))
        states.append(data.qpos.copy().tolist())
        velocities.append(data.qvel.copy().tolist())
        torques.append(data.qfrc_applied.copy().tolist())
    return rows, {
        "initial_error": initial,
        "final_error": rows[-1][2],
        "qpos": states,
        "qvel": velocities,
        "time_s": [row[0] for row in rows],
        "joint_names": [model.joint(j).name for j in range(model.njnt)],
        "target_qpos": target_q.tolist(),
        "kd": float(kd),
        "control_rows": control_rows,
        "torque_nm": torques,
        "gain": gain,
        "mode": mode,
        "commanded_joint_error": float(abs(target_q[0] - data.qpos[0])),
    }


def run(
    identifier: str,
    output: Path,
    seed: int,
    samples: int,
    variant: float = 1.0,
    parameters: dict[str, float] | None = None,
) -> Experiment:
    parameters = parameters or {}
    if identifier == "core-00":
        host: dict[str, Any] = detect_host().to_dict()
        status = host["capability_status"]
        rows = [
            (float(i), 1.0, float(value["state"] == "available"))
            for i, value in enumerate(status.values())
        ]
        return Experiment(
            rows,
            float(len(host["capabilities"])),
            host,
            {"python_3_12": "python-3.12" in host["capabilities"]},
        )
    if identifier == "core-02":
        manifest = json.loads((ROOT / "assets/sources.json").read_text())
        receipts = [
            provenance(name) for name in ("fr3", "wuji", "enlight", "g1", "sharpa", "aloha")
        ]
        rows = [
            (float(i), 1.0, float(len(item["revision"]) == 40)) for i, item in enumerate(receipts)
        ]
        return Experiment(
            rows,
            float(np.mean([r[2] for r in rows])),
            {"sources": manifest, "models": receipts},
            {"source_pins": not check_sources()},
        )
    if identifier == "core-01":
        model, data = pendulum()
        model.opt.timestep = parameters.get("timestep", model.opt.timestep * variant)
        initial_energy = float(data.energy.sum())
        rows, states = [], []
        for _ in range(samples):
            for _ in range(10):
                mujoco.mj_step(model, data)
            mujoco.mj_forward(model, data)
            rows.append((float(data.time), initial_energy, float(data.energy.sum())))
            states.append([float(data.time), float(data.qpos[0]), float(data.qvel[0])])
        drift = max(abs(row[2] - row[1]) for row in rows)
        return Experiment(
            rows,
            drift,
            {"state": states, "dt_s": float(model.opt.timestep)},
            {"energy_drift_below_1e_5_J": drift < 1e-5},
            model,
            data,
        )
    if identifier == "core-03":
        models, rows = {}, []
        for i, name in enumerate(("fr3", "wuji", "enlight", "g1", "sharpa", "aloha")):
            model, data, receipt = load(name, output)
            models[name] = {**inventory(model), "source": receipt}
            rows.append((float(i), float(model.nv), float(model.nv)))
        return Experiment(
            rows,
            float(sum(v["mass_kg"] > 0 for v in models.values()) / len(models)),
            models,
            {"all_models_loaded": len(models) == 6},
            model,
            data,
            ["enlight-draft.xml"],
        )
    name = "enlight" if "enlight" in identifier else "fr3"
    model, data, receipt = load(name, output)
    info = {**inventory(model), "source": receipt, "x_axis": "time_s"}
    files = ["enlight-draft.xml"] if name == "enlight" else []
    if identifier in {"core-04", "core-fr3-01", "core-enlight-01"}:
        rows = [(float(i), float(data.qpos[i]), float(data.qpos[i])) for i in range(model.nq)]
        info["frame_positions_m"] = data.xpos.tolist()
        return Experiment(
            rows,
            float(model.njnt if identifier != "core-enlight-01" else model.nbody),
            info,
            {"positive_mass": info["mass_kg"] > 0, "seven_joints": model.njnt == 7},
            model,
            data,
            files,
        )
    if identifier == "core-enlight-02":
        errors, rows = [], []
        rng = np.random.default_rng(seed)
        for i in range(samples):
            q = rng.uniform(-0.4, 0.4, size=7) * variant
            data.qpos[:] = q
            mujoco.mj_forward(model, data)
            error = float(np.linalg.norm(enlight_fk(q)[:3, 3] - data.site_xpos[0]))
            errors.append(error)
            rows.append((float(i), 0.0, error))
        info["fk_error_m"] = errors
        info["comparison"] = "independent vendor homogeneous transforms versus compiled MJCF"
        return Experiment(
            rows,
            max(errors),
            info,
            {"fk_error_below_1e_9_m": max(errors) < 1e-9},
            model,
            data,
            files,
        )
    if identifier == "core-fr3-04":
        analytic = jacobian(model, data)
        numeric = np.zeros_like(analytic)
        original = data.qpos.copy()
        epsilon = 1e-6 * variant
        for j in range(model.nv):
            data.qpos[:] = original
            data.qpos[j] += epsilon
            mujoco.mj_forward(model, data)
            plus = data.site_xpos[0].copy()
            data.qpos[j] -= 2 * epsilon
            mujoco.mj_forward(model, data)
            numeric[:, j] = (plus - data.site_xpos[0]) / (2 * epsilon)
        data.qpos[:] = original
        mujoco.mj_forward(model, data)
        target = data.site_xpos[0] + np.array([0.03, 0.02, 0.01])
        errors = inverse_kinematics(model, data, target)
        difference = float(np.max(np.abs(analytic - numeric)))
        info.update(
            analytic=analytic.tolist(),
            finite_difference=numeric.tolist(),
            jacobian_max_error=difference,
            target_m=target.tolist(),
            ik_errors_m=errors,
        )
        rows = [(float(i), 0.0, value) for i, value in enumerate(errors)]
        return Experiment(
            rows,
            errors[-1],
            info,
            {"jacobian_below_1e_6": difference < 1e-6, "ik_below_1mm": errors[-1] < 0.001},
            model,
            data,
        )
    if identifier == "core-fr3-03":
        uncompensated = arm_control(model, data, samples, 120.0 * variant, "pd")
        model, data, _ = load("fr3")
        rows, measured = arm_control(model, data, samples, 120.0 * variant, "gravity")
        info.update(measured, without_compensation_error=uncompensated[0][-1][2])
        return Experiment(
            rows,
            rows[-1][2],
            info,
            {"gravity_reduces_error": rows[-1][2] < uncompensated[0][-1][2]},
            model,
            data,
        )
    if identifier in {"core-fr3-02", "core-fr3-05", "core-fr3-07"}:
        mode = "pd" if identifier == "core-fr3-02" else "task"
        rows, measured = arm_control(
            model, data, samples, parameters.get("kp", 120.0 * variant), mode, parameters.get("kd")
        )
        info.update(measured)
        if identifier == "core-fr3-07":
            info.update(
                observation_dimension=17,
                action_dimension=7,
                reward=[-r[2] for r in rows],
                terminated=rows[-1][2] < 0.01,
                truncated=rows[-1][2] >= 0.01,
                horizon=samples,
            )
        return Experiment(
            rows,
            rows[-1][2],
            info,
            {
                "finite_state": bool(np.isfinite(data.qpos).all()),
                "bounded_error": rows[-1][2] < (0.5 if mode == "pd" else 0.04),
                "target_joint_tracks": measured["commanded_joint_error"] < 0.02
                if mode == "pd"
                else True,
            },
            model,
            data,
        )
    if identifier == "core-fr3-06":
        spec = mujoco.MjSpec.from_file(
            str(ROOT / ".cache/assets/mujoco-menagerie/franka_fr3/scene.xml")
        )
        tip = data.site_xpos[0].copy()
        spec.body("fr3_link7").add_geom(
            name="contact_probe",
            type=mujoco.mjtGeom.mjGEOM_SPHERE,
            size=[0.018, 0, 0],
            pos=[0, 0, 0.107],
            mass=0.02,
        )
        spec.worldbody.add_geom(
            name="contact_table",
            type=mujoco.mjtGeom.mjGEOM_BOX,
            size=[0.1, 0.1, 0.01],
            pos=tip + [0, 0, -0.026],
            friction=[0.6 * variant, 0.005, 0.0001],
        )
        model = spec.compile()
        data = mujoco.MjData(model)
        mujoco.mj_resetDataKeyframe(model, data, 0)
        mujoco.mj_forward(model, data)
        model.opt.disableflags |= int(mujoco.mjtDisableBit.mjDSBL_ACTUATION)
        home = data.qpos.copy()
        rows, contacts = [], []
        for _ in range(samples):
            for _ in range(10):
                data.qfrc_applied[:] = data.qfrc_bias + 150 * (home - data.qpos) - 15 * data.qvel
                data.qfrc_applied[:] += jacobian(model, data).T @ np.array([1.0, 0.0, -5.0])
                mujoco.mj_step(model, data)
            normal = 0.0
            for c in range(data.ncon):
                contact = data.contact[c]
                names = {model.geom(int(contact.geom1)).name, model.geom(int(contact.geom2)).name}
                if names == {"contact_probe", "contact_table"}:
                    force = np.zeros(6)
                    mujoco.mj_contactForce(model, data, c, force)
                    normal += abs(force[0])
            rows.append((float(data.time), 5.0, float(normal)))
            contacts.append(int(data.ncon))
        info.update(
            friction=0.6 * variant, contact_counts=contacts, normal_force_N=[r[2] for r in rows]
        )
        return Experiment(
            rows,
            float(np.mean([r[2] for r in rows])),
            info,
            {"actual_probe_contact": max(r[2] for r in rows) > 0},
            model,
            data,
        )
    raise ValueError(f"no physics experiment for {identifier}")
