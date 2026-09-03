---
id: T19
title: "MuJoCo–ROS 2 bridge"
phase: "ROS 2"
mode: "development"
requires: [dev_core, mujoco_supported, ros2_core_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T04, T17]
gpu: "none"
hardware: "none"
---

# T19 — MuJoCo–ROS 2 bridge

## Objective

MuJoCo state를 ROS 2 JointState/TF로 발행하고 ROS 2 명령으로 simulation을 제어한다.

## Prerequisites

- Tutorial status: T04, T17
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/05_MAC_ROS2.md`

## Concepts to explain

- simulation clock
- state publisher
- command subscriber
- rate separation
- thread ownership

## Required implementation targets

- `src/pai_lab/ros2_bridge/`
- `ros2_ws/src/pai_mujoco_bridge/`
- `tests/T19/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. physics thread와 ROS executor를 분리한다
2. joint names/units를 registry에서 읽는다
3. JointState와 `/clock`을 발행한다
4. safe joint target command를 수신한다

## Commands that must exist or be replaced by documented equivalents

- `pixi run ros2 launch pai_mujoco_bridge fr3_bridge.launch.py`
- `pytest tests/T19 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- ros_sim_timeline.png
- joint_command_tracking.png
- rollout.mp4

Persist outputs under `outputs/T19/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] ROS rate와 physics rate 기록
- [ ] 명령 timeout 시 safe hold/stop
- [ ] joint order round-trip 검증
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
