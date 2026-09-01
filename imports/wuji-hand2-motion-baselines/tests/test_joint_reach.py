import numpy as np
import pytest

from wuji_hand2_motion.envs import WujiHand2JointReachEnv


@pytest.mark.parametrize("side", ["left", "right"])
def test_joint_reach_contract(side: str) -> None:
    env = WujiHand2JointReachEnv(side, episode_steps=3)
    observation, info = env.reset(seed=42)
    assert observation.shape == (60,)
    assert np.isfinite(info["joint_error_rmse"])
    for step in range(3):
        observation, reward, terminated, truncated, info = env.step(
            np.zeros(20, dtype=np.float32)
        )
        assert observation.shape == (60,)
        assert np.isfinite(reward)
        assert not terminated
    assert truncated
    env.close()
