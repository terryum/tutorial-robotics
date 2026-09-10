import pytest

from pai_lab.lessons import check_lesson, implementation_status, run_lesson


def test_hw_enlight_01_contract(tmp_path) -> None:
    assert implementation_status("hw-enlight-01") == "scaffolded"
    with pytest.raises(NotImplementedError):
        run_lesson("hw-enlight-01", output_dir=tmp_path, seed=7, samples=16)
    assert check_lesson("hw-enlight-01") == []
