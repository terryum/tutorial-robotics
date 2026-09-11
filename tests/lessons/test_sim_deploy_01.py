from tests.lesson_contract import assert_contract


def test_sim_deploy_01_contract(tmp_path):
    assert_contract("sim-deploy-01", tmp_path)
