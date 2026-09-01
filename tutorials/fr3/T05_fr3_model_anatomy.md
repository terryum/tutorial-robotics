---
id: T05
title: "FR3 model anatomy"
phase: "Manipulator Control"
host: "mac/either"
prerequisites: [T04]
gpu: "none"
hardware: "none"
---

# T05 — FR3 model anatomy

## Objective

FR3 v2의 7축 구조, frame, joint range, actuator, inertia와 end-effector site를 코드로 탐색한다.

## Prerequisites

- Tutorial status: T04
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- serial-chain kinematics
- mass and inertia
- joint limit
- site/frame conventions

## Required implementation targets

- `examples/T05/fr3_anatomy.py`
- `src/pai_lab/embodiments/fr3.py`
- `tests/T05/test_fr3_contract.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. joint와 link 순서를 이름 기반으로 정의한다
2. 세 개 deterministic pose의 FK 정보를 기록한다
3. actuator와 controllable joint map을 검증한다
4. 기준 자세와 joint axis를 시각화한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T05`
- `pytest tests/T05 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- fr3_joint_axes.png
- fr3_pose_table.md

Persist outputs under `outputs/T05/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 7개 arm joint 계약 확인
- [ ] frame convention 명시
- [ ] joint index 하드코딩이 adapter 밖에 없음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
