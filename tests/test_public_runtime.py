import json

from pai_lab.cli import PUBLIC_ROBOTS, main
from pai_lab.tutorials import discover, progress, validate_graph


def test_public_tutorial_graph_is_closed() -> None:
    assert len(discover()) == 49
    assert validate_graph() == []


def test_public_cli_needs_no_private_repository(capsys) -> None:
    assert main(["robot", "list"]) == 0
    output = capsys.readouterr().out
    for robot in PUBLIC_ROBOTS:
        assert robot in output


def test_doctor_json_and_tutorial_commands(capsys, monkeypatch, tmp_path) -> None:
    monkeypatch.setattr("pai_lab.progress.PROGRESS_PATH", tmp_path / "progress.json")
    assert main(["doctor", "--format", "json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["repository_errors"] == []

    assert main(["tutorial", "status"]) == 0
    assert "core-00\tpending" in capsys.readouterr().out
    assert progress()["core-00"] == "implemented"

    assert main(["tutorial", "next"]) == 0
    assert capsys.readouterr().out.startswith("id=core-00")
