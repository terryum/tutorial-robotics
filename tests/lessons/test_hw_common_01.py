from tests.lesson_contract import assert_contract


def test_hw_common_01_contract(tmp_path):
    assert_contract("hw-common-01", tmp_path)
