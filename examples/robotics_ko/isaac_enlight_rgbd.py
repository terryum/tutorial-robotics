"""Capture the same pinned Enlight home pose and camera in MuJoCo or Isaac Sim."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

import numpy as np
from PIL import Image

from pai_lab.local import write_json

WIDTH, HEIGHT = 320, 240
FOV_Y_DEG = 38.0
CAMERA_POSITION_M = (0.505, 0.095, 0.9)
CAMERA_NAME = "book-rgbd"
JOINT_NAMES = tuple(f"joint{i}" for i in range(1, 8))
TCP_ATOL_M = 0.002
JOINT_ATOL_RAD = 1e-5


def vector_text(values: tuple[float, ...]) -> str:
    return " ".join(str(value) for value in values)


def camera_contract() -> dict[str, Any]:
    focal_px = float(HEIGHT / (2 * np.tan(np.deg2rad(FOV_Y_DEG / 2))))
    return {
        "width_px": WIDTH,
        "height_px": HEIGHT,
        "fov_y_deg": FOV_Y_DEG,
        "position_world_m": CAMERA_POSITION_M,
        "optical_axes_in_world": ["+X", "-Y", "-Z"],
        "intrinsics_fx_fy_cx_cy_px": (focal_px, focal_px, (WIDTH - 1) / 2, (HEIGHT - 1) / 2),
        "depth_units": "m",
        "depth_convention": "axial-in-optical-frame",
    }


def capture_mujoco(
    model: Any, data: Any, directory: Path
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str]:
    import mujoco

    tree = ET.parse(directory / "enlight-draft.xml")
    world = tree.find("worldbody")
    if world is None:
        raise ValueError("generated Enlight model has no worldbody")
    ET.SubElement(
        world,
        "camera",
        name=CAMERA_NAME,
        pos=vector_text(CAMERA_POSITION_M),
        quat="1 0 0 0",
        fovy=str(FOV_Y_DEG),
    )
    camera_path = directory / "camera-scene.xml"
    tree.write(camera_path, encoding="unicode")
    scene = mujoco.MjModel.from_xml_path(str(camera_path))
    state = mujoco.MjData(scene)
    state.qpos[:] = data.qpos
    mujoco.mj_forward(scene, state)
    with mujoco.Renderer(scene, height=HEIGHT, width=WIDTH) as renderer:
        renderer.update_scene(state, camera=CAMERA_NAME)
        pixels = renderer.render().copy()
        renderer.enable_depth_rendering()
        depth = renderer.render().copy()
    tcp = state.site_xpos[model.site("attachment_site").id].copy()
    return pixels, depth, state.qpos.copy(), tcp, mujoco.__version__


def capture_physx(
    model: Any, data: Any, directory: Path
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, str]:
    from isaacsim import SimulationApp

    app = SimulationApp({"headless": True})
    try:
        import mujoco
        import omni.replicator.core as rep
        import omni.usd
        from isaacsim.core.api import World
        from isaacsim.core.api.articulations import Articulation
        from isaacsim.core.prims import SingleXFormPrim
        from isaacsim.core.version import get_version
        from pxr import Gf, UsdGeom

        from pai_lab.lessons.isaac_adapter import import_mjcf

        mjcf = directory / "source.xml"
        mujoco.mj_saveLastXML(str(mjcf), model)
        imported, root, _ = import_mjcf(mjcf, directory / "source.usda", fix_base=True)
        context = omni.usd.get_context()
        context.open_stage(imported.GetRootLayer().realPath)
        stage = context.get_stage()
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(stage, 1.0)
        world = World(stage_units_in_meters=1.0, physics_dt=0.002, rendering_dt=0.02)
        robot = world.scene.add(Articulation(prim_path=root, name="enlight"))
        world.reset()
        indices = np.array([robot.dof_names.index(name) for name in JOINT_NAMES])
        robot.set_joint_positions(data.qpos.copy(), joint_indices=indices)
        robot.set_joint_velocities(np.zeros(len(indices)), joint_indices=indices)
        tcp_prims = [prim for prim in stage.Traverse() if prim.GetName() == "attachment_site"]
        if len(tcp_prims) != 1:
            raise RuntimeError("TCP frame import not validated")
        tcp_prim = SingleXFormPrim(prim_path=str(tcp_prims[0].GetPath()), name="book_tcp")

        # USD pinhole cameras look along local -Z; their +Y points up in the image.
        # A translate-only camera thus shares the MuJoCo optical axes exactly.
        path = "/World/BookRGBDCamera"
        camera = UsdGeom.Camera.Define(stage, path)
        camera.AddTranslateOp().Set(Gf.Vec3d(*CAMERA_POSITION_M))
        focal = 20.0
        aperture_y = float(2 * focal * np.tan(np.deg2rad(FOV_Y_DEG / 2)))
        camera.CreateFocalLengthAttr(focal)
        camera.CreateVerticalApertureAttr(aperture_y)
        camera.CreateHorizontalApertureAttr(aperture_y * WIDTH / HEIGHT)
        camera.CreateClippingRangeAttr(Gf.Vec2f(0.01, 5.0))
        rep.create.light(light_type="dome", intensity=1000.0)
        render_product = rep.create.render_product(path, (WIDTH, HEIGHT))
        rgb = rep.AnnotatorRegistry.get_annotator("rgb")
        depth = rep.AnnotatorRegistry.get_annotator("distance_to_image_plane")
        rgb.attach(render_product)
        depth.attach(render_product)
        world.render()
        for _ in range(8):
            rep.orchestrator.step(delta_time=0.0, pause_timeline=True)
        pixels = np.array(rgb.get_data())
        depths = np.array(depth.get_data())
        joints = np.asarray(robot.get_joint_positions())[indices]
        tcp = np.asarray(tcp_prim.get_world_pose()[0])
        return pixels, depths, joints, tcp, str(get_version())
    finally:
        app.close()


def inspect_rgbd(
    pixels: np.ndarray, depth: np.ndarray
) -> tuple[np.ndarray, np.ndarray, dict[str, Any]]:
    if depth.shape == (HEIGHT, WIDTH, 1):
        depth = depth[..., 0]
    if (
        pixels.shape not in ((HEIGHT, WIDTH, 3), (HEIGHT, WIDTH, 4))
        or pixels.dtype != np.uint8
        or depth.shape != (HEIGHT, WIDTH)
    ):
        raise ValueError(
            f"unexpected RGB-D shapes or dtype: {pixels.shape}, {depth.shape}, {pixels.dtype}"
        )
    rgb = pixels[..., :3]
    valid = depth[np.isfinite(depth) & (depth > 0.0)]
    if valid.size < 100 or float(np.ptp(valid)) < 1e-4:
        raise ValueError("axial depth has too few positive finite pixels or no spatial variation")
    spatial_std = float(rgb.std(axis=(0, 1)).mean())
    if spatial_std <= 1.0:
        raise ValueError("RGB has no meaningful spatial variation")
    return (
        rgb,
        depth,
        {
            "rgb_shape": rgb.shape,
            "depth_shape": depth.shape,
            "rgb_spatial_std": spatial_std,
            "finite_positive_depth_pixels": int(valid.size),
            "depth_min_m": float(valid.min()),
            "depth_median_m": float(np.median(valid)),
            "depth_max_m": float(valid.max()),
        },
    )


def run(engine: str, directory: Path) -> dict[str, Any]:
    from pai_lab.lessons.models import load

    directory.mkdir(parents=True)
    model, baseline, source = load("enlight", directory)
    capture = capture_mujoco if engine == "mujoco" else capture_physx
    pixels, depth, joints, tcp, version = capture(model, baseline, directory)
    rgb, depth, image = inspect_rgbd(pixels, depth)
    expected_joints = baseline.qpos
    expected_tcp = baseline.site_xpos[model.site("attachment_site").id]
    joint_error = float(np.max(np.abs(joints - expected_joints)))
    tcp_error = float(np.linalg.norm(tcp - expected_tcp))
    if (
        not np.isfinite([joint_error, tcp_error]).all()
        or joint_error > JOINT_ATOL_RAD
        or tcp_error > TCP_ATOL_M
    ):
        raise ValueError(f"home pose mismatch: joint max {joint_error:g} rad, TCP {tcp_error:g} m")
    Image.fromarray(rgb).save(directory / "rgb.png")
    np.save(directory / "depth.npy", depth, allow_pickle=False)
    hashes = {
        filename: hashlib.sha256((directory / filename).read_bytes()).hexdigest()
        for filename in ("rgb.png", "depth.npy")
    }
    receipt = {
        "schema_version": 1,
        "engine": engine,
        "version": version,
        "source": source,
        "camera": camera_contract(),
        "joint_names": JOINT_NAMES,
        "initial_q_rad": expected_joints.tolist(),
        "measured_q_rad": joints.tolist(),
        "measured_tcp_world_m": tcp.tolist(),
        "home_joint_max_error_rad": joint_error,
        "home_tcp_error_m": tcp_error,
        "sha256": hashes,
        **image,
    }
    write_json(directory / "rgbd.json", receipt)
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", required=True, choices=("mujoco", "physx"))
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    receipt = run(args.engine, args.output_dir)
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
