import json

import pai_lab.progress as progress_module
from pai_lab.cli import main


def test_course_init_next_and_setup_plan_are_json(tmp_path, monkeypatch, capsys) -> None:
    progress_path = tmp_path / "progress.json"
    monkeypatch.setattr(progress_module, "PROGRESS_PATH", progress_path)
    assert main(["course", "init", "--through", "core", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["through"] == "core"
    assert main(["course", "next", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "core-00"

    plan_path = tmp_path / "plan.json"
    assert main(["setup", "plan", "--stage", "core", "--out", str(plan_path), "--json"]) == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["stage"] == "core"
    assert plan["profile"] == "core"
    assert "sudo" in plan["prohibited_automation"]
    assert plan_path.is_file()

    assert main(["course", "runnable", "--without-hardware", "--json"]) == 0
    runnable = json.loads(capsys.readouterr().out)
    assert len(runnable) == 41
    assert all(item["hardware_free"] for item in runnable)


def test_profile_plan_does_not_pull_unrelated_stacks(tmp_path, capsys) -> None:
    plan_path = tmp_path / "ros-plan.json"
    assert main([
        "setup", "plan", "--profile", "ros", "--out", str(plan_path), "--json"
    ]) == 0
    plan = json.loads(capsys.readouterr().out)
    assert plan["profile"] == "ros"
    assert "ros" in plan["python_extras"]
    assert all("Isaac" not in item for item in plan["manual_requirements"])


def test_missing_hardware_snapshot_is_capability_unavailable(tmp_path, capsys) -> None:
    code = main([
        "hardware",
        "preflight",
        "wuji",
        "--read-only",
        "--snapshot",
        str(tmp_path / "missing.json"),
        "--json",
    ])
    assert code == 2
    assert json.loads(capsys.readouterr().out)["status"] == "capability-unavailable"
