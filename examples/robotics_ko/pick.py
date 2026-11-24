"""Enlight pick-and-place with a known pose or a calibrated CPU RGB-D measurement."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco
import numpy as np
from PIL import Image
from scipy.spatial.transform import Rotation

from pai_lab.lessons.models import enlight_parameters, enlight_xml, provenance

CUBE_HALF = 0.018  # m
TABLE_TOP = 0.025  # m
SOURCE = np.array([0.432, 0.087])
GOAL = np.array([0.403, -0.085])
DOWN = np.diag([-1.0, 1.0, -1.0])
WIDTH, HEIGHT = 320, 240
THRESHOLDS = {
    "reprojection_px": 1e-8,
    "table_depth_error_m": 1e-7,
    "object_error_m": 0.005,
    "lift_m": 0.065,
    "placement_error_m": 0.025,
    "placement_height_error_m": 0.005,
    "placement_speed_m_s": 0.015,
    "table_support_force_N": 0.2,
    "bilateral_lift_normal_force_N": 0.1,
    "minimum_bilateral_lift_steps": 25,
}


def add_scene(path: Path, friction: float) -> Path:
    tree = ET.parse(enlight_xml(path))
    root = tree.getroot()
    world = root.find("worldbody")
    actuators = root.find("actuator")
    flange = root.find(".//body[@name='link7']")
    attachment = flange.find("site[@name='attachment_site']")
    root.remove(root.find("keyframe"))  # initialize qpos explicitly after adding joints
    ET.SubElement(
        world,
        "geom",
        name="table",
        type="box",
        pos=".52 0 .0125",
        size=".20 .24 .0125",
        rgba=".25 .32 .40 1",
    )
    ET.SubElement(
        world,
        "site",
        name="goal",
        type="cylinder",
        pos=f"{GOAL[0]} {GOAL[1]} {TABLE_TOP + 0.0002}",
        size=".025 .0002",
        rgba=".15 .8 .35 .55",
    )
    ET.SubElement(world, "camera", name="rgbd", pos=".505 .095 .9", fovy="38")
    cube = ET.SubElement(
        world, "body", name="cube", pos=f"{SOURCE[0]} {SOURCE[1]} {TABLE_TOP + CUBE_HALF}"
    )
    ET.SubElement(cube, "freejoint", name="cube_pose")
    ET.SubElement(
        cube,
        "geom",
        name="object",
        type="box",
        size=f"{CUBE_HALF} " * 3,
        mass=".045",
        rgba=".9 .07 .04 1",
        friction=".7 .01 .002",
        solref=".008 1",
    )
    tool = ET.SubElement(flange, "body", name="tool", pos=attachment.attrib["pos"])
    ET.SubElement(
        tool,
        "geom",
        type="box",
        name="palm",
        pos="0 0 .009",
        size=".029 .043 .009",
        mass=".08",
        rgba=".32 .48 .64 1",
    )
    ET.SubElement(tool, "site", name="grasp", pos="0 0 .058")
    for sign, name in ((-1, "left"), (1, "right")):
        finger = ET.SubElement(tool, "body", name=name, pos=f"0 {sign * 0.034} .051")
        ET.SubElement(
            finger,
            "joint",
            name=f"{name}_slide",
            type="slide",
            axis=f"0 {-sign} 0",
            range="0 .019",
            damping="1",
        )
        ET.SubElement(
            finger,
            "geom",
            type="box",
            name=f"{name}_pad",
            size=".018 .008 .017",
            rgba=".32 .48 .64 1",
            mass=".025",
            friction=f"{friction} .02 .004",
            priority="1",
            solref=".008 1",
        )
        ET.SubElement(
            actuators,
            "position",
            name=f"{name}_servo",
            joint=f"{name}_slide",
            kp="700",
            ctrlrange="0 .019",
            forcerange="-12 12",
        )
    scene = path / "scene.xml"
    tree.write(scene, encoding="unicode")
    return scene


def rgbd_frame(model, data):
    """Use a pinhole and MuJoCo's first visible intersection for each pixel."""
    camera_id = model.camera("rgbd").id
    origin = data.cam_xpos[camera_id].copy()
    # MuJoCo camera coordinates are right/up/back; optical coordinates right/down/forward.
    rotation = data.cam_xmat[camera_id].reshape(3, 3) @ np.diag([1, -1, -1])
    f = HEIGHT / (2 * np.tan(np.deg2rad(model.cam_fovy[camera_id]) / 2))
    center = np.array([(WIDTH - 1) / 2, (HEIGHT - 1) / 2])
    u, v = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))
    pixels = np.column_stack((u.ravel(), v.ravel()))
    optical = np.column_stack(((pixels - center) / f, np.ones(len(pixels))))
    # The ray is intentionally unnormalized: its parameter is forward depth Z.
    rays = np.ascontiguousarray(optical @ rotation.T)
    geom_ids = np.empty(len(rays), dtype=np.int32)
    depth = np.empty(len(rays))
    mujoco.mj_multiRay(
        model,
        data,
        origin,
        rays.ravel(),
        None,
        True,
        -1,
        geom_ids,
        depth,
        None,
        len(rays),
        2.0,
    )
    rgb = np.zeros((len(rays), 3), dtype=np.uint8)
    visible = geom_ids >= 0
    rgb[visible] = np.round(255 * model.geom_rgba[geom_ids[visible], :3]).astype(np.uint8)
    return rgb, depth, pixels, optical, origin, rotation, f, center


