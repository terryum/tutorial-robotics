from tests.lesson_contract import assert_contract


def test_core_00_contract(tmp_path):
    assert_contract("core-00", tmp_path)
