---
id: T06
title: "FR3 joint-space PD control"
phase: "Manipulator Control"
mode: "development"
requires: [dev_core, mujoco_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T05]
gpu: "none"
hardware: "none"
---

# T06 — FR3 joint-space PD control

## Objective

joint-space PD controller를 구현하고 gain과 tracking error의 관계를 측정한다.

## Prerequisites

- Tutorial status: T05
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- position error
- velocity damping
- control saturation
- closed-loop response

## Required implementation targets

- `src/pai_lab/control/joint_pd.py`
- `examples/T06/fr3_joint_pd.py`
- `tests/T06/test_joint_pd.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. step target과 smooth target을 지원하는 PD를 구현한다
2. 토크/제어 범위를 제한한다
3. 낮은 damping과 높은 damping을 한 변수 비교한다
4. RMS·overshoot·settling proxy를 계산한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T06 --kp-scale 1.0 --kd-scale 1.0`
- `pal compare T06 --parameter kd_scale --values 0.5 2.0`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- joint_tracking.png
- control_effort.png
- rollout.mp4

Persist outputs under `outputs/T06/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] stable tracking
- [ ] saturation 기록
- [ ] 두 gain 실행의 동일 seed/target 보장
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
