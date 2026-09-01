import numpy as np

from wuji_hand2_setup import WujiHand2MujocoBackend


def test_both_side_backends() -> None:
    for side in ("left", "right"):
        backend = WujiHand2MujocoBackend(side)
        assert len(backend.joint_names) == 20
        backend.set_joint_targets({backend.controlled_joints[4]: 0.3})
        for _ in range(50):
            backend.step()
        assert np.all(np.isfinite(backend.read_state().positions))
