"""Regression coverage for path blocking, durable teaching and numeric checkpoint transfer."""

import json

import numpy as np
import pytest

from pai_lab.cli import main
from pai_lab.local import write_json
from pai_lab.paths import path_lessons, validate_paths
from pai_lab.progress import load_progress, save_progress
from pai_lab.session import pause, resume, update_session
from pai_lab.training import latest_checkpoint, train, transfer_export, transfer_import


def test_paths_have_closed_prerequisites_and_no_unrelated_manipulator_requirements():
    assert validate_paths() == []
    required = path_lessons("manipulator")
    assert "sim-fr3-01" in required and "sim-enlight-05" in required
    assert not any("wuji" in i or "vla" in i or "g1" in i for i in required)


def test_init_preserves_old_completion_and_blocks_at_first_required_lesson(monkeypatch, capsys):
    from pai_lab import cli

    p = load_progress()
    p.completed["core-00"] = {"retained": True}
    save_progress(p)
    assert main(["course", "init", "--path", "manipulator", "--json"]) == 0
    assert load_progress().completed["core-00"]["retained"]
    capsys.readouterr()
    monkeypatch.setattr(cli, "completion_gaps", lambda _: [])
    monkeypatch.setattr(cli, "gaps", lambda _: ["missing Isaac host"])
    assert main(["course", "next", "--json"]) == 2
    result = json.loads(capsys.readouterr().out)
    assert len(result["blocked"]) == 1
    assert main(["course", "summary", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["total"] == len(path_lessons("manipulator"))


def test_pause_resume_preserves_explanation_and_does_not_execute(tmp_path):
    update_session(
        lesson="core-fr3-09",
        phase="explaining",
        notes="error in metres",
        run_dir="BASE",
        comparison_run="COMPARE",
        parameters=["x=1"],
    )
    pause()
    pause()
    result = resume()
    assert result["resume_phase"] == "explaining"
    assert result["saved_state"]["notes"] == "error in metres"
    assert result["automatic_execution"] is False
    write_json(tmp_path / "run.json", {"lesson": "hw-enlight-04", "status": "running"})
    assert resume(tmp_path)["resume_available"] is False
    with pytest.raises(ValueError, match="mismatch"):
        resume(tmp_path, "core-fr3-09")


class ToyArm:
    """Fast deterministic numerical transport for update/resume equivalence."""

    name = "fr3"
    source = None

    def __init__(self):
        self.source = {"revision": "test-only"}
        self.rng = np.random.default_rng(7)
        self.state = np.zeros(17)
        self.target = np.zeros(3)
        self.count = 0

    def reset(self):
        self.state = self.rng.normal(0, 0.01, 17)
        self.count = 0
        return self.state.copy()

    def expert(self):
        return self.state[:7] * 0.1

    def tcp(self):
        return self.state[:3]

    def step(self, action):
        self.state[:7] *= 0.9
        self.count += 1
        return self.state.copy(), -float(np.linalg.norm(self.state)), False, self.count >= 12


@pytest.mark.parametrize("algorithm", ["bc", "ppo"])
def test_interrupted_training_resume_matches_uninterrupted_and_transfer(tmp_path, algorithm):
    first = tmp_path / "first"
    second = tmp_path / "second"
    full = tmp_path / "full"
    result = train(ToyArm(), first, algorithm=algorithm, epochs=4, stop_after=2)
    assert result["status"] == "interrupted"
    transfer_export(first, tmp_path / "portable.json")
    transfer_import(tmp_path / "portable.json", tmp_path / "imported")
    train(ToyArm(), second, algorithm=algorithm, epochs=4, resume_from=tmp_path / "imported")
    train(ToyArm(), full, algorithm=algorithm, epochs=4)
    assert np.array_equal(
        np.load(second / "policy.npz")["weights"], np.load(full / "policy.npz")["weights"]
    )
    assert latest_checkpoint(second)["epoch"] == 4
    (second / "checkpoints/epoch-000005.json").write_text("corrupt")
    assert latest_checkpoint(second)["epoch"] == 4
    with pytest.raises(ValueError, match="incompatible"):
        train(ToyArm(), tmp_path / "bad", algorithm=algorithm, epochs=4, seed=9, resume_from=first)
    bundle = json.loads((tmp_path / "portable.json").read_text())
    bundle["payload"]["checkpoint"]["epoch"] = 999
    write_json(tmp_path / "tampered.json", bundle)
    with pytest.raises(ValueError, match="checksum"):
        transfer_import(tmp_path / "tampered.json", tmp_path / "bad-import")


def test_checkpoint_rejects_data_change(tmp_path):
    train(ToyArm(), tmp_path / "first", epochs=2, stop_after=1)
    records = json.loads((tmp_path / "first/demonstrations.json").read_text())
    records[0]["action"][0] += 1
    write_json(tmp_path / "first/demonstrations.json", records)
    with pytest.raises(ValueError, match="data"):
        train(ToyArm(), tmp_path / "resumed", epochs=2, resume_from=tmp_path / "first")


def test_evaluation_requires_consecutive_hold_and_sixteen_successes():
    from pai_lab.lessons.arm import evaluate

    env = ToyArm()
    result = evaluate(env, np.zeros((18, 7)))
    assert result["hold_steps"] == 10
    assert result["performance_verified"] is False
    assert result["successes"] == 0
    assert result["hardware_tolerance"] is False


@pytest.mark.parametrize("signum", [__import__("signal").SIGINT, __import__("signal").SIGTERM])
def test_real_signal_stops_at_update_boundary(tmp_path, signum):
    import os
    import signal

    env = ToyArm()
    original = env.step
    sent = False

    def step(action):
        nonlocal sent
        if not sent:
            sent = True
            os.kill(os.getpid(), signum)
        return original(action)

    env.step = step
    previous = signal.getsignal(signum)
    result = train(env, tmp_path, algorithm="ppo", epochs=10)
    assert result["status"] == "interrupted"
    assert latest_checkpoint(tmp_path)["epoch"] == 1
    assert signal.getsignal(signum) == previous


def test_isaac_task_modes_keep_enlight_control_separate_from_ppo():
    from pai_lab.lessons.isaac_tasks import task_mode

    assert task_mode("sim-enlight-03") == "control"
    assert task_mode("sim-enlight-04") == "bc"
    assert task_mode("sim-enlight-05") == "ppo"
    assert task_mode("sim-fr3-01") == "control"
    assert task_mode("sim-fr3-02") == "bc"
    assert task_mode("sim-fr3-03") == "ppo"