def estimate(model, data, output: Path):
    rgb, depth, pixels, optical, origin, rotation, f, center = rgbd_frame(model, data)
    mask = (rgb[:, 0] > 160) & (rgb[:, 1] < 70) & (rgb[:, 2] < 70) & (depth > 0)
    if np.count_nonzero(mask) < 40:
        raise RuntimeError("insufficient red pixels with valid depth")
    camera_points = optical[mask] * depth[mask, None]
    points = origin + camera_points @ rotation.T
    # Select the top surface from all visible red faces using world height.
    top = points[points[:, 2] >= points[:, 2].max() - 0.001]
    target = (top.min(axis=0) + top.max(axis=0)) / 2
    target[2] -= CUBE_HALF
    optical_again = (points - origin) @ rotation
    reprojection = f * optical_again[:, :2] / optical_again[:, 2, None] + center
    doubled = 2 * camera_points
    same_pixels = f * doubled[:, :2] / doubled[:, 2, None] + center
    table_color = np.round(255 * model.geom("table").rgba[:3]).astype(np.uint8)
    table_mask = (rgb == table_color).all(axis=1) & (depth > 0)
    if not np.any(table_mask):
        raise RuntimeError("workbench not visible for depth calibration check")
    table_check = origin + (optical[table_mask] * depth[table_mask, None]) @ rotation.T
    # Crop to the flat top inset so table edge pixels cannot skew the check.
    interior = (np.abs(table_check[:, 0] - 0.52) < 0.17) & (np.abs(table_check[:, 1]) < 0.21)
    if not np.any(interior):
        raise RuntimeError("no workbench interior pixels for depth calibration check")
    Image.fromarray(rgb.reshape(HEIGHT, WIDTH, 3)).save(output / "pick-rgb.png")
    Image.fromarray((mask.reshape(HEIGHT, WIDTH) * 255).astype(np.uint8)).save(
        output / "pick-mask.png"
    )
    np.savez_compressed(
        output / "pick-camera.npz", depth_m=depth.reshape(HEIGHT, WIDTH), points_world_m=points
    )
    return target, {
        "mask_pixels": int(mask.sum()),
        "top_surface_pixels": len(top),
        "image_hw": [HEIGHT, WIDTH],
        "focal_length_px": float(f),
        "principal_point_px": center.tolist(),
        "camera_origin_world_m": origin.tolist(),
        "camera_to_world_rotation": rotation.tolist(),
        "object_estimate_m": target.tolist(),
        "camera_depth_m": float(np.median(depth[mask])),
        "monocular_scale_comparison": {
            "depth_scale": 2.0,
            "scaled_median_depth_m": float(np.median(doubled[:, 2])),
            "same_pixel_max_error_px": float(
                np.max(np.linalg.norm(same_pixels - pixels[mask], axis=1))
            ),
        },
        "reprojection_rmse_px": float(
            np.sqrt(np.mean(np.sum((reprojection - pixels[mask]) ** 2, axis=1)))
        ),
        "table_depth_error_m": float(np.max(np.abs(table_check[interior, 2] - TABLE_TOP))),
    }


def wanted_joints(model, ik_data, site: int, target: np.ndarray) -> np.ndarray:
    """Solve only on separate kinematics state; the simulated body advances via mj_step."""
    jac_p = np.zeros((3, model.nv))
    jac_r = np.zeros((3, model.nv))
    for _ in range(150):
        mujoco.mj_forward(model, ik_data)
        position_error = target - ik_data.site_xpos[site]
        orientation_error = Rotation.from_matrix(
            DOWN @ ik_data.site_xmat[site].reshape(3, 3).T
        ).as_rotvec()
        if np.linalg.norm(position_error) < 0.0002 and np.linalg.norm(orientation_error) < 0.002:
            return ik_data.qpos[:7].copy()
        mujoco.mj_jacSite(model, ik_data, jac_p, jac_r, site)
        jac = np.vstack((jac_p[:, :7], 0.18 * jac_r[:, :7]))
        error = np.concatenate((position_error, 0.18 * orientation_error))
        step = jac.T @ np.linalg.solve(jac @ jac.T + 0.0001 * np.eye(6), error)
        ik_data.qpos[:7] = np.clip(
            ik_data.qpos[:7] + np.clip(step, -0.07, 0.07),
            model.jnt_range[:7, 0],
            model.jnt_range[:7, 1],
        )
    raise RuntimeError(f"IK did not reach waypoint {target.tolist()}")


