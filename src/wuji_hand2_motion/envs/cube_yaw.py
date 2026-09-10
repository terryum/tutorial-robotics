"""Contact-based cube yaw reorientation in the Wuji Hand 2 palm frame."""

from __future__ import annotations

from pathlib import Path
from typing import Any, ClassVar

import gymnasium as gym
import mujoco
import numpy as np
from gymnasium import spaces
from mujoco_ros2_core import MujocoPositionActuatorBackend

from wuji_hand2_motion.model import DESCRIPTION_ROOT, joint_names, model_path, prefix, validate_side

CUBE_HALF_SIZE = 0.020
CUBE_MASS = 0.050
CONTROL_DELTA_RAD = 0.05
PALM_GRAVITY = 2.0


def build_cube_scene(side: str, output: Path | None = None) -> Path:
    side = validate_side(side)
    output = output or (
        Path(__file__).resolve().parents[3] / ".cache/models" / f"cube_yaw_{side}.xml"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    spec = mujoco.MjSpec.from_file(str(model_path(side)))
    spec.compiler.meshdir = str(DESCRIPTION_ROOT / "meshes" / side)
    palm_side = -1.0 if side == "right" else 1.0
    spec.option.gravity = [0.0, -palm_side * PALM_GRAVITY, 0.0]
    cube = spec.worldbody.add_body(
        name="cube",
        pos=[0.0, palm_side * 0.030, -0.105],
        quat=[1.0, 0.0, 0.0, 0.0],
    )
    cube.add_freejoint(name="cube_freejoint")
    cube.add_geom(
        name="cube_geom",
        type=mujoco.mjtGeom.mjGEOM_BOX,
        size=[CUBE_HALF_SIZE] * 3,
        mass=CUBE_MASS,
        friction=[1.0, 0.01, 0.001],
        condim=3,
        rgba=[0.92, 0.35, 0.12, 1.0],
    )
    cube.add_site(
        name="cube_center",
        type=mujoco.mjtGeom.mjGEOM_SPHERE,
        size=[0.003, 0.0, 0.0],
        rgba=[1.0, 1.0, 1.0, 1.0],
    )
    output.write_text(spec.to_xml())
    return output


def pregrasp_pose(side: str) -> dict[str, float]:
    value = prefix(side)
    pose = dict.fromkeys(joint_names(side), 0.0)
    pose[f"{value}_thumb_cmc_flex"] = 0.24
    pose[f"{value}_thumb_cmc_abd"] = -0.36
    pose[f"{value}_thumb_mcp"] = 0.36
    pose[f"{value}_thumb_ip"] = 0.30
    for finger in ("index_finger", "middle_finger", "ring_finger", "pinky"):
        pose[f"{value}_{finger}_mcp_flex"] = 0.33
        pose[f"{value}_{finger}_pip"] = 0.48
        pose[f"{value}_{finger}_dip"] = 0.30
    return pose


class WujiHand2CubeYawEnv(gym.Env[np.ndarray, np.ndarray]):
    metadata: ClassVar[dict[str, list[str]]] = {"render_modes": []}

    def __init__(
        self,
        side: str = "right",
        *,
        episode_seconds: float = 10.0,
        frame_skip: int = 10,
    ) -> None:
        super().__init__()
        self.side = validate_side(side)
        self.scene_path = build_cube_scene(self.side)
        self.backend = MujocoPositionActuatorBackend(
            self.scene_path, joint_names(self.side), frame_skip=frame_skip
        )
        self.model = self.backend.model
        self.data = self.backend.data
        self.lower = self.backend.lower.copy()
        self.upper = self.backend.upper.copy()
        self.center = 0.5 * (self.lower + self.upper)
        self.half_range = 0.5 * (self.upper - self.lower)
        self.command = np.asarray(
            [pregrasp_pose(self.side)[name] for name in self.backend.controlled_joints],
            dtype=np.float64,
        )
        cube_joint = mujoco.mj_name2id(
            self.model, mujoco.mjtObj.mjOBJ_JOINT, "cube_freejoint"
        )
        self.cube_qpos = int(self.model.jnt_qposadr[cube_joint])
        self.cube_dof = int(self.model.jnt_dofadr[cube_joint])
        self.cube_body = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_BODY, "cube")
        self.cube_geom = mujoco.mj_name2id(self.model, mujoco.mjtObj.mjOBJ_GEOM, "cube_geom")
        self.nominal_cube_pos = self.model.qpos0[self.cube_qpos : self.cube_qpos + 3].copy()
        self.target_yaw = 0.0
        self.previous_action = np.zeros(20, dtype=np.float64)
        self.steps = 0
        self.success_steps = 0
        self.max_steps = max(1, round(episode_seconds / self.backend.control_dt))
        self.action_space = spaces.Box(-1.0, 1.0, shape=(20,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(71,), dtype=np.float32
        )

    @property
    def control_dt(self) -> float:
        return self.backend.control_dt

    def _cube_yaw(self) -> float:
        matrix = np.empty(9, dtype=np.float64)
        mujoco.mju_quat2Mat(matrix, self.data.qpos[self.cube_qpos + 3 : self.cube_qpos + 7])
        rotation = matrix.reshape(3, 3)
        return float(np.arctan2(rotation[0, 2], rotation[0, 0]))

    def _yaw_error(self) -> float:
        return float(np.arctan2(np.sin(self.target_yaw - self._cube_yaw()), np.cos(self.target_yaw - self._cube_yaw())))

    def _contact_count(self) -> int:
        count = 0
        for index in range(self.data.ncon):
            contact = self.data.contact[index]
            if self.cube_geom not in (contact.geom1, contact.geom2):
                continue
            other = contact.geom2 if contact.geom1 == self.cube_geom else contact.geom1
            body_id = int(self.model.geom_bodyid[other])
            body_name = mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_BODY, body_id) or ""
            if body_name != "cube":
                count += 1
        return count

    def _dropped(self) -> bool:
        position = self.data.qpos[self.cube_qpos : self.cube_qpos + 3]
        return bool(np.linalg.norm(position - self.nominal_cube_pos) > 0.08)

    def _observation(self) -> np.ndarray:
        state = self.backend.read_control_state()
        position = (state.positions - self.center) / self.half_range
        velocity = state.velocities / 5.0
        command = (self.command - self.center) / self.half_range
        cube_position = self.data.qpos[self.cube_qpos : self.cube_qpos + 3]
        relative_position = (cube_position - self.nominal_cube_pos) / 0.08
        error = self._yaw_error()
        cube_velocity = self.data.qvel[self.cube_dof : self.cube_dof + 6]
        observation = np.concatenate(
            (
                position,
                velocity,
                command,
                relative_position,
                (np.sin(error), np.cos(error)),
                cube_velocity[:3] / 1.0,
                cube_velocity[3:] / 10.0,
            )
        )
        return observation.astype(np.float32)

    def _info(self) -> dict[str, float]:
        return {
            "yaw_error_rad": abs(self._yaw_error()),
            "contact_count": float(self._contact_count()),
            "is_success": float(self.success_steps >= 25),
            "is_dropped": float(self._dropped()),
        }

    def reset(self, *, seed=None, options: dict[str, Any] | None = None):
        super().reset(seed=seed)
        del options
        grasp = pregrasp_pose(self.side)
        self.backend.reset(grasp)
        self.command = np.asarray(
            [grasp[name] for name in self.backend.controlled_joints], dtype=np.float64
        )
        jitter = self.np_random.uniform(-0.001, 0.001, size=3)
        self.data.qpos[self.cube_qpos : self.cube_qpos + 3] = self.nominal_cube_pos + jitter
        initial_yaw = float(self.np_random.uniform(-np.deg2rad(5.0), np.deg2rad(5.0)))
        self.data.qpos[self.cube_qpos + 3 : self.cube_qpos + 7] = (
            np.cos(initial_yaw / 2.0),
            0.0,
            np.sin(initial_yaw / 2.0),
            0.0,
        )
        self.data.qvel[self.cube_dof : self.cube_dof + 6] = 0.0
        magnitude = float(
            self.np_random.uniform(np.deg2rad(15.0), np.deg2rad(30.0))
        )
        self.target_yaw = magnitude * (-1.0 if self.np_random.random() < 0.5 else 1.0)
        self.previous_action[:] = 0.0
        self.steps = 0
        self.success_steps = 0
        mujoco.mj_forward(self.model, self.data)
        return self._observation(), self._info()

    def step(self, action: np.ndarray):
        action = np.clip(np.asarray(action, dtype=np.float64), -1.0, 1.0)
        self.command = np.clip(
            self.command + CONTROL_DELTA_RAD * action, self.lower, self.upper
        )
        self.backend.set_joint_targets(
            dict(zip(self.backend.controlled_joints, self.command))
        )
        self.backend.step()
        self.steps += 1

        error = abs(self._yaw_error())
        relative_position = (
            self.data.qpos[self.cube_qpos : self.cube_qpos + 3]
            - self.nominal_cube_pos
        )
        contacts = min(self._contact_count(), 3)
        reward = float(np.exp(-4.0 * error))
        reward -= 20.0 * float(np.dot(relative_position, relative_position))
        reward += 0.05 * contacts
        reward -= 0.001 * float(np.mean(np.square(action)))
        reward -= 0.002 * float(np.mean(np.square(action - self.previous_action)))
        self.previous_action[:] = action

        if error < np.deg2rad(10.0):
            self.success_steps += 1
        else:
            self.success_steps = 0
        success = self.success_steps >= 25
        dropped = self._dropped()
        if success:
            reward += 5.0
        if dropped:
            reward -= 5.0
        terminated = success or dropped
        truncated = self.steps >= self.max_steps
        return self._observation(), reward, terminated, truncated, self._info()

    def close(self) -> None:
        pass
