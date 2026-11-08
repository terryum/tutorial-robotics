from tests.lesson_contract import assert_contract


def test_contract(tmp_path):
    assert_contract("sim-enlight-04", tmp_path)