def simulate(model, target_mode: str, output: Path):
    data = mujoco.MjData(model)
    initial = enlight_parameters()["initial"]
    data.qpos[:7] = [initial[f"joint{i}"] for i in range(1, 8)]
    mujoco.mj_forward(model, data)
    cube = model.body("cube").id
    site = model.site("grasp").id
    cube_geom = model.geom("object").id
    pad_geoms = [model.geom(f"{name}_pad").id for name in ("left", "right")]
    table_geom = model.geom("table").id
    cube_dof = int(model.joint("cube_pose").dofadr.item())
    ik_data = mujoco.MjData(model)
    ik_data.qpos[:] = data.qpos
    inertia = np.zeros((model.nv, model.nv))
    q_goal = data.qpos[:7].copy()
    rows = []
    unilateral = 0
    bilateral_lift = 0
    peak_bilateral_force = 0.0
    unexpected_contacts = 0
    arm_bodies = {model.body(f"link{i}").id for i in range(1, 8)}
    robot_bodies = arm_bodies | {model.body(name).id for name in ("tool", "left", "right")}
    robot_geoms = {
        index for index in range(model.ngeom) if model.geom_bodyid[index] in robot_bodies
    }
    intended_grasps = [{cube_geom, geom} for geom in pad_geoms]
    force = np.zeros(6)

    def advance(phase, joints, finger_position, seconds):
        nonlocal q_goal, unilateral, bilateral_lift, peak_bilateral_force, unexpected_contacts
        start = q_goal
        count = round(seconds / model.opt.timestep)
        for index in range(count):
            fraction = (index + 1) / count
            s = 3 * fraction**2 - 2 * fraction**3  # smooth starts and stops
            q_desired = (1 - s) * start + s * joints
            mujoco.mj_fullM(model, data, inertia)
            acceleration = 380 * (q_desired - data.qpos[:7]) - 34 * data.qvel[:7]
            torques = data.qfrc_bias[:7] + inertia[:7, :7] @ acceleration
            limits = model.actuator_ctrlrange[:7]
            data.ctrl[:7] = np.clip(torques, limits[:, 0], limits[:, 1])
            data.ctrl[7:] = finger_position
            mujoco.mj_step(model, data)
            normal = np.zeros(2)
            for ci in range(data.ncon):
                contact = data.contact[ci]
                geoms = {int(contact.geom1), int(contact.geom2)}
                if geoms & robot_geoms and geoms not in intended_grasps:
                    unexpected_contacts += 1
                for fi, pair in enumerate(intended_grasps):
                    if pair == geoms:
                        mujoco.mj_contactForce(model, data, ci, force)
                        normal[fi] += abs(force[0])
            if np.any(normal > 0.1):
                unilateral += 1
            if phase in ("lift", "carry") and data.xpos[cube, 2] > TABLE_TOP + CUBE_HALF + 0.03:
                minimum_force = float(normal.min())
                peak_bilateral_force = max(peak_bilateral_force, minimum_force)
                if minimum_force >= THRESHOLDS["bilateral_lift_normal_force_N"]:
                    bilateral_lift += 1
            if index % 5 == 0 or index == count - 1:
                rows.append(
                    [phase, float(data.time), *data.site_xpos[site], *data.xpos[cube], *normal]
                )
        q_goal = joints

    advance("settle", q_goal, 0, 0.4)
    actual_start = data.xpos[cube].copy()
    perception = None
    if target_mode == "rgbd":
        target, perception = estimate(model, data, output)
        perception["object_error_m"] = float(np.linalg.norm(target - actual_start))
    else:
        target = np.r_[SOURCE, TABLE_TOP + CUBE_HALF]
    closed = 0.015
    release_height = TABLE_TOP + CUBE_HALF + 0.005
    for phase, xyz, opening, duration in (
        ("approach", target + [0, 0, 0.075], 0, 1.4),
        ("lower", target, 0, 1.0),
        ("close", target, closed, 0.6),
        ("lift", target + [0, 0, 0.085], closed, 1.2),
        ("carry", np.r_[GOAL, release_height + 0.08], closed, 1.4),
        ("place", np.r_[GOAL, release_height], closed, 1.2),
        ("release", np.r_[GOAL, release_height], 0, 0.55),
        ("retreat", np.r_[GOAL, release_height + 0.080], 0, 0.7),
        ("finish", np.r_[GOAL, release_height + 0.080], 0, 0.6),
    ):
        advance(phase, wanted_joints(model, ik_data, site, xyz), opening, duration)

    xyz_final = data.xpos[cube].copy()
    table_support = 0.0
    for ci in range(data.ncon):
        contact = data.contact[ci]
        if {contact.geom1, contact.geom2} == {cube_geom, table_geom}:
            mujoco.mj_contactForce(model, data, ci, force)
            table_support += abs(force[0])
    metrics = {
        "initial_object_m": actual_start.tolist(),
        "commanded_target_m": target.tolist(),
        "goal_xy_m": GOAL.tolist(),
        "final_object_m": xyz_final.tolist(),
        "lift_m": float(max(row[7] for row in rows) - actual_start[2]),
        "placement_error_m": float(np.linalg.norm(xyz_final[:2] - GOAL)),
        "placement_height_error_m": float(abs(xyz_final[2] - TABLE_TOP - CUBE_HALF)),
        "placement_speed_m_s": float(np.linalg.norm(data.qvel[cube_dof : cube_dof + 3])),
        "pad_contact_steps": unilateral,
        "bilateral_lift_steps": bilateral_lift,
        "peak_bilateral_normal_force_N": peak_bilateral_force,
        "final_table_support_force_N": table_support,
        "unexpected_robot_contact_records": unexpected_contacts,
    }
    metrics["passed"] = (
        metrics["lift_m"] >= THRESHOLDS["lift_m"]
        and metrics["placement_error_m"] < THRESHOLDS["placement_error_m"]
        and metrics["placement_height_error_m"] < THRESHOLDS["placement_height_error_m"]
        and metrics["placement_speed_m_s"] < THRESHOLDS["placement_speed_m_s"]
        and bilateral_lift >= THRESHOLDS["minimum_bilateral_lift_steps"]
        and table_support >= THRESHOLDS["table_support_force_N"]
        and unexpected_contacts == 0
    )
    return metrics, perception, rows


