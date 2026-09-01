# Architecture

```text
official wuji-description v2026.8.3 (read-only)
              |
              +-- native MJCF position actuators -- MuJoCo viewer/tests
              |
              +-- wuji_hand2_description -- robot_state_publisher -- RViz

sensor_msgs/JointState command
              |
              v
WujiHand2MujocoBackend (public mujoco-ros2-core v0.2.0)
              |
              +-- native actuator ctrl
              +-- named joint state
```

Left and right simulations are independent processes with unique model names,
joint names, ROS namespaces, topics, and wrist frames. This is deliberate: a
future teleoperation source can publish the official per-hand command topics
without knowing whether the consumer is MuJoCo or a separately gated hardware
driver.
