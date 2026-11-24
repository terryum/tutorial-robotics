import json

import numpy as np
import pytest

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons import runner
from pai_lab.lessons.evidence import validate_run
from pai_lab.readiness import gaps
from tests.lesson_contract import assert_contract


def test_core_04_contract(tmp_path):
    assert_contract("core-04", tmp_path)


def test_camera_azimuth_changes_rendered_pixels_with_fixed_fr3_pose(tmp_path, monkeypatch):
    lesson = resolve_lesson("core-04")
    missing = gaps(lesson, prerequisites=False)
    if missing:
        pytest.skip("; ".join(missing))
    monkeypatch.setattr(runner, "gaps", lambda lesson: gaps(lesson, prerequisites=False))

    baseline, comparison = tmp_path / "baseline", tmp_path / "comparison"
    for path, azimuth in ((baseline, 135.0), (comparison, 165.0)):
        runner.run_lesson(lesson.id, output_dir=path, parameters={"camera_azimuth": azimuth})
        assert validate_run(lesson.id, path) == []

    first, second = [
        json.loads((path / "experiment.json").read_text()) for path in (baseline, comparison)
    ]
    assert first["parameters"] == {"camera_azimuth": 135.0}
    assert second["parameters"] == {"camera_azimuth": 165.0}
    assert first["payload"] == second["payload"]
    assert (baseline / "frame.png").read_bytes() != (comparison / "frame.png").read_bytes()
    with np.load(baseline / "replay.npz") as a, np.load(comparison / "replay.npz") as b:
        for field in ("time_s", "qpos", "qvel"):
            np.testing.assert_array_equal(a[field], b[field])
