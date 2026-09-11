from tests.lesson_contract import assert_contract


def test_core_il_01_contract(tmp_path):
    assert_contract("core-il-01", tmp_path)
