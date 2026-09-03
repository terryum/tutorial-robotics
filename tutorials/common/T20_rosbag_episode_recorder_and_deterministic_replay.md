---
id: T20
title: "Rosbag episode recorder and deterministic replay"
phase: "Data"
mode: "development"
requires: [dev_core, mujoco_supported, ros2_core_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T19]
gpu: "none"
hardware: "none"
---

# T20 — Rosbag episode recorder and deterministic replay

## Objective

시뮬레이션 joint/camera/task 정보를 rosbag으로 기록하고 같은 모델에서 재생해 차이를 측정한다.

## Prerequisites

- Tutorial status: T19
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/05_MAC_ROS2.md`

## Concepts to explain

- timestamp synchronization
- bag storage
- command vs state recording
- deterministic replay limits

## Required implementation targets

- `ros2_ws/src/pai_episode_recorder/`
- `src/pai_lab/data/rosbag_adapter.py`
- `tests/T20/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. episode start/stop metadata를 정의한다
2. state와 command를 함께 기록한다
3. bag을 읽어 MuJoCo target을 재생한다
4. 원본과 replay trajectory를 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T20 --record`
- `pal run T20 --replay <bag-path>`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- replay_error.png
- topic_alignment.png
- replay.mp4

Persist outputs under `outputs/T20/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] timestamp 단조 증가
- [ ] 필수 topic 존재
- [ ] replay error가 정의된 tolerance 내 또는 원인 설명
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
