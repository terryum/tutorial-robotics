import mujoco
import numpy as np
import pytest

from wuji_hand2_setup import WujiHand2MujocoBackend, joint_names, verification_pose


@pytest.mark.parametrize("side,prefix", [("left", "l"), ("right", "r")])
def test_model_contract_and_native_motion(side: str, prefix: str) -> None:
    backend = WujiHand2MujocoBackend(side)
    assert backend.model.njnt == 20
    assert backend.model.nu == 20
    assert backend.joint_names == joint_names(side)
    assert backend.controlled_joints == joint_names(side)
    assert np.all(np.isfinite(backend.read_state().positions))

    tips = {
        mujoco.mj_id2name(backend.model, mujoco.mjtObj.mjOBJ_SITE, index)
        for index in range(backend.model.nsite)
    }
    assert len({name for name in tips if name and name.endswith("_tip")}) == 5

    joint = f"{prefix}_index_finger_mcp_flex"
    initial = float(backend.read_control_state().positions[4])
    backend.set_joint_targets({joint: initial + 0.35})
    for _ in range(250):
        backend.step()
    final = float(backend.read_control_state().positions[4])
    assert final > initial + 0.15

    backend.reset()
    np.testing.assert_allclose(backend.read_control_state().positions, backend.home)


@pytest.mark.parametrize("side", ["left", "right"])
@pytest.mark.parametrize("pose_name", ["open", "fist"])
def test_verification_poses_fit_limits(side: str, pose_name: str) -> None:
    backend = WujiHand2MujocoBackend(side)
    pose = verification_pose(side, pose_name)
    assert set(pose) == set(backend.controlled_joints)
    backend.set_joint_targets(pose)
    assert np.all(backend.target >= backend.lower)
    assert np.all(backend.target <= backend.upper)
