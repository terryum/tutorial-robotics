from tests.lesson_contract import assert_contract


def test_sim_vla_02_contract(tmp_path):
    assert_contract("sim-vla-02", tmp_path)
