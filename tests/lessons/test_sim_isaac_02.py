from tests.lesson_contract import assert_contract


def test_sim_isaac_02_contract(tmp_path):
    assert_contract("sim-isaac-02", tmp_path)
