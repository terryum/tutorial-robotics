---
id: T01
title: "MuJoCo hello world: pendulum state and timestep"
phase: "MuJoCo Basics"
host: "mac/either"
prerequisites: [T00]
gpu: "none"
hardware: "none"
---

# T01 — MuJoCo hello world: pendulum state and timestep

## Objective

작은 pendulum MJCF를 직접 만들고 `mjModel`, `mjData`, `qpos`, `qvel`, `ctrl`, `mj_step`의 관계를 코드와 그래프로 확인한다.

## Prerequisites

- Tutorial status: T00
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/02_MAC_CORE.md`

## Concepts to explain

- fixed model vs mutable state
- physics timestep
- passive dynamics
- viewer와 offscreen renderer

## Required implementation targets

- `assets/tutorial/T01/pendulum.xml`
- `examples/T01/pendulum_rollout.py`
- `tests/T01/test_pendulum.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. mac-core 환경을 생성·고정한다
2. pendulum XML과 loader를 만든다
3. 무제어 rollout을 실행한다
4. 각도와 각속도를 기록하고 energy sanity check를 수행한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T01 --headless --duration 8`
- `pal run T01 --viewer`
- `pytest tests/T01 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- angle_vs_time.png
- rollout.mp4

Persist outputs under `outputs/T01/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 모델 compile 성공
- [ ] qpos/qvel이 유한
- [ ] 저장된 frame이 비어 있지 않음
- [ ] timestep 변경 실험을 리포트에 기록
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
