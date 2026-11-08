from tests.lesson_contract import assert_contract


def test_contract(tmp_path):
    assert_contract("sim-fr3-02", tmp_path)
