from tests.lesson_contract import assert_contract


def test_sim_wuji_02_contract(tmp_path):
    assert_contract("sim-wuji-02", tmp_path)
