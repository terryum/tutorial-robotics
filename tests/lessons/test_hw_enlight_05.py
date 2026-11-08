from tests.lesson_contract import assert_contract


def test_contract(tmp_path):
    assert_contract("hw-enlight-05", tmp_path)
