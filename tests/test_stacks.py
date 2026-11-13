"""Optional GPU setup must not fabricate readiness or mutate existing sources."""

import json
from unittest.mock import patch

import pytest

from pai_lab import stacks


def test_registry_has_immutable_revisions():
    for entry in stacks.registry()["profiles"].values():
        assert len(entry["revision"]) == 40
        assert all(c in "0123456789abcdef" for c in entry["revision"])


def test_mac_plan_and_apply_do_not_launch_installers():
    with (
        patch.object(stacks.platform, "system", return_value="Darwin"),
        patch.object(stacks, "run") as run,
    ):
        assert stacks.plan("groot")["status"] == "capability-unavailable"
        with pytest.raises(RuntimeError, match="native Linux"):
            stacks.apply("groot")
        run.assert_not_called()


def test_missing_environment_is_not_ready(tmp_path):
    with patch.object(stacks, "paths", return_value=(tmp_path / "source", tmp_path / "env")):
        assert stacks.verify("pi05")["ready"] is False


def test_source_mismatch_rejected_before_sync(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    with (
        patch.object(stacks.platform, "system", return_value="Linux"),
        patch.object(stacks.platform, "machine", return_value="x86_64"),
        patch.object(stacks.shutil, "which", return_value="installed"),
        patch.object(
            stacks.shutil, "disk_usage", return_value=type("Disk", (), {"free": 100_000_000_000})()
        ),
        patch.object(stacks, "paths", return_value=(source, tmp_path / "env")),
        patch.object(stacks.subprocess, "check_output", side_effect=["wrong", ""]),
        patch.object(stacks, "run") as run,
    ):
        with pytest.raises(RuntimeError, match="revision/cleanliness"):
            stacks.apply("groot")
        run.assert_not_called()


def test_cli_failure_is_json(capsys):
    with patch.object(stacks, "download", side_effect=RuntimeError("missing weights")):
        assert stacks.main(["download", "--profile", "groot", "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "blocked"