def write_figure(output: Path, known_rows, rgbd_rows):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (motion, forces) = plt.subplots(2, 1, figsize=(8, 5), sharex=True, layout="constrained")
    for label, rows in (("Known pose", known_rows), ("RGB-D", rgbd_rows)):
        values = np.asarray([row[1:] for row in rows])
        motion.plot(values[:, 0], values[:, 6] * 100, label=label)
    motion.set_ylabel("Cube height (cm)")
    motion.legend()
    forces.plot(values[:, 0], values[:, 7:9], label=["Left jaw", "Right jaw"])
    forces.set(xlabel="Simulation time (s)", ylabel="Normal force (N)")
    forces.legend()
    fig.savefig(output / "pick-lift.png", dpi=120)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pad-friction", type=float, default=1.3)
    args = parser.parse_args()
    if not np.isfinite(args.pad_friction) or args.pad_friction <= 0:
        parser.error("--pad-friction must be finite and positive")
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    source = provenance("enlight")
    model = mujoco.MjModel.from_xml_path(str(add_scene(output, args.pad_friction)))
    known, _, known_rows = simulate(model, "known", output)
    rgbd, perception, rgbd_rows = simulate(model, "rgbd", output)
    perception["passed"] = (
        perception["object_error_m"] < THRESHOLDS["object_error_m"]
        and perception["table_depth_error_m"] < THRESHOLDS["table_depth_error_m"]
        and perception["reprojection_rmse_px"] < THRESHOLDS["reprojection_px"]
    )
    report = {
        "source": source,
        "mujoco_version": mujoco.__version__,
        "physical_timestep_s": model.opt.timestep,
        "pad_friction": args.pad_friction,
        "known_pose": known,
        "rgbd": rgbd,
        "perception": perception,
        "thresholds": THRESHOLDS,
        "passed": known["passed"] and rgbd["passed"] and perception["passed"],
    }
    (output / "pick.json").write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")
    with (output / "pick-trace.csv").open("w", newline="") as stream:
        trace = csv.writer(stream)
        trace.writerow(
            (
                "mode",
                "phase",
                "time_s",
                "tcp_x_m",
                "tcp_y_m",
                "tcp_z_m",
                "cube_x_m",
                "cube_y_m",
                "cube_z_m",
                "left_N",
                "right_N",
            )
        )
        for mode, rows in (("known_pose", known_rows), ("rgbd", rgbd_rows)):
            trace.writerows((mode, *row) for row in rows)
    write_figure(output, known_rows, rgbd_rows)
    print(json.dumps(report, allow_nan=False))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
