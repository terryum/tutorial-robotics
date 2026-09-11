from tests.lesson_contract import assert_contract


def test_sim_enlight_02_contract(tmp_path):
    assert_contract("sim-enlight-02", tmp_path)
