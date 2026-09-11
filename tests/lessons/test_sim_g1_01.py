from tests.lesson_contract import assert_contract


def test_sim_g1_01_contract(tmp_path):
    assert_contract("sim-g1-01", tmp_path)
