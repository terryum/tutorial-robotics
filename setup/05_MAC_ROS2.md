# ROS 2 Jazzy on macOS

## Purpose

Learn ROS 2 concepts and build message/TF/bag bridges locally. This is not the production runtime for vendor hardware.

## Recommended approach

- Pixi
- RoboStack ROS 2 Jazzy channel
- isolated workspace
- CycloneDDS as the first middleware choice
- minimal packages first: ros-base, rclpy, tf2, robot_state_publisher, joint_state_publisher, rosbag2, xacro

## Validation

- two Python nodes communicate
- reliable and best-effort QoS behavior is demonstrated
- TF can be published and queried
- a short bag can be recorded and replayed

## Caveat

Some desktop/GUI or DDS packages may behave differently on macOS. If RViz is unreliable, continue with MuJoCo rendering and TF numerical tests; do not block conceptual ROS lessons solely on RViz.
