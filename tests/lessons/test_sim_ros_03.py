from tests.lesson_contract import assert_contract


def test_sim_ros_03_contract(tmp_path):
    assert_contract("sim-ros-03", tmp_path)
