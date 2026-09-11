from wuji_hand2_motion.gestures import GESTURE_NAMES, gesture_pose, gesture_trajectory
from wuji_hand2_setup.model import (
    DESCRIPTION_ROOT,
    MODEL_COMMIT,
    MODEL_RELEASE,
    ROS_DESCRIPTION_PACKAGE,
    USD_FILENAME,
    fingertip_sensor_frames,
    inspect_model_xml,
    joint_names,
    model_id,
    model_variants,
    validate_beta2_inventory,
)


def test_beta2_identifiers_and_inventory_are_canonical() -> None:
    assert "hand2_beta2/body" in DESCRIPTION_ROOT.as_posix()
    assert MODEL_RELEASE == "v2026.8.19"
    assert MODEL_COMMIT == "c003186833616b23c06784ebefe442474cc5f4b5"
    assert ROS_DESCRIPTION_PACKAGE == "wuji_hand2_beta2_description"
    assert USD_FILENAME == "wujihand2_beta2.usd"
    assert len(model_variants()) == 4
    for side in ("left", "right"):
        assert model_id(side) == f"wujihand2-beta2-{side}"
        assert len(joint_names(side)) == 20
        frames = fingertip_sensor_frames(side)
        assert len(frames) == 5
        assert all(name.endswith("_tip_sensor_frame") for name in frames)


def test_beta2_xml_inventory_validation(tmp_path) -> None:
    bodies = "".join(
        f'<body name="f{index}_tip_sensor_frame"><site name="f{index}_tip"/></body>'
        for index in range(5)
    )
    joints = "".join(f'<joint name="j{index}"/>' for index in range(20))
    path = tmp_path / "hand.xml"
    path.write_text(
        f'<mujoco><worldbody><body><inertial mass="1.0"/>{joints}{bodies}'
        "<geom/></body></worldbody></mujoco>",
        encoding="utf-8",
    )
    inventory = inspect_model_xml(path)
    assert validate_beta2_inventory(inventory) == []


def test_gestures_are_asset_independent_and_bounded() -> None:
    for side in ("left", "right"):
        for name in GESTURE_NAMES:
            pose = gesture_pose(side, name)
            assert tuple(pose) == joint_names(side)
            assert all(-1.5 <= value <= 1.5 for value in pose.values())
        trajectory = gesture_trajectory(side)
        assert trajectory.positions.shape == (376, 20)
        assert trajectory.model_id == "wuji-description-v2026.8.19-beta2"
