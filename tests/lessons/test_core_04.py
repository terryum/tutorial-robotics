from tests.lesson_contract import assert_contract


def test_core_04_contract(tmp_path):
    assert_contract("core-04", tmp_path)
