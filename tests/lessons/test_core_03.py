import json

import pytest

from pai_lab.catalog import resolve_lesson
from pai_lab.lessons import runner
from pai_lab.lessons.evidence import validate_run
from pai_lab.readiness import gaps
from tests.lesson_contract import assert_contract


def test_core_03_contract(tmp_path):
    assert_contract("core-03", tmp_path)


def test_model_inventory_records_compiled_configuration_velocity_and_control_counts(
    tmp_path, monkeypatch
):
    lesson = resolve_lesson("core-03")
    missing = gaps(lesson, prerequisites=False)
    if missing:
        pytest.skip("; ".join(missing))
    monkeypatch.setattr(runner, "gaps", lambda lesson: gaps(lesson, prerequisites=False))

    runner.run_lesson(lesson.id, output_dir=tmp_path)
    assert validate_run(lesson.id, tmp_path) == []
    inventory = json.loads((tmp_path / "model-inventory.json").read_text())
    assert tuple(inventory["fr3"][key] for key in ("nq", "nv", "nu")) == (7, 7, 7)
    assert tuple(inventory["g1"][key] for key in ("nq", "nv", "nu")) == (36, 35, 29)
