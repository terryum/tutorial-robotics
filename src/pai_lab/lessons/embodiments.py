"""Shadow finger synergies/contact and Stretch wheel/arm coordination in MuJoCo."""

from pathlib import Path

import mujoco
import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import load


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    name = "shadow" if "shadow" in identifier else "stretch3"
    model, data, source = load(name, output)
    rows, states, velocities, contacts, commands = [], [], [], [], []
    if name == "stretch3":
        data.ctrl[model.actuator("lift").id] = 0.35
        data.ctrl[model.actuator("arm").id] = 0.08
        for _ in range(1500):
            mujoco.mj_step(model, data)
    initial = data.qpos.copy()
    reach_errors, tcp_positions = [], []
    reach_target = None
    reach_lift = reach_extension = None
    gripper_body = model.body("link_SG3_gripper_body").id if name == "stretch3" else None
    count = max(240, samples * 4)
    if name == "shadow":
        # An explicit object placed in the palm; derived model stays in the run.
        from xml.etree import ElementTree as ET

        from pai_lab.catalog import ROOT

        vendor = ROOT / ".cache/assets/menagerie-extended/shadow_hand/scene_right.xml"
        tree = ET.parse(vendor)
        root = tree.getroot()
        ET.SubElement(root, "compiler", meshdir=str(vendor.parent / "assets"))
        include = root.find("include")
        assert include is not None
        include.set("file", str(vendor.parent / "right_hand.xml"))
        world = root.find("worldbody")
        assert world is not None
        original_object = world.find("body[@name='object']")
        assert original_object is not None
        world.remove(original_object)
        point = data.site_xpos[model.site("grasp_site").id].copy()
        ET.SubElement(
            world,
            "geom",
            name="contact_object",
            type="sphere",
            pos=" ".join(map(str, point)),
            size="0.025",
            rgba="1 .3 .1 1",
        )
        path = output / "shadow-contact.xml"
        tree.write(path, encoding="unicode")
        model = mujoco.MjModel.from_xml_path(str(path))
        data = mujoco.MjData(model)
        initial = data.qpos.copy()
    for i in range(count):
        phase = i / (count - 1)
        if name == "shadow":
            # Wrist stays centered. First a single finger, then a full-hand close/open synergy.
            u = np.zeros(model.nu)
            ramp = (1 - np.cos(2 * np.pi * phase)) * 0.5
            indices = [2] if phase < 0.25 else list(range(2, model.nu))
            for j in indices:
                lo, hi = model.actuator_ctrlrange[j]
                u[j] = np.clip(ramp * hi * 0.7 * variant, lo, hi)
            data.ctrl[:] = u
        else:
            u = data.ctrl.copy()

            def set_control(actuator: str, value: float, controls: np.ndarray = u) -> None:
                index = model.actuator(actuator).id
                controls[index] = value

            # Forward, turn, arm, then combined base+arm. The free base is never an action vector.
            set_control("left_wheel_vel", 0.2 * variant if phase < 0.5 or phase > 0.75 else 0.0)
            set_control(
                "right_wheel_vel",
                (0.2 if phase < 0.25 or phase > 0.75 else -0.2 if phase < 0.5 else 0.0) * variant,
            )
            set_control("lift", 0.35 + 0.1 * np.sin(np.pi * phase))
            set_control("arm", 0.08 + 0.1 * phase * variant)
            if phase > 0.75:
                assert gripper_body is not None
                if reach_target is None:
                    data.ctrl[:2] = 0.0
                    for _ in range(1000):
                        mujoco.mj_step(model, data)
                    forward_axis = data.xmat[model.body("base_link").id].reshape(3, 3)[:, 0]
                    reach_target = (
                        data.xpos[gripper_body].copy()
                        + 0.04 * forward_axis
                        + np.array([0.0, 0.0, 0.02])
                    )
                    reach_lift = float(data.ctrl[model.actuator("lift").id])
                    reach_extension = float(data.ctrl[model.actuator("arm").id])
                error = reach_target - data.xpos[gripper_body]
                # Differential wheel correction for world x/y; lift handles vertical error.
                base = data.xmat[model.body("base_link").id].reshape(3, 3)
                heading = base[:2, 0]
                forward = float(error[:2] @ heading)
                turn = float(heading[0] * error[1] - heading[1] * error[0])
                set_control("left_wheel_vel", np.clip(6 * forward - 4 * turn, -0.2, 0.2))
                set_control("right_wheel_vel", np.clip(6 * forward + 4 * turn, -0.2, 0.2))
                assert reach_lift is not None and reach_extension is not None
                set_control("lift", np.clip(reach_lift + error[2], 0.2, 1.0))
                set_control("arm", reach_extension)
            data.ctrl[:] = u
        for _ in range(10):
            mujoco.mj_step(model, data)
        if name == "stretch3":
            assert gripper_body is not None
            tcp_positions.append(data.xpos[gripper_body].tolist())
            if reach_target is not None:
                reach_errors.append(float(np.linalg.norm(reach_target - data.xpos[gripper_body])))
        commands.append(u.tolist())
        states.append(data.qpos.tolist())
        velocities.append(data.qvel.tolist())
        if name == "shadow":
            object_id = model.geom("contact_object").id
            contacts.append(sum(object_id in (c.geom1, c.geom2) for c in data.contact[: data.ncon]))
        else:
            contacts.append(int(data.ncon))
        observed = (
            (reach_errors[-1] if reach_errors else float(data.xpos[gripper_body, 2]))
            if name == "stretch3"
            else float(np.linalg.norm(data.qpos - initial))
        )
        rows.append((float(data.time), 0.0, observed))
    payload = {
        "reach_target_m": reach_target.tolist() if reach_target is not None else None,
        "reach_errors_m": reach_errors,
        "tcp_positions_m": tcp_positions,
        "engine": "MuJoCo",
        "source": source,
        "qpos": states,
        "qvel": velocities,
        "time_s": [r[0] for r in rows],
        "actuator_names": [model.actuator(i).name for i in range(model.nu)],
        "commands": commands,
        "contact_counts": contacts,
        "nq": model.nq,
        "nu": model.nu,
        "groups": {"hand": [model.actuator(i).name for i in range(model.nu)]}
        if name == "shadow"
        else {
            "base": ["left_wheel_vel", "right_wheel_vel"],
            "arm": ["lift", "arm", "wrist_yaw", "wrist_pitch", "wrist_roll"],
            "gripper": ["gripper"],
        },
        "couplings": int(model.neq),
        "free_base": bool(np.any(model.jnt_type == mujoco.mjtJoint.mjJNT_FREE)),
    }
    return Experiment(
        rows,
        rows[-1][2],
        payload,
        {
            "finite_states": bool(np.isfinite(states).all()),
            "motion_observed": max(r[2] for r in rows) > 0.01,
            "contact_observed": max(contacts) > 0,
            "coordinated_reach_reduced": name != "stretch3" or reach_errors[-1] < reach_errors[0],
        },
        model,
        data,
    )
