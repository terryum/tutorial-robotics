from pai_lab.cli import PUBLIC_ROBOTS, main
from pai_lab.tutorials import discover, validate_graph


def test_public_tutorial_graph_is_closed() -> None:
    assert discover()
    assert validate_graph() == []


def test_public_cli_needs_no_private_repository(capsys) -> None:
    assert main(["robot", "list"]) == 0
    output = capsys.readouterr().out
    for robot in PUBLIC_ROBOTS:
        assert robot in output

