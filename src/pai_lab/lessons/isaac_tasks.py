"""PhysX runtime tasks; prepared on Mac, must be validated on the installed Isaac host.

MuJoCo is used to load pinned source metadata and generate the MJCF export only.
Every observation, Jacobian and control step below comes from PhysX.
"""

from contextvars import ContextVar
from pathlib import Path
from typing import Any

import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.local import write_json

TRAIN_REQUEST: ContextVar[dict[str, Any] | None] = ContextVar(
    "physx_training_request", default=None
)


def task_mode(identifier: str) -> str:
    if identifier in {"sim-fr3-02", "sim-enlight-04"}:
        return "bc"
    if identifier in {"sim-fr3-03", "sim-enlight-05"}:
        return "ppo"
    return "control"


def train_physx(model: str, output: Path, **request: Any) -> dict[str, Any]:
    algorithm = request["algorithm"]
    identifier = (
        ("sim-fr3-02" if algorithm == "bc" else "sim-fr3-03")
        if model == "fr3"
        else ("sim-enlight-04" if algorithm == "bc" else "sim-enlight-05")
    )
    token = TRAIN_REQUEST.set(request)
    try:
        experiment = run(identifier, output, request["seed"], 64)
        return experiment.payload
    finally:
        TRAIN_REQUEST.reset(token)


