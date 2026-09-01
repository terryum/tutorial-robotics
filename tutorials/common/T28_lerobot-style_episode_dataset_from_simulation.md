---
id: T28
title: "LeRobot-style episode dataset from simulation"
phase: "Imitation Learning"
host: "mac/either"
prerequisites: [T20, T21]
gpu: "optional"
hardware: "none"
---

# T28 — LeRobot-style episode dataset from simulation

## Objective

MuJoCo/ROS episode를 synchronized image, state, action, task metadata를 가진 LeRobot-compatible dataset으로 변환한다.

## Prerequisites

- Tutorial status: T20, T21
- Host: `mac/either`
- GPU: `optional`
- Hardware access: `none`
- Read first: `setup/06_LEROBOT.md`

## Concepts to explain

- episode schema
- feature metadata
- video encoding
- state/action normalization
- train/validation split

## Required implementation targets

- `src/pai_lab/data/lerobot_adapter.py`
- `examples/T28/create_dataset.py`
- `tests/T28/test_dataset_roundtrip.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. mac-lerobot 환경을 생성한다
2. FR3 scripted demonstration을 수집한다
3. feature shape/unit/frame을 metadata에 기록한다
4. dataset viewer 또는 custom visualization으로 검증한다

## Commands that must exist or be replaced by documented equivalents

- `pal dataset create T28 --episodes 20`
- `pal dataset inspect <dataset-path>`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- episode_montage.png
- state_action_alignment.png
- dataset_summary.md

Persist outputs under `outputs/T28/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 20개 episode round-trip
- [ ] frame/action timestamp alignment
- [ ] normalization stats 저장
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
