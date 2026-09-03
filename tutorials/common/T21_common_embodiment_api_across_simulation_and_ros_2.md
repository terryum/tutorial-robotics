---
id: T21
title: "Common embodiment API across simulation and ROS 2"
phase: "Architecture"
mode: "development"
requires: [dev_core, mujoco_supported, ros2_core_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T15, T19]
gpu: "none"
hardware: "none"
---

# T21 — Common embodiment API across simulation and ROS 2

## Objective

Define a typed public embodiment API and validate it across FR3, Wuji Hand 2,
and simulation-backed ROS 2 without erasing robot-specific capabilities.

## Prerequisites

- Tutorial status: T15, T19
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- protocol and capabilities
- typed observation/action
- backend abstraction
- unsupported operation handling

## Required implementation targets

- `src/pai_lab/embodiments/base.py`
- `src/pai_lab/schemas/`
- `tests/T21/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. typed schema와 capability flags를 정의한다
2. MuJoCo backend 세 개를 adapter로 감싼다
3. unsupported action이 명확한 오류를 내게 한다
4. same task spec을 로봇별로 instantiate한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T21 --smoke-all`
- `pytest tests/T21 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- architecture_graph.md
- capability_matrix.md

Persist outputs under `outputs/T21/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 세 backend가 공통 smoke contract 통과
- [ ] shape/unit/frame metadata 존재
- [ ] raw vendor semantics를 과도하게 평준화하지 않음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
