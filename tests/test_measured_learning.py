import numpy as np

from pai_lab.lessons.learning import Pendulum, generalized_advantage, ppo
from pai_lab.lessons.physics import run


def test_gae_bootstraps_truncation_but_not_terminal():
    rewards = np.array([1.0, 1.0])
    values = np.array([0.0, 0.0])
    next_values = np.array([2.0, 2.0])
    terminal = np.array([False, True])
    boundary = np.array([True, True])
    actual = generalized_advantage(rewards, values, next_values, terminal, boundary, gamma=0.5)
    np.testing.assert_allclose(actual, [2.0, 1.0])


def test_ppo_changes_parameters_and_reloads_real_policy(tmp_path):
    result = ppo(Pendulum(7), tmp_path, 7, 32, 1.0)
    assert all(result.checks.values())
    weights = np.load(tmp_path / "policy.npz")["weights"]
    assert weights.shape == (3, 1)
    assert result.payload["parameter_delta"] > 1e-8
    assert result.payload["reload_max_error"] == 0
    assert result.payload["performance_verified"] is False
    assert all(np.isfinite(row["objective"]) for row in result.payload["updates"])


def test_pendulum_energy_is_computed_from_mujoco(tmp_path):
    result = run("core-01", tmp_path, 7, 64)
    assert result.metric < 1e-5
    assert result.model.nq == 1
    state = np.array(result.payload["state"])
    assert np.ptp(state[:, 1]) > 0.01
    assert state[-1, 0] > state[0, 0]


def test_acceptance_recomputes_energy_instead_of_trusting_success_flag(tmp_path):
    from pai_lab.lessons.acceptance import measurement_errors

    actual = run("core-01", tmp_path, 7, 64)
    experiment = {"payload": actual.payload, "metric": actual.metric, "checks": {"passed": True}}
    trace = np.array(actual.rows)
    assert measurement_errors("core-01", tmp_path, trace, experiment) == []
    trace[-1, 2] += 0.01
    assert measurement_errors("core-01", tmp_path, trace, experiment)
