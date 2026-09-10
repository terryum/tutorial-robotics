from pai_lab.lessons import check_lesson, run_lesson


def test_sim_cross_01_contract(tmp_path) -> None:
    result = run_lesson("sim-cross-01", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "sim-cross-01"
    assert result.metric_value >= 0.0
    assert {path.name for path in tmp_path.iterdir()} == set(result.artifacts)
    assert check_lesson("sim-cross-01") == []
