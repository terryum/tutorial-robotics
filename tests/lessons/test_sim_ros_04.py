from tests.lesson_contract import assert_contract


def test_sim_ros_04_contract(tmp_path):
    assert_contract("sim-ros-04", tmp_path)
