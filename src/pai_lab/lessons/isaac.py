"""Isaac Sim 5.1/6.0 URDF import, camera data and measured engine comparison."""

from __future__ import annotations

from pathlib import Path
from xml.etree import ElementTree as ET

import mujoco
import numpy as np

from pai_lab.catalog import ROOT
from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import load
from pai_lab.local import write_json


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    from isaacsim import SimulationApp

    # Version-specific import is selected by the available documented importer API.
    app = SimulationApp({"headless": True})
    try:
        import omni.replicator.core as rep
        import omni.usd
        from isaacsim.core.api import World
        from isaacsim.core.api.articulations import Articulation
        from isaacsim.core.utils.extensions import enable_extension
        from PIL import Image

        enable_extension("isaacsim.asset.importer.urdf")
        model, data, source = load("wuji")
        vendor = ROOT / ".cache/assets/wuji-description/hand2/hand2_beta2/body/urdf/right.urdf"
        tree = ET.parse(vendor)
        for mesh in tree.findall(".//mesh"):
            mesh.set("filename", str((vendor.parent / mesh.attrib["filename"]).resolve()))
        urdf = output / "wuji-local.urdf"
        tree.write(urdf, encoding="unicode")
        from pai_lab.lessons.isaac_adapter import import_urdf

        imported, prim, adapter = import_urdf(urdf, output / "imported.usda", fix_base=True)
        omni.usd.get_context().open_stage(imported.GetRootLayer().realPath)
        world = World(stage_units_in_meters=1.0, physics_dt=0.002, rendering_dt=0.02)
        robot = world.scene.add(Articulation(prim_path=prim, name="wuji"))
        world.reset()
        names = [model.joint(i).name for i in range(model.njnt)]
        mapping = [robot.dof_names.index(name) for name in names]
        camera = rep.create.camera(position=(0.35, -0.45, 0.3), look_at=(0, 0, 0))
        rep.create.light(
            light_type="dome", intensity=1000.0 * (variant if identifier != "sim-cross-01" else 1.0)
        )
        product = rep.create.render_product(camera, (480, 360))
        rgb = rep.AnnotatorRegistry.get_annotator("rgb")
        rgb.attach(product)
        depth = rep.AnnotatorRegistry.get_annotator("distance_to_camera")
        depth.attach(product)
        rows, states = [], []
        robot.set_joint_positions(data.qpos.copy(), joint_indices=np.array(mapping))
        robot.set_joint_velocities(np.zeros(model.nv), joint_indices=np.array(mapping))
        controller = robot.get_articulation_controller()
        if identifier == "sim-cross-01":
            controller.switch_control_mode("effort")
            model.opt.disableflags |= int(mujoco.mjtDisableBit.mjDSBL_ACTUATION)
        for i in range(samples):
            if identifier == "sim-cross-01":
                torque = np.full(model.nv, 0.002 * variant * np.sin(i * 0.1))
                data.qfrc_applied[:] = torque
                robot.set_joint_efforts(torque, joint_indices=np.array(mapping))
                mujoco.mj_step(model, data)
                world.step(render=True)
            else:
                q = np.full(model.nq, 0.1 * np.sin(i * 0.1))
                data.qpos[:] = q
                mujoco.mj_forward(model, data)
                robot.set_joint_positions(q, joint_indices=np.array(mapping))
                world.step(render=True)
            observed = robot.get_joint_positions()[mapping]
            rows.append((float(i) * 0.002, float(data.qpos[0]), float(observed[0])))
            states.append({"mujoco_qpos": data.qpos.tolist(), "isaac_qpos": observed.tolist()})
        for _ in range(8):
            rep.orchestrator.step()
        pixels = np.asarray(rgb.get_data())
        distance = np.asarray(depth.get_data())
        Image.fromarray(pixels[..., :3].astype(np.uint8)).save(output / "isaac-frame.png")
        np.save(output / "camera-depth.npy", distance)
        omni.usd.get_context().get_stage().GetRootLayer().Export(str(output / "imported.usda"))
        error = float(
            np.sqrt(np.mean([(np.array(s["mujoco_qpos"]) - s["isaac_qpos"]) ** 2 for s in states]))
        )
        payload = {
            "source": source,
            "import_adapter": adapter,
            "joint_order": names,
            "isaac_joint_indices": mapping,
            "states": states,
            "state_rmse_rad": error,
            "image_shape": list(pixels.shape),
            "pixel_std": float(pixels.std()),
            "depth_finite_count": int(np.isfinite(distance).sum()),
            "dt_s": 0.002,
            "comparison": "matched efforts and initial states"
            if identifier == "sim-cross-01"
            else "asset and camera",
        }
        write_json(output / "isaac-observations.json", payload)
        return Experiment(
            rows,
            error if identifier == "sim-cross-01" else float(model.njnt),
            payload,
            {
                "all_twenty_joints": len(mapping) == 20,
                "camera_nonempty": float(pixels.std()) > 1.0,
                "depth_nonempty": bool(np.isfinite(distance).any()),
                "state_parity": error < 0.15 if identifier == "sim-cross-01" else True,
            },
            files=[
                "wuji-local.urdf",
                "isaac-frame.png",
                "camera-depth.npy",
                "imported.usda",
                "isaac-observations.json",
            ],
        )
    finally:
        app.close()
