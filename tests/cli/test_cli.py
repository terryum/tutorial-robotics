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
    assert "sudo" in plan["prohibited_automation"]
    assert plan_path.is_file()


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
