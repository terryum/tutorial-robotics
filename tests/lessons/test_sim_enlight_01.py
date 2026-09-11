from tests.lesson_contract import assert_contract


def test_sim_enlight_01_contract(tmp_path):
    assert_contract("sim-enlight-01", tmp_path)
