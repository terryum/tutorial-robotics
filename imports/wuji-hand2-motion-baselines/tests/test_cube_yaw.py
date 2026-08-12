import mujoco
import numpy as np
import pytest

from wuji_hand2_motion.envs import WujiHand2CubeYawEnv


@pytest.mark.parametrize("side", ["left", "right"])
def test_cube_yaw_contract_and_drop(side: str) -> None:
    env = WujiHand2CubeYawEnv(side, episode_seconds=0.08)
    observation, info = env.reset(seed=42)
    assert observation.shape == (71,)
    assert env.model.njnt == 21
    assert env.model.nu == 20
    assert mujoco.mj_name2id(env.model, mujoco.mjtObj.mjOBJ_BODY, "cube") >= 0
    assert np.isfinite(info["yaw_error_rad"])

    contact_steps = 0
    for _ in range(20):
        observation, reward, terminated, truncated, info = env.step(
            np.zeros(20, dtype=np.float32)
        )
        assert observation.shape == (71,)
        assert np.isfinite(reward)
        assert np.all(np.isfinite(observation))
        assert not terminated
        contact_steps += info["contact_count"] > 0

    assert contact_steps >= 15

    env.data.qpos[env.cube_qpos] += 1.0
    mujoco.mj_forward(env.model, env.data)
    _, reward, terminated, _, info = env.step(np.zeros(20, dtype=np.float32))
    assert terminated
    assert info["is_dropped"] == 1.0
    assert reward < 0.0
    env.close()
