---
id: T07
title: "Gravity compensation and feedforward"
phase: "Manipulator Control"
mode: "development"
requires: [dev_core, mujoco_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T06]
gpu: "none"
hardware: "none"
---

# T07 — Gravity compensation and feedforward

## Objective

PD-only와 inverse-dynamics gravity feedforward를 비교해 steady-state error와 effort를 이해한다.

## Prerequisites

- Tutorial status: T06
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- inverse dynamics
- gravity torque
- feedback vs feedforward
- model error

## Required implementation targets

- `src/pai_lab/control/gravity.py`
- `examples/T07/fr3_gravity_comp.py`
- `tests/T07/test_gravity_comp.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. MuJoCo inverse dynamics에서 gravity 항을 구한다
2. PD-only와 PD+gravity를 같은 자세에서 비교한다
3. payload mass perturbation으로 model mismatch를 만든다
4. error와 torque를 기록한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T07 --mode pd`
- `pal run T07 --mode pd-gravity`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- steady_state_error.png
- gravity_torque.png
- comparison.mp4

Persist outputs under `outputs/T07/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] gravity feedforward가 정의된 실험에서 error를 줄임
- [ ] payload mismatch 한계를 설명
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
