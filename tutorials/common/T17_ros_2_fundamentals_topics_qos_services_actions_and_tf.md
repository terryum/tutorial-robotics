---
id: T17
title: "ROS 2 fundamentals: communication, parameters, lifecycle, URDF, and TF"
phase: "ROS 2"
mode: "development"
requires: [dev_core, ros2_core_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T00, T02]
gpu: "none"
hardware: "none"
---

# T17 — ROS 2 fundamentals: communication, parameters, lifecycle, URDF, and TF

## Objective

RoboStack Jazzy 환경에서 robot state/command에 필요한 ROS 2 node, executor, topic/QoS, service, action, parameter, launch, lifecycle, URDF, `robot_state_publisher`, `JointState`와 TF를 작은 예제로 학습한다.

## Prerequisites

- Tutorial status: T00, T02
- Host: `mac/either`
- GPU: none
- Hardware access: none
- Read first: `setup/05_MAC_ROS2.md`

## Concepts to explain

- node, callback and executor
- topic and QoS; reliable versus best-effort
- service versus action
- parameter and launch substitution
- lifecycle node states and transitions
- URDF/Xacro, `JointState`, `robot_state_publisher`
- tf2 tree and simulation time
- CycloneDDS preference on Mac; alternative RMW only after explicit test

## Required implementation targets

- `ros2_ws/src/pai_ros2_tutorial/`
- `ros2_ws/src/pai_robot_description/`
- `reports/T17_ros2_fundamentals.md`

## Execution procedure

1. `mac-ros2` environment is created without changing system Python.
2. Record ROS distro and active RMW; prefer CycloneDDS.
3. Implement JointState publisher/subscriber and observe reliable/best-effort behavior.
4. Implement one service and one action with cancellation/feedback.
5. Implement parameters and a launch file with overrides.
6. Implement a lifecycle node and demonstrate configure→activate→deactivate→cleanup.
7. Load one pinned robot URDF, run `robot_state_publisher`, publish JointState and query TF.
8. RViz is optional; a TF graph and numeric transform check are mandatory.

## Commands that must exist or be replaced by documented equivalents

- `pixi run ros2 launch pai_ros2_tutorial fundamentals.launch.py`
- `pixi run ros2 lifecycle get /tutorial_lifecycle_node`
- `pixi run colcon test`

## Visualization contract

- `topic_rate.csv`
- `qos_delivery_comparison.png`
- `lifecycle_transitions.md`
- `tf_tree.md`
- `message_timeline.png`

Persist outputs under `outputs/T17/<run-id>/`.

## Acceptance criteria

- [ ] pub/sub, QoS mismatch, service and action behavior are demonstrated
- [ ] parameter override and launch substitution work
- [ ] lifecycle transitions are verified
- [ ] URDF + JointState + robot_state_publisher produces queryable TF
- [ ] ROS distro/RMW and Mac limitations are recorded
- [ ] tests, actual execution, persistent outputs and Korean report exist
- [ ] state is updated

## Failure handling

Do not substitute a Linux-only vendor runtime for this Mac lesson. If RViz is unstable, complete the numeric TF/offscreen path and record the limitation.
