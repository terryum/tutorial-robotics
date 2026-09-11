"""Evidence must connect user interventions, exact controls and saved replay."""
import json

import numpy as np
import pytest

from pai_lab.lessons.dependencies import semantic_source
from pai_lab.lessons.evidence import validate_run
from pai_lab.lessons.models import load
from pai_lab.lessons.observation import inspect_run
from pai_lab.lessons.parameters import parse_parameters, resolve_parameters
from pai_lab.lessons.physics import arm_control
from pai_lab.lessons.runner import run_lesson


def test_kp_only_keeps_damping_and_legacy_variant_records_coupling():
    baseline = resolve_parameters("core-fr3-02", {}, 1.)
    isolated = resolve_parameters("core-fr3-02", {"kp": 180.}, 1.)
    coupled = resolve_parameters("core-fr3-02", {}, 1.5)
    assert isolated["kd"] == baseline["kd"]
    assert coupled["kp"] == isolated["kp"]
    assert coupled["kd"] > isolated["kd"]
    for bad in [["kp=nan"], ["kp=120", "kp=180"]]:
        with pytest.raises(ValueError): parse_parameters(bad)
    with pytest.raises(ValueError): resolve_parameters("core-fr3-02", {"typo": 1}, 1.)
    with pytest.raises(ValueError): resolve_parameters("core-fr3-02", {"kp": 180}, 1.5)


def test_fingerprint_ignores_unrelated_branch_but_not_shared_helper():
    source = '''def helper(x): return x * 2
def run(identifier):
    if identifier == "a": return helper(3)
    if identifier == "b": return 9
'''
    before = semantic_source(source, "a")
    assert semantic_source(source.replace('return 9', 'return 100'), "a") == before
    assert semantic_source(source.replace('x * 2', 'x * 4'), "a") != before
    assert semantic_source('# documentation\n' + source, "a") == before


def test_pd_control_samples_reconstruct_requested_and_clipped_torque():
    model, data, _ = load("fr3")
    _, payload = arm_control(model, data, 8, 180., "pd", 21.)
    for time_s, name, target, q, velocity, requested, applied in payload["control_rows"]:
        assert time_s >= 0
        assert requested == pytest.approx(180 * (target - q) - 21 * velocity)
        limits = model.jnt_actfrcrange[model.joint(name).id]
        assert applied == pytest.approx(np.clip(requested, *limits))
    assert payload["control_rows"][0][5] == pytest.approx(32.4)


def test_inspect_rejects_corruption_and_audit_needs_no_fake_comparison(tmp_path, monkeypatch):
    from pai_lab.lessons.evidence import comparison_errors
    result = run_lesson("core-00", output_dir=tmp_path)
    assert inspect_run("core-00", tmp_path)["value"] == result.metric_value
    assert comparison_errors("core-00", tmp_path, None) == []
    receipt = json.loads((tmp_path / "run.json").read_text())
    assert receipt["schema_version"] == 3
    assert "dependencies" in receipt
    (tmp_path / "trace.csv").write_text("bad evidence")
    assert validate_run("core-00", tmp_path)
    with pytest.raises(ValueError): inspect_run("core-00", tmp_path)
