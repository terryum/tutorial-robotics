from tests.lesson_contract import assert_contract


def test_core_rl_01_contract(tmp_path):
    assert_contract("core-rl-01", tmp_path)
