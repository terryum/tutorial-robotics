"""Enlight-only wrist pose IK for the MuJoCo Arm; no gripper or hardware API."""

from __future__ import annotations

from typing import Any

import numpy as np
from scipy.spatial.transform import Rotation

from pai_lab.teleop import HandInput


def wrist_target(arm: Any, pose: tuple[float, ...]) -> Any:
    import mujoco

    HandInput("left", pose, (), (), True, "calibrated", "none").validate("left")
    jp, jr = np.zeros((3, arm.model.nv)), np.zeros((3, arm.model.nv))
    mujoco.mj_jacSite(arm.model, arm.data, jp, jr, arm.site)
    current = Rotation.from_matrix(arm.data.site_xmat[arm.site].reshape(3, 3))
    error = np.r_[
        np.asarray(pose[:3]) - arm.tcp(), (Rotation.from_quat(pose[3:]) * current.inv()).as_rotvec()
    ]
    jac = np.vstack([jp[:, arm.vadr], jr[:, arm.vadr]])
    delta = jac.T @ np.linalg.solve(jac @ jac.T + 0.001 * np.eye(6), error)
    return np.clip(
        arm.data.qpos[arm.qadr] + np.clip(delta, -0.02, 0.02), arm.bounds[:, 0], arm.bounds[:, 1]
    )
