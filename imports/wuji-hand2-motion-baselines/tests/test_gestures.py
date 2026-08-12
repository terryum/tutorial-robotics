import pytest

from mujoco_ros2_core import MujocoPositionActuatorBackend, validate_trajectory

from wuji_hand2_motion import GESTURE_NAMES, gesture_pose, gesture_trajectory
from wuji_hand2_motion.model import joint_names, model_path


@pytest.mark.parametrize("side", ["left", "right"])
def test_gestures_validate_for_pinned_model(side: str) -> None:
    backend = MujocoPositionActuatorBackend(model_path(side), joint_names(side))
    for name in GESTURE_NAMES:
        backend.set_joint_targets(gesture_pose(side, name))
    trajectory = gesture_trajectory(side)
    report = validate_trajectory(
        trajectory,
        known_joints=set(backend.joint_names),
        position_limits=backend.position_limits,
        max_velocity=3.0,
    )
    assert report.is_valid, report.errors
    assert report.sample_count == 376