class IsaacArm:
    engine = "PhysX"

    def __init__(
        self,
        name: str,
        robot: Any,
        world: Any,
        tcp: Any,
        source: dict[str, Any],
        home: np.ndarray,
        seed: int,
    ):
        self.name, self.robot, self.world, self.link, self.source = name, robot, world, tcp, source
        names = [f"fr3_joint{i}" if name == "fr3" else f"joint{i}" for i in range(1, 8)]
        self.indices = np.array([robot.dof_names.index(n) for n in names])
        self.home = home
        self.rng = np.random.default_rng(seed)
        self.target = self.tcp()
        self.steps = self.hold = 0
        self.bounds = np.asarray(robot.get_dof_limits()).reshape(-1, 2)[self.indices]
        from isaacsim.core.version import get_version

        self.runtime_version = list(get_version())

    def tcp(self) -> np.ndarray:
        return np.asarray(self.link.get_world_pose()[0])

    def reset(self) -> np.ndarray:
        self.robot.set_joint_positions(self.home, joint_indices=self.indices)
        self.robot.set_joint_velocities(np.zeros(7), joint_indices=self.indices)
        for _ in range(10):
            self.world.step(render=True)
        self.target = self.tcp() + self.rng.uniform(-0.035, 0.035, 3)
        self.steps = self.hold = 0
        return self.observation()

    def observation(self) -> np.ndarray:
        return np.concatenate(
            [
                self.robot.get_joint_positions()[self.indices] - self.home,
                0.1 * self.robot.get_joint_velocities()[self.indices],
                10 * (self.target - self.tcp()),
            ]
        )

    def expert(self) -> np.ndarray:
        # PhysX articulation Jacobian; transform link-origin velocity to the imported TCP.
        from isaacsim.core.prims import SingleXFormPrim

        link_name = "fr3_link7" if self.name == "fr3" else "link7"
        view = self.robot._articulation_view
        body_index = self.robot.get_body_index(link_name)
        values = np.asarray(view.get_jacobians())[0]
        # Both supported arms have a fixed base, excluded from the Jacobian rows.
        jacobian = values[body_index - 1, :, self.indices].T
        if jacobian.shape != (6, 7) or not np.isfinite(jacobian).all():
            raise RuntimeError("PhysX Jacobian shape/frame validation required")
        import omni.usd

        stage = omni.usd.get_context().get_stage()
        links = [p for p in stage.Traverse() if p.GetName() == link_name]
        if len(links) != 1:
            raise RuntimeError("TCP parent link is ambiguous")
        link = SingleXFormPrim(prim_path=str(links[0].GetPath()), name="jacobian_origin")
        offset = self.tcp() - link.get_world_pose()[0]
        jac = jacobian[:3] + np.cross(jacobian[3:].T, offset).T
        delta = jac.T @ np.linalg.solve(jac @ jac.T + 0.001 * np.eye(3), self.target - self.tcp())
        return np.asarray(np.arctanh(np.clip(delta / 0.03, -0.9, 0.9)))

    def step(self, action: np.ndarray) -> tuple[np.ndarray, float, bool, bool]:
        from isaacsim.core.utils.types import ArticulationAction

        q = self.robot.get_joint_positions()[self.indices]
        command = np.clip(q + 0.03 * np.tanh(action), self.bounds[:, 0], self.bounds[:, 1])
        self.robot.apply_action(
            ArticulationAction(joint_positions=command, joint_indices=self.indices)
        )
        for _ in range(10):
            self.world.step(render=True)
        error = float(np.linalg.norm(self.target - self.tcp()))
        self.hold = self.hold + 1 if error <= 0.01 else 0
        self.steps += 1
        return (
            self.observation(),
            -error - 0.001 * float(np.sum(action**2)),
            self.hold >= 10,
            self.steps >= 160,
        )


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    from isaacsim import SimulationApp

    app = SimulationApp({"headless": True})
    try:
        import mujoco
        import omni.replicator.core as rep
        import omni.usd
        from isaacsim.core.api import World
        from isaacsim.core.api.articulations import Articulation
        from isaacsim.core.prims import SingleRigidPrim, SingleXFormPrim
        from isaacsim.core.utils.types import ArticulationAction
        from PIL import Image
        from pxr import UsdGeom, UsdPhysics

        from pai_lab.lessons.isaac_adapter import import_mjcf
        from pai_lab.lessons.models import load

        name = next(n for n in ("fr3", "enlight", "shadow", "stretch3") if n in identifier)
        model, data, source = load(name, output)
        # A flattened MJCF resolves includes; mesh paths remain absolute in the local generated export.
        xml = output / "source.xml"
        mujoco.mj_saveLastXML(str(xml), model)
        stage, root, adapter = import_mjcf(xml, output / "robot.usda", fix_base=name != "stretch3")
        omni.usd.get_context().open_stage(stage.GetRootLayer().realPath)
        stage = omni.usd.get_context().get_stage()
        scene = UsdPhysics.Scene.Define(stage, "/World/PhysicsScene")
        scene.CreateGravityDirectionAttr().Set((0.0, 0.0, -1.0))
        scene.CreateGravityMagnitudeAttr().Set(9.81)
        world = World(stage_units_in_meters=1.0, physics_dt=0.002, rendering_dt=0.02)
        robot = world.scene.add(Articulation(prim_path=root, name=name))
        world.reset()
        # Importing a model is insufficient: enforce joints, equality/coupling and free-base metadata.
        joint_names = [
            model.joint(i).name for i in range(model.njnt) if model.jnt_type[i] in (2, 3)
        ]
        missing = set(joint_names) - set(robot.dof_names)
        if missing:
            raise RuntimeError(f"PhysX missing joints: {sorted(missing)}")
        if model.neq and not any(
            "Mimic" in str(p.GetAppliedSchemas()) or "Tendon" in str(p.GetAppliedSchemas())
            for p in stage.Traverse()
        ):
            raise RuntimeError(
                "coupling parity unverified; imported equality constraints require review"
            )
        camera = rep.create.camera(position=(1.8, -1.8, 1.5), look_at=(0, 0, 0.5))
        rep.create.light(light_type="dome", intensity=1000.0)
        product = rep.create.render_product(camera, (480, 360))
        rgb = rep.AnnotatorRegistry.get_annotator("rgb")
        rgb.attach(product)
        rows = []
        files = ["robot.usda"]
        payload: dict[str, Any] = {
            "engine": "PhysX",
            "source": source,
            "adapter": adapter,
            "joint_names": robot.dof_names,
            "control_dt_s": 0.02,
            "model": name,
        }
        if name in {"fr3", "enlight"}:
            tcp_prims = [p for p in stage.Traverse() if p.GetName() == "attachment_site"]
            if len(tcp_prims) != 1:
                raise RuntimeError("TCP frame import not validated")
            tcp = SingleXFormPrim(prim_path=str(tcp_prims[0].GetPath()), name="tcp")
            env = IsaacArm(name, robot, world, tcp, source, data.qpos[:7].copy(), seed)
            link_name = "fr3_link7" if name == "fr3" else "link7"
            links = [p for p in stage.Traverse() if p.GetName() == link_name]
            if len(links) != 1:
                raise RuntimeError("contact sensor body identity ambiguous")
            contact_sensor = world.scene.add(
                SingleRigidPrim(
                    prim_path=str(links[0].GetPath()),
                    name="tcp_contact_sensor",
                    track_contact_forces=True,
                )
            )
            world.reset()
            if task_mode(identifier) in {"bc", "ppo"}:
                from pai_lab.training import train

                result = train(
                    env,
                    output,
                    **(
                        TRAIN_REQUEST.get()
                        or {
                            "algorithm": task_mode(identifier),
                            "seed": seed,
                            "epochs": max(4, samples // 4),
                            "learning_rate": 0.01 * variant,
                        }
                    ),
                )
                if result["status"] == "interrupted":
                    return Experiment(result["rows"], 0.0, result, {"checkpoint_saved": True})
                rows = result.pop("rows")
                payload.update(result)
                files.extend(["policy.npz", "evaluation.json", "training-contract.json"])
                if task_mode(identifier) == "bc":
                    files.append("demonstrations.json")
            else:
                env.reset()
                origin = data.site_xpos[model.site("attachment_site").id].copy()
                targets, joint_errors, reaction_forces, contact_force_norms = [], [], [], []
                count = max(160, samples * 4)
                for i in range(count):
                    phase = i / (count - 1)
                    if phase < 0.5:
                        q = env.home.copy()
                        q[0] += 0.06 * variant * np.sin(4 * np.pi * phase)
                        env.target = origin.copy()
                        robot.apply_action(
                            ArticulationAction(joint_positions=q, joint_indices=env.indices)
                        )
                        for _ in range(10):
                            world.step(render=True)
                    else:
                        angle = 4 * np.pi * (phase - 0.5)
                        env.target = origin + 0.012 * variant * np.array(
                            [np.sin(angle), 1 - np.cos(angle), 0]
                        )
                        action = env.expert()
                        q = robot.get_joint_positions()[env.indices] + 0.03 * np.tanh(action)
                        env.step(action)
                    targets.append(env.target.tolist())
                    joint_errors.append(
                        float(np.linalg.norm(q - robot.get_joint_positions()[env.indices]))
                    )
                    # Reaction forces include gravity; retain them separately from contact sensor evidence.
                    reaction_forces.append(np.asarray(robot.get_measured_joint_forces()).tolist())
                    contact_force_norms.append(
                        float(np.linalg.norm(contact_sensor.get_net_contact_forces(dt=0.002)))
                    )
                    rows.append(
                        ((i + 1) * 0.02, 0.0, float(np.linalg.norm(env.target - env.tcp())))
                    )
                payload.update(
                    tcp_errors_m=[r[2] for r in rows],
                    tcp_targets_m=targets,
                    joint_errors_rad=joint_errors,
                    joint_reaction_forces=reaction_forces,
                    contact_force_norms_N=contact_force_norms,
                    initial_q_rad=env.home.tolist(),
                    frame="world",
                )
                # Separate probe experiment: attach a small collision sphere to the TCP,
                # introduce a plane, and require measured PhysX contact forces.
                from isaacsim.core.objects import FixedCuboid

                probe = UsdGeom.Sphere.Define(stage, str(tcp_prims[0].GetPath()) + "/ContactProbe")
                probe.CreateRadiusAttr(0.012)
                UsdPhysics.CollisionAPI.Apply(probe.GetPrim())
                point = env.tcp().copy()
                world.scene.add(
                    FixedCuboid(
                        prim_path="/World/ProbePlane",
                        name="probe_plane",
                        position=point + np.array([0.0, 0.0, -0.021]),
                        scale=np.array([0.2, 0.2, 0.02]),
                    )
                )
                held = robot.get_joint_positions()[env.indices].copy()
                world.reset()
                robot.set_joint_positions(held, joint_indices=env.indices)
                robot.apply_action(
                    ArticulationAction(joint_positions=held, joint_indices=env.indices)
                )
                probe_forces = []
                for _ in range(80):
                    world.step(render=True)
                    probe_forces.append(
                        float(np.linalg.norm(contact_sensor.get_net_contact_forces(dt=0.002)))
                    )
                if not np.isfinite(probe_forces).all() or max(probe_forces) <= 0:
                    raise RuntimeError("PhysX probe contact not observed")
                payload["probe_contact_forces_N"] = probe_forces
        else:
            initial = robot.get_joint_positions().copy()
            commands, observed_states, base_poses, object_contact_forces = [], [], [], []
            hand_contact = None
            if name == "shadow":
                palms = [p for p in stage.Traverse() if p.GetName() == "rh_palm"]
                objects = [p for p in stage.Traverse() if p.GetName() == "object"]
                if len(palms) != 1 or len(objects) != 1:
                    raise RuntimeError("hand/object contact identity unverified")
                hand_contact = world.scene.add(
                    SingleRigidPrim(
                        prim_path=str(palms[0].GetPath()),
                        name="hand_object_contact",
                        track_contact_forces=True,
                        contact_filter_prim_paths=[str(objects[0].GetPath())],
                    )
                )
                world.reset()
            if name == "stretch3" and robot._articulation_view.is_physics_handle_valid() is False:
                raise RuntimeError("free-base articulation physics handle invalid")
            for i in range(max(240, samples * 4)):
                phase = i / (max(240, samples * 4) - 1)
                target = initial.copy()
                if name == "shadow":
                    ramp = (1 - np.cos(2 * np.pi * phase)) * 0.5
                    for index, joint in enumerate(robot.dof_names):
                        if "WRJ" not in joint:
                            target[index] = 0.7 * variant * ramp
                    robot.apply_action(ArticulationAction(joint_positions=target))
                else:
                    names = robot.dof_names
                    wheel_indices = np.array(
                        [names.index("joint_left_wheel"), names.index("joint_right_wheel")]
                    )
                    velocity = (
                        np.array([0.7, 0.7 if phase < 0.25 or phase > 0.75 else -0.7]) * variant
                    )
                    if 0.5 <= phase <= 0.75:
                        velocity[:] = 0
                    robot.apply_action(
                        ArticulationAction(joint_velocities=velocity, joint_indices=wheel_indices)
                    )
                    lift = names.index("joint_lift")
                    extension = [names.index(f"joint_arm_l{j}") for j in range(4)]
                    indices = np.array([lift] + extension)
                    group_targets = np.array(
                        [0.35 + 0.1 * np.sin(np.pi * phase)]
                        + [(0.08 + 0.1 * phase * variant) / 4] * 4
                    )
                    robot.apply_action(
                        ArticulationAction(joint_positions=group_targets, joint_indices=indices)
                    )
                for _ in range(10):
                    world.step(render=True)
                if hand_contact is not None:
                    object_contact_forces.append(
                        float(np.linalg.norm(hand_contact.get_contact_force_matrix(dt=0.002)))
                    )
                observed = robot.get_joint_positions()
                commands.append(target.tolist())
                observed_states.append(observed.tolist())
                base_poses.append(np.asarray(robot.get_world_pose()[0]).tolist())
                rows.append((i * 0.02, float(target[0]), float(observed[0])))
            if float(np.max(np.ptp(np.array(observed_states), axis=0))) <= 0.01:
                raise RuntimeError("imported articulation did not move under drive commands")
            if name == "shadow" and max(object_contact_forces, default=0) <= 0:
                raise RuntimeError("no measured Shadow/object contact")
            if (
                name == "stretch3"
                and np.linalg.norm(np.array(base_poses[-1]) - base_poses[0]) <= 0.005
            ):
                raise RuntimeError("mobile base did not move freely")
            for eq in range(model.neq):
                if model.eq_type[eq] != mujoco.mjtEq.mjEQ_JOINT:
                    continue
                j1, j2 = int(model.eq_obj1id[eq]), int(model.eq_obj2id[eq])
                if j2 < 0:
                    continue
                i1 = robot.dof_names.index(model.joint(j1).name)
                i2 = robot.dof_names.index(model.joint(j2).name)
                states = np.array(observed_states)
                expected = sum(
                    model.eq_data[eq, power] * states[:, i2] ** power for power in range(5)
                )
                if np.max(np.abs(states[:, i1] - expected)) > 0.05:
                    raise RuntimeError("PhysX dynamic joint coupling parity failed")
            payload.update(
                object_contact_forces_N=object_contact_forces,
                free_base_required=name == "stretch3",
                couplings_required=int(model.neq),
                commands=commands,
                joint_states=observed_states,
                base_positions_m=base_poses,
            )
        for _ in range(8):
            rep.orchestrator.step()
        pixels = np.asarray(rgb.get_data())
        Image.fromarray(pixels[..., :3].astype(np.uint8)).save(output / "isaac-frame.png")
        payload["pixel_std"] = float(pixels.std())
        write_json(output / "physx-observations.json", payload)
        return Experiment(
            rows,
            float(np.sqrt(np.mean(np.square([r[2] - r[1] for r in rows])))),
            payload,
            {
                "physx_observations": bool(np.isfinite(rows).all()),
                "rendered": float(pixels.std()) > 1,
            },
            files=files + ["physx-observations.json", "isaac-frame.png"],
        )
    finally:
        app.close()
