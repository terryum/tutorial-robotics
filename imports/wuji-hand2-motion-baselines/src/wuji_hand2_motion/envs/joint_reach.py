"""Twenty-joint target-reaching baseline."""

from __future__ import annotations

from typing import Any

import gymnasium as gym
from gymnasium import spaces
import numpy as np

from mujoco_ros2_core import MujocoPositionActuatorBackend

from wuji_hand2_motion.model import joint_names, model_path, validate_side


class WujiHand2JointReachEnv(gym.Env[np.ndarray, np.ndarray]):
    metadata = {"render_modes": []}

    def __init__(
        self,
        side: str = "right",
        *,
        episode_steps: int = 150,
        frame_skip: int = 10,
    ) -> None:
        super().__init__()
        self.side = validate_side(side)
        self.backend = MujocoPositionActuatorBackend(
            model_path(self.side), joint_names(self.side), frame_skip=frame_skip
        )
        self.model = self.backend.model
        self.data = self.backend.data
        self.episode_steps = episode_steps
        self.lower = self.backend.lower.copy()
        self.upper = self.backend.upper.copy()
        self.center = 0.5 * (self.lower + self.upper)
        self.half_range = 0.5 * (self.upper - self.lower)
        self.target = self.backend.home.copy()
        self.steps = 0
        self.action_space = spaces.Box(-1.0, 1.0, shape=(20,), dtype=np.float32)
        self.observation_space = spaces.Box(
            low=-np.inf, high=np.inf, shape=(60,), dtype=np.float32
        )

    @property
    def control_dt(self) -> float:
        return self.backend.control_dt

    def _observation(self) -> np.ndarray:
        state = self.backend.read_control_state()
        position = (state.positions - self.center) / self.half_range
        velocity = state.velocities / 5.0
        target = (self.target - self.center) / self.half_range
        return np.concatenate((position, velocity, target)).astype(np.float32)

    def _info(self) -> dict[str, float]:
        position = self.backend.read_control_state().positions
        rmse = float(np.sqrt(np.mean(np.square((position - self.target) / self.half_range))))
        return {"joint_error_rmse": rmse, "is_success": float(rmse < 0.10)}

    def reset(self, *, seed=None, options: dict[str, Any] | None = None):
        super().reset(seed=seed)
        del options
        initial = np.clip(
            self.backend.home + self.np_random.uniform(-0.08, 0.08, size=20) * self.half_range,
            self.lower,
            self.upper,
        )
        self.target = np.clip(
            self.backend.home + self.np_random.uniform(-0.55, 0.55, size=20) * self.half_range,
            self.lower,
            self.upper,
        )
        self.backend.reset(dict(zip(self.backend.controlled_joints, initial)))
        self.steps = 0
        return self._observation(), self._info()

    def step(self, action: np.ndarray):
        action = np.clip(np.asarray(action, dtype=np.float64), -1.0, 1.0)
        desired = self.center + 0.90 * action * self.half_range
        self.backend.set_joint_targets(dict(zip(self.backend.controlled_joints, desired)))
        self.backend.step()
        self.steps += 1
        position = self.backend.read_control_state().positions
        error = (position - self.target) / self.half_range
        reward = -float(np.mean(np.square(error))) - 0.001 * float(np.mean(np.square(action)))
        truncated = self.steps >= self.episode_steps
        return self._observation(), reward, False, truncated, self._info()

    def close(self) -> None:
        pass
