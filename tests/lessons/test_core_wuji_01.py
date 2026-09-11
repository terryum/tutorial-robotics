from tests.lesson_contract import assert_contract


def test_core_wuji_01_contract(tmp_path):
    assert_contract("core-wuji-01", tmp_path)
