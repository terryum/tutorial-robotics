from tests.lesson_contract import assert_contract


def test_contract(tmp_path):
    assert_contract("core-fr3-10", tmp_path)
