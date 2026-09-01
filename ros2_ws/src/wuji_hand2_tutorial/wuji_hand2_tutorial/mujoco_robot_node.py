"""Bridge one Wuji Hand 2 MuJoCo model to side-specific ROS 2 topics."""

from __future__ import annotations

from pathlib import Path

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_srvs.srv import Trigger

from wuji_hand2_setup import WujiHand2MujocoBackend, model_path


class MujocoRobotNode(Node):
    def __init__(self) -> None:
        super().__init__("mujoco_robot_node")
        self.declare_parameter("side", "right")
        self.declare_parameter("model_path", "")
        self.declare_parameter("frame_skip", 10)
        self.declare_parameter("show_viewer", False)
        side = str(self.get_parameter("side").value)
        configured_path = str(self.get_parameter("model_path").value)
        path = Path(configured_path) if configured_path else model_path(side)
        frame_skip = int(self.get_parameter("frame_skip").value)
        self.show_viewer = bool(self.get_parameter("show_viewer").value)
        self.hand_name = f"{side}_hand"

        self.backend = WujiHand2MujocoBackend(side, path=path, frame_skip=frame_skip)
        self.publisher = self.create_publisher(
            JointState, f"/{self.hand_name}/joint_states", 10
        )
        self.subscription = self.create_subscription(
            JointState,
            f"/{self.hand_name}/joint_commands",
            self.receive_command,
            10,
        )
        self.reset_service = self.create_service(
            Trigger, f"/{self.hand_name}/mujoco_reset", self.reset
        )
        self.viewer = None
        if self.show_viewer:
            import mujoco.viewer

            self.viewer = mujoco.viewer.launch_passive(
                self.backend.model, self.backend.data
            )
            self.viewer.cam.lookat[:] = (0.0, 0.0, -0.08)
            self.viewer.cam.distance = 0.45
            self.viewer.cam.azimuth = 135
            self.viewer.cam.elevation = -20

        self.timer = self.create_timer(self.backend.control_dt, self.advance)
        self.publish_state()
        self.get_logger().info(
            f"Simulation-only {side} Wuji Hand 2 bridge ready; "
            f"dt={self.backend.control_dt:.3f}s"
        )

    def receive_command(self, message: JointState) -> None:
        if len(message.name) != len(message.position):
            self.get_logger().warning("Ignoring mismatched JointState command")
            return
        try:
            self.backend.set_joint_targets(dict(zip(message.name, message.position)))
        except ValueError as error:
            self.get_logger().warning(f"Ignoring invalid command: {error}")

    def advance(self) -> None:
        self.backend.step()
        self.publish_state()
        if self.viewer is not None:
            if not self.viewer.is_running():
                rclpy.try_shutdown()
                return
            self.viewer.sync()

    def publish_state(self) -> None:
        state = self.backend.read_state()
        message = JointState()
        message.header.stamp = self.get_clock().now().to_msg()
        message.name = list(state.joint_names)
        message.position = state.positions.tolist()
        message.velocity = state.velocities.tolist()
        self.publisher.publish(message)

    def reset(self, request, response):
        del request
        self.backend.reset()
        self.publish_state()
        response.success = True
        response.message = f"{self.hand_name} MuJoCo state reset"
        return response

    def close(self) -> None:
        if self.viewer is not None:
            self.viewer.close()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = MujocoRobotNode()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.close()
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()
