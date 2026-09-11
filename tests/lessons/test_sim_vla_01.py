from tests.lesson_contract import assert_contract


def test_sim_vla_01_contract(tmp_path):
    assert_contract("sim-vla-01", tmp_path)
