"""Visualize one side-specific MuJoCo state stream in RViz."""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context):
    side = LaunchConfiguration("side").perform(context)
    share = get_package_share_directory("wuji_hand2_description")
    with open(os.path.join(share, "urdf", f"{side}-ros.urdf"), encoding="utf-8") as file:
        description = file.read()
    prefix = "l" if side == "left" else "r"
    return [
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[{"robot_description": description}],
            remappings=[("/joint_states", f"/{side}_hand/joint_states")],
        ),
        Node(
            package="tf2_ros",
            executable="static_transform_publisher",
            arguments=["--frame-id", "world", "--child-frame-id", f"{prefix}_wrist"],
        ),
        Node(package="rviz2", executable="rviz2"),
    ]


def generate_launch_description():
    return LaunchDescription(
        [DeclareLaunchArgument("side", default_value="right"), OpaqueFunction(function=launch_setup)]
    )
