---
id: T08
title: "FR3 forward kinematics, Jacobian, and inverse kinematics"
phase: "Manipulator Control"
host: "mac/either"
prerequisites: [T07]
gpu: "none"
hardware: "none"
---

# T08 — FR3 forward kinematics, Jacobian, and inverse kinematics

## Objective

FK와 Jacobian을 MuJoCo API와 수치미분으로 교차 검증하고 damped least-squares IK를 구현한다.

## Prerequisites

- Tutorial status: T07
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- SE(3)
- quaternion convention
- geometric Jacobian
- singularity and damping
- null space

## Required implementation targets

- `src/pai_lab/control/kinematics.py`
- `src/pai_lab/control/ik.py`
- `examples/T08/fr3_ik.py`
- `tests/T08/test_kinematics.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. end-effector pose API를 만든다
2. Jacobian을 finite difference로 검증한다
3. DLS IK와 joint-limit handling을 구현한다
4. reachable/unreachable target을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T08 --trajectory circle`
- `pytest tests/T08 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- ee_path_3d.png
- ik_error.png
- joint_trajectory.png
- rollout.mp4

Persist outputs under `outputs/T08/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] Jacobian 검증 오차 기준 통과
- [ ] reachable target 수렴
- [ ] unreachable target이 안전하게 종료
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
