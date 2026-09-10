from pai_lab.lessons import check_lesson, run_lesson


def test_core_data_01_contract(tmp_path) -> None:
    result = run_lesson("core-data-01", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "core-data-01"
    assert result.metric_value >= 0.0
    assert {path.name for path in tmp_path.iterdir()} == set(result.artifacts)
    assert check_lesson("core-data-01") == []
