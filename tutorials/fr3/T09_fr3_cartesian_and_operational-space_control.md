---
id: T09
title: "FR3 Cartesian and operational-space control"
phase: "Manipulator Control"
mode: "development"
requires: [dev_core, mujoco_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T08]
gpu: "none"
hardware: "none"
---

# T09 — FR3 Cartesian and operational-space control

## Objective

task-space pose error를 joint torque 또는 joint target으로 변환하고 null-space posture와 함께 제어한다.

## Prerequisites

- Tutorial status: T08
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- task-space error
- operational-space control
- Cartesian stiffness/damping
- null-space projection

## Required implementation targets

- `src/pai_lab/control/task_space.py`
- `examples/T09/fr3_task_space.py`
- `tests/T09/test_task_space.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. position/orientation error를 일관된 frame에서 계산한다
2. Cartesian PD와 Jacobian transpose 제어를 구현한다
3. null-space posture 항을 추가한다
4. 원·직선·8자 궤적을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T09 --trajectory figure8`
- `pal compare T09 --parameter stiffness_scale --values 0.5 1.5`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- task_space_tracking.png
- orientation_error.png
- rollout.mp4

Persist outputs under `outputs/T09/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] frame/단위 명시
- [ ] 안정된 궤적 추종
- [ ] null-space 항이 end-effector 목표를 크게 훼손하지 않음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
