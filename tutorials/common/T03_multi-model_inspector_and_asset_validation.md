---
id: T03
title: "Multi-model inspector and asset validation"
phase: "Assets"
mode: "development"
requires: [dev_core, mujoco_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T01, T02]
gpu: "none"
hardware: "none"
---

# T03 — Multi-model inspector and asset validation

## Objective

Inspect FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, and ALOHA assets through one
read-only interface while preserving each upstream model's native semantics.

## Prerequisites

- Tutorial status: T01, T02
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/04_MODEL_VALIDATION.md`, `docs/06_VISUALIZATION_STANDARD.md`

## Concepts to explain

- joint vs DoF vs qpos/qvel dimension
- fixed/free base
- actuator mapping
- asset compiler warning

## Required implementation targets

- `src/pai_lab/assets/inspect.py`
- `examples/T03/inspect_models.py`
- `tests/T03/test_model_inventory.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. format별 loader를 구현하고 unresolved file과 compiler warning을 분류한다
2. body/link/joint/actuator/sensor/camera inventory를 registry와 비교한다
3. joint name, lower/upper limit, unit, axis와 fixed/free/mobile-base semantics를 검증한다
4. default/named pose의 unintended self-collision과 environment penetration을 검사한다
5. deterministic 10-second passive/held simulation에서 NaN, Inf, numerical explosion을 검사한다
6. rigid-body mass/inertia와 total-mass expected range를 검증한다
7. actuator order, control dimension, actuator-to-joint mapping을 검증한다
8. left/right sign, mirror, naming convention을 검증한다
9. 가능한 모델은 URDF↔MJCF FK를 최소 세 deterministic pose에서 비교한다
10. USD가 있는 모델은 WS2 T33/T35에서 같은 pose의 USD↔MJCF 비교를 끝낼 수 있도록 pending evidence를 생성한다
11. model별 warning, capability, unavailable format과 tolerance를 기록한다

## Commands that must exist or be replaced by documented equivalents

- `pal model inspect franka_fr3_v2`
- `pal run T03`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- model_counts.csv
- model_comparison.png
- model_inventory.md

Persist outputs under `outputs/T03/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] `setup/04_MODEL_VALIDATION.md`의 mandatory ten checks가 model별 evidence에 연결됨
- [ ] 각 available MJCF가 compile되고 deterministic 10-second stability test가 통과함
- [ ] mass/inertia, actuator mapping, bilateral convention, self-collision 결과가 기록됨
- [ ] URDF↔MJCF FK 비교가 가능한 모델에서 수행됨
- [ ] USD 비교가 필요한 항목은 T33/T35 pending evidence로 명시됨
- [ ] unavailable format은 명시적 상태로 남음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
