from tests.lesson_contract import assert_contract


def test_sim_ros_01_contract(tmp_path):
    assert_contract("sim-ros-01", tmp_path)
