from tests.lesson_contract import assert_contract


def test_sim_wuji_01_contract(tmp_path):
    assert_contract("sim-wuji-01", tmp_path)
