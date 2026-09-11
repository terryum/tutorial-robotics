"""Actual isolated ROS 2 communication and rosbag2 replay. Requires sourced Jazzy."""

from __future__ import annotations

import os
import time
from pathlib import Path
from typing import Any

import mujoco
import numpy as np

from pai_lab.lessons.experiment import Experiment
from pai_lab.lessons.models import load
from pai_lab.lessons.physics import pendulum


def run(identifier: str, output: Path, seed: int, samples: int, variant: float = 1.0) -> Experiment:
    os.environ["ROS_LOCALHOST_ONLY"] = "1"
    os.environ["ROS_DOMAIN_ID"] = "217"
    import rclpy
    from geometry_msgs.msg import TransformStamped
    from rclpy.node import Node
    from rclpy.qos import QoSProfile, ReliabilityPolicy
    from rclpy.serialization import deserialize_message, serialize_message
    from sensor_msgs.msg import JointState
    from std_srvs.srv import Trigger
    from tf2_ros import Buffer, StaticTransformBroadcaster, TransformListener

    context = rclpy.Context()
    rclpy.init(context=context)
    node = Node("pal_lesson", namespace="/pal_isolated", context=context)
    model, data = pendulum()
    if identifier == "sim-enlight-01":
        model, data, source = load("enlight", output)
    else:
        source = {"model": "repository pendulum"}
    qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)
    received: list[Any] = []
    written, rows = [], []
    publisher = node.create_publisher(JointState, "joint_states", qos)
    subscription = node.create_subscription(JointState, "joint_states", received.append, qos)
    service = node.create_service(
        Trigger, "reset", lambda request, response: reset_response(response, model, data)
    )
    client = node.create_client(Trigger, "reset")
    broadcaster = StaticTransformBroadcaster(node)
    buffer = Buffer()
    _listener = TransformListener(buffer, node)
    writer = None
    try:
        tf = TransformStamped()
        tf.header.stamp = node.get_clock().now().to_msg()
        tf.header.frame_id, tf.child_frame_id = "pal_world", "pal_base"
        tf.transform.rotation.w = 1.0
        broadcaster.sendTransform(tf)
        deadline = time.monotonic() + 5
        while publisher.get_subscription_count() == 0 and time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=0.05)
        if publisher.get_subscription_count() == 0:
            raise RuntimeError("DDS discovery timeout in isolated domain")
        if not client.wait_for_service(timeout_sec=3):
            raise RuntimeError("ROS service unavailable")
        response = client.call_async(Trigger.Request())
        rclpy.spin_until_future_complete(node, response, timeout_sec=3)
        service_ok = response.done() and response.result().success
        if identifier == "sim-ros-03":
            import rosbag2_py

            writer = rosbag2_py.SequentialWriter()
            writer.open(
                rosbag2_py.StorageOptions(uri=str(output / "episode_bag"), storage_id="sqlite3"),
                rosbag2_py.ConverterOptions("", ""),
            )
            writer.create_topic(
                rosbag2_py.TopicMetadata(
                    id=0,
                    name="/pal_isolated/joint_states",
                    type="sensor_msgs/msg/JointState",
                    serialization_format="cdr",
                )
            )
        for i in range(samples):
            data.ctrl[:] = 0.1 * variant * np.sin(i * 0.1)
            for _ in range(10):
                mujoco.mj_step(model, data)
            message = JointState()
            message.header.stamp.sec = int(data.time)
            message.header.stamp.nanosec = int((data.time - int(data.time)) * 1e9)
            message.name = [model.joint(j).name for j in range(model.njnt)]
            message.position = data.qpos.tolist()
            message.velocity = data.qvel.tolist()
            publisher.publish(message)
            written.append(message)
            if writer:
                writer.write(
                    "/pal_isolated/joint_states", serialize_message(message), int(data.time * 1e9)
                )
            deadline = time.monotonic() + 2
            while len(received) <= i and time.monotonic() < deadline:
                rclpy.spin_once(node, timeout_sec=0.02)
            if len(received) <= i:
                raise RuntimeError("ROS sample receive timeout")
            rows.append(
                (float(data.time), float(message.position[0]), float(received[-1].position[0]))
            )
        graph = {
            "nodes": node.get_node_names(),
            "topics": node.get_topic_names_and_types(),
            "services": node.get_service_names_and_types(),
            "qos": "reliable depth=10",
            "domain": 217,
            "localhost_only": True,
            "source": source,
        }
        tf_ok = buffer.can_transform("pal_world", "pal_base", rclpy.time.Time())
        checks = {
            "all_messages_received": len(received) == samples,
            "service_roundtrip": bool(service_ok),
            "tf_received": bool(tf_ok),
            "state_equal": all(a == b for _, a, b in rows),
        }
        if identifier == "sim-ros-01":
            from example_interfaces.action import Fibonacci
            from rclpy.action import ActionClient, ActionServer

            def execute(goal: Any) -> Any:
                result = Fibonacci.Result()
                result.sequence = [0, 1]
                for _ in range(goal.request.order - 2):
                    result.sequence.append(result.sequence[-1] + result.sequence[-2])
                goal.succeed()
                return result

            server = ActionServer(node, Fibonacci, "bounded_action", execute)
            action_client = ActionClient(node, Fibonacci, "bounded_action")
            try:
                if not action_client.wait_for_server(timeout_sec=3):
                    raise RuntimeError("action discovery timeout")
                goal = Fibonacci.Goal()
                goal.order = 8
                future = action_client.send_goal_async(goal)
                rclpy.spin_until_future_complete(node, future, timeout_sec=3)
                if not future.done() or not future.result().accepted:
                    raise RuntimeError("action goal rejected")
                result_future = future.result().get_result_async()
                rclpy.spin_until_future_complete(node, result_future, timeout_sec=3)
                checks["action_roundtrip"] = result_future.done() and list(
                    result_future.result().result.sequence
                ) == [0, 1, 1, 2, 3, 5, 8, 13]
                graph["action_result"] = list(result_future.result().result.sequence)
            finally:
                action_client.destroy()
                server.destroy()
        if identifier == "sim-ros-03":
            del writer
            writer = None
            reader = rosbag2_py.SequentialReader()
            reader.open(
                rosbag2_py.StorageOptions(uri=str(output / "episode_bag"), storage_id="sqlite3"),
                rosbag2_py.ConverterOptions("", ""),
            )
            replay = []
            while reader.has_next():
                _, payload, stamp = reader.read_next()
                message = deserialize_message(payload, JointState)
                replay.append((stamp, message.position))
            checks["bag_replay_exact"] = len(replay) == samples and all(
                list(position) == list(message.position)
                for (_, position), message in zip(replay, written, strict=True)
            )
            graph.update(
                storage_id="sqlite3", messages_written=samples, messages_replayed=len(replay)
            )
        if identifier == "sim-ros-04":
            graph["embodiment"] = {
                "reset": bool(service_ok),
                "observe": len(received),
                "act": samples,
                "close": "destroy local publisher/subscription in finally",
                "observation_units": ["rad", "rad/s"],
                "action_units": "Nm",
            }
        return Experiment(
            rows,
            float(max(abs(a - b) for _, a, b in rows)),
            graph,
            checks,
            model,
            data,
            ["enlight-draft.xml"] if identifier == "sim-enlight-01" else [],
        )
    finally:
        if writer is not None:
            del writer
        node.destroy_subscription(subscription)
        node.destroy_service(service)
        node.destroy_node()
        context.shutdown()


def reset_response(response: Any, model: Any, data: Any) -> Any:
    mujoco.mj_resetData(model, data)
    if model.nkey:
        mujoco.mj_resetDataKeyframe(model, data, 0)
    mujoco.mj_forward(model, data)
    response.success = True
    response.message = "simulation reset"
    return response
