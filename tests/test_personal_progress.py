"""Opt-in boundary, local evidence and backwards-compatible CLI tests."""

import json
import subprocess

import pytest

from pai_lab import personal_progress as bridge
from pai_lab.cli import main
from pai_lab.local import write_json
from pai_lab.progress import load_progress, save_progress


def registration(root):
    write_json(
        root / ".local/personal-progress.json",
        {"enabled": True, "registered_root": str(root), "helper": ["helper"]},
    )


def test_new_learner_summary_is_zero_and_does_not_spawn_helper(monkeypatch, capsys):
    def forbidden(*args, **kwargs):
        raise AssertionError("a default user must not invoke a helper")

    monkeypatch.setattr(bridge.subprocess, "run", forbidden)
    assert main(["course", "summary", "--json"]) == 0
    value = json.loads(capsys.readouterr().out)
    assert value["completed"] == 0
    from pai_lab.paths import selected_lessons

    assert value["total"] == len(selected_lessons())
    assert value["sync"]["status"] == "disabled"


def test_developer_override_even_same_path_disables_registration(tmp_path, monkeypatch):
    registration(tmp_path)
    monkeypatch.setenv("PAL_LOCAL_DIR", str(tmp_path / ".local"))
    assert bridge.configuration(tmp_path) is None
    monkeypatch.delenv("PAL_LOCAL_DIR")
    assert bridge.configuration(tmp_path)
    monkeypatch.setenv("PAL_PRIVATE_LOCAL_DIR", str(tmp_path / ".local"))
    assert bridge.configuration(tmp_path) is None


def test_helper_unavailable_keeps_cached_history(tmp_path, monkeypatch):
    registration(tmp_path)
    monkeypatch.delenv("PAL_LOCAL_DIR")
    write_json(
        tmp_path / ".local/personal-progress-cache.json",
        {
            "schema_version": 1,
            "completed": 1,
            "lessons": [],
            "sync": {"status": "synced", "last_success": "yesterday"},
        },
    )

    def unavailable(*args, **kwargs):
        raise subprocess.TimeoutExpired("helper", 1)

    monkeypatch.setattr(bridge.subprocess, "run", unavailable)
    result = bridge.exchange(root=tmp_path)
    assert result["completed"] == 1
    assert result["sync"]["status"] == "pending"
    assert result["sync"]["last_success"] == "yesterday"


def test_shared_completion_has_no_local_run_and_is_not_saved(monkeypatch, tmp_path):
    monkeypatch.setattr(
        bridge,
        "snapshot",
        lambda *args: {
            "lessons": [
                {"id": "core-00", "scope": "public", "completed": True, "needs_review": False}
            ]
        },
    )
    progress = load_progress()
    assert progress.completed["core-00"]["shared"]
    assert "run_dir" not in progress.completed["core-00"]
    path = tmp_path / "progress.json"
    save_progress(progress, path)
    assert json.loads(path.read_text())["completed"] == {}
    from pai_lab.lessons.learning import previous_run

    with pytest.raises(FileNotFoundError, match="actual data/policy"):
        previous_run("core-00")


def test_shared_history_does_not_supply_host_or_hardware_capabilities(monkeypatch):
    from pai_lab.catalog import resolve_lesson
    from pai_lab.readiness import gaps

    monkeypatch.setattr(bridge, "shared_gaps", lambda *args, **kwargs: [])
    monkeypatch.setattr(bridge, "snapshot", lambda *args: {"lessons": []})
    errors = gaps(resolve_lesson("hw-fr3-01"), prerequisites=False)
    assert any("capability" in item for item in errors)
    assert any("scaffolded" in item for item in errors)


def test_shared_version_mismatch_is_review_not_lost_completion(monkeypatch):
    monkeypatch.setattr(
        bridge,
        "snapshot",
        lambda *args: {
            "lessons": [
                {"id": "core-00", "scope": "public", "completed": True, "needs_review": True}
            ]
        },
    )
    assert "core-00" in load_progress().completed
    assert bridge.shared_gaps("core-00")


def test_previous_core_contract_retains_shared_progress(monkeypatch):
    from pai_lab.lessons.evidence import CORE_HISTORY

    row = {
        "id": "core-01",
        "scope": "public",
        "completed": True,
        "needs_review": True,
        "verified_digests": [CORE_HISTORY["core-01"][0]],
    }
    monkeypatch.setattr(bridge, "snapshot", lambda *args: {"lessons": [row]})
    assert bridge.shared_gaps("core-01") == []
    row["unresolved_feedback"] = True
    assert bridge.shared_gaps("core-01") == [
        "unresolved shared feedback; resume the originating environment"
    ]


def test_shared_summary_excludes_diagnostic_without_mutating_history(monkeypatch):
    cached = {
        "lessons": [
            {"id": "core-00", "scope": "public", "stage": "core", "completed": True},
            {"id": "core-01", "scope": "public", "stage": "core", "completed": False},
            {"id": "private-example", "scope": "private", "stage": "private", "completed": True},
        ],
        "groups": {
            "core": {"completed": 1, "total": 2, "percent": 50},
            "private": {"completed": 1, "total": 1, "percent": 100},
        },
        "completed": 2,
        "total": 3,
        "verified_completed": 2,
    }
    monkeypatch.setattr(bridge, "snapshot", lambda *args: cached)
    summary = bridge.summary()
    assert [row["id"] for row in summary["lessons"]] == ["core-01", "private-example"]
    assert (summary["completed"], summary["total"], summary["percent"]) == (1, 2, 50)
    assert summary["verified_completed"] == 1
    assert summary["groups"]["core"] == {"completed": 0, "total": 1, "percent": 0}
    assert summary["groups"]["private"] == cached["groups"]["private"]
    assert load_progress().completed["core-00"]["shared"]
    assert len(cached["lessons"]) == 3
