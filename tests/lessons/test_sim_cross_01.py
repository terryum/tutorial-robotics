from tests.lesson_contract import assert_contract


def test_sim_cross_01_contract(tmp_path):
    assert_contract("sim-cross-01", tmp_path)
