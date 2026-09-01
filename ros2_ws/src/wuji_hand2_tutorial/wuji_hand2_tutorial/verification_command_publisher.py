"""Publish bounded sine, open, or fist verification targets."""

from __future__ import annotations

import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState

from wuji_hand2_setup import joint_names, verification_pose


class VerificationCommandPublisher(Node):
    def __init__(self) -> None:
        super().__init__("verification_command_publisher")
        self.declare_parameter("side", "right")
        self.declare_parameter("mode", "sine")
        self.declare_parameter("amplitude", 0.3)
        self.declare_parameter("frequency", 0.2)
        self.side = str(self.get_parameter("side").value)
        self.mode = str(self.get_parameter("mode").value)
        if self.mode not in {"sine", "open", "fist"}:
            raise ValueError("mode must be sine, open, or fist")
        self.amplitude = float(self.get_parameter("amplitude").value)
        self.frequency = float(self.get_parameter("frequency").value)
        self.publisher = self.create_publisher(
            JointState, f"/{self.side}_hand/joint_commands", 10
        )
        self.started = self.get_clock().now()
        self.timer = self.create_timer(0.05, self.publish_target)

    def publish_target(self) -> None:
        if self.mode == "sine":
            elapsed = (self.get_clock().now() - self.started).nanoseconds / 1e9
            names = [joint_names(self.side)[4]]
            positions = [
                self.amplitude * math.sin(2.0 * math.pi * self.frequency * elapsed)
            ]
        else:
            pose = verification_pose(self.side, self.mode)
            names = list(pose)
            positions = list(pose.values())
        message = JointState()
        message.header.stamp = self.get_clock().now().to_msg()
        message.name = names
        message.position = positions
        self.publisher.publish(message)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = VerificationCommandPublisher()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
