import json

import numpy as np
import pytest

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons.evidence import validate_run
from pai_lab.lessons.parameters import resolve_parameters
from pai_lab.lessons.runner import run_lesson
from pai_lab.readiness import gaps
from tests.lesson_contract import assert_contract


@pytest.mark.usefixtures("native_macos_gl")
def test_core_01_contract(tmp_path):
    assert_contract("core-01", tmp_path)


@pytest.mark.usefixtures("native_macos_gl")
def test_release_angle_changes_peak_with_synchronized_observations(tmp_path):
    missing = gaps(resolve_lesson("core-01"), prerequisites=False)
    if missing:
        pytest.skip("; ".join(missing))
    baseline, comparison = tmp_path / "baseline", tmp_path / "comparison"
    for path, angle in ((baseline, 0.35), (comparison, 0.70)):
        run_lesson("core-01", output_dir=path, parameters={"initial_angle_rad": angle})
        assert validate_run("core-01", path) == []

    first, second = [
        json.loads((path / "experiment.json").read_text()) for path in (baseline, comparison)
    ]
    assert first["parameters"] == {"initial_angle_rad": 0.35, "timestep": 0.002}
    assert second["parameters"] == {"initial_angle_rad": 0.70, "timestep": 0.002}
    reference, changed = first["payload"], second["payload"]
    assert reference["gravity_m_s2"] == changed["gravity_m_s2"]
    assert (
        reference["initial_angular_velocity_rad_s"]
        == changed["initial_angular_velocity_rad_s"]
        == 0
    )
    assert (baseline / "replay.mjb").read_bytes() == (comparison / "replay.mjb").read_bytes()
    a, b = [np.asarray(data["state"]) for data in (reference, changed)]
    np.testing.assert_array_equal(a[:, 0], b[:, 0])
    assert a[0, 0] == 0
    assert a[-1, 0] == pytest.approx(1.28)
    a_turn, b_turn = np.argmin(a[:, 1]), np.argmin(b[:, 1])
    assert b[b_turn, 1] < a[a_turn, 1] < 0
    assert changed["tip_positions_m"][b_turn][2] > reference["tip_positions_m"][a_turn][2]


def test_optional_timestep_parameter_preserves_default_release_angle():
    assert (
        resolve_parameters("core-01", {"timestep": 0.004}, 1.0)
        == resolve_parameters("core-01", {}, 2.0)
        == {"initial_angle_rad": 0.35, "timestep": 0.004}
    )
