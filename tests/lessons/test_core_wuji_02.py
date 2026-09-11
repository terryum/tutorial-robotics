from tests.lesson_contract import assert_contract


def test_core_wuji_02_contract(tmp_path):
    assert_contract("core-wuji-02", tmp_path)
