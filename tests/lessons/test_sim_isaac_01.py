from tests.lesson_contract import assert_contract


def test_sim_isaac_01_contract(tmp_path):
    assert_contract("sim-isaac-01", tmp_path)
