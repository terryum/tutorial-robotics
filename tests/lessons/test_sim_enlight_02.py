from pai_lab.lessons import check_lesson, run_lesson


def test_sim_enlight_02_contract(tmp_path) -> None:
    result = run_lesson("sim-enlight-02", output_dir=tmp_path, seed=7, samples=16)
    assert result.lesson_id == "sim-enlight-02"
    assert result.metric_value >= 0.0
    assert {path.name for path in tmp_path.iterdir()} == {"summary.json", "trace.csv", "lesson-report.md"}
    assert check_lesson("sim-enlight-02") == []
