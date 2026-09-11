from tests.lesson_contract import assert_contract


def test_core_aloha_01_contract(tmp_path):
    assert_contract("core-aloha-01", tmp_path)
