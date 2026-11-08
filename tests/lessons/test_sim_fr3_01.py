from tests.lesson_contract import assert_contract


def test_contract(tmp_path):
    assert_contract("sim-fr3-01", tmp_path)
