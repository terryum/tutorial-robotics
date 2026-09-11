from tests.lesson_contract import assert_contract


def test_sim_ros_02_contract(tmp_path):
    assert_contract("sim-ros-02", tmp_path)
