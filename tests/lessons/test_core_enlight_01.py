from tests.lesson_contract import assert_contract


def test_core_enlight_01_contract(tmp_path):
    assert_contract("core-enlight-01", tmp_path)
