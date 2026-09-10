from pai_lab.lessons import check_lesson, run_lesson


def test_core_fr3_05_contract(tmp_path) -> None:
    result = run_lesson("core-fr3-05", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "core-fr3-05"
    assert result.metric_value >= 0.0
    assert {path.name for path in tmp_path.iterdir()} == set(result.artifacts)
    assert check_lesson("core-fr3-05") == []
