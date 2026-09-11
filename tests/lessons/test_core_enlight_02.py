from tests.lesson_contract import assert_contract


def test_core_enlight_02_contract(tmp_path):
    assert_contract("core-enlight-02", tmp_path)
