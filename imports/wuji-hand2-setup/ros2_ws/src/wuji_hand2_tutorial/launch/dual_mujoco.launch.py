"""Start independent left and right Wuji Hand 2 MuJoCo nodes."""

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="wuji_hand2_tutorial",
                executable="mujoco_robot_node",
                name="left_mujoco_robot_node",
                parameters=[{"side": "left", "show_viewer": False}],
            ),
            Node(
                package="wuji_hand2_tutorial",
                executable="mujoco_robot_node",
                name="right_mujoco_robot_node",
                parameters=[{"side": "right", "show_viewer": False}],
            ),
        ]
    )
