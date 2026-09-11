from tests.lesson_contract import assert_contract


def test_core_g1_01_contract(tmp_path):
    assert_contract("core-g1-01", tmp_path)
