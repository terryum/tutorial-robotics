import pytest

from pai_lab.lessons import check_lesson, implementation_status, run_lesson


def test_hw_enlight_03_contract(tmp_path) -> None:
    assert implementation_status("hw-enlight-03") == "scaffolded"
    with pytest.raises(NotImplementedError):
        run_lesson("hw-enlight-03", output_dir=tmp_path, seed=7, samples=16)
    assert check_lesson("hw-enlight-03") == []
