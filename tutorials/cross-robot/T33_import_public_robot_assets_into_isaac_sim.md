---
id: T33
title: "Import public robot assets into Isaac Sim"
phase: "Isaac"
mode: "development"
requires: [dev_core, ubuntu_24_04_x86_64, nvidia_cuda, isaac_sim_supported]
preferred_execution: "full-gpu-linux-host"
prerequisites: [T04]
gpu: "required"
hardware: "none"
---

# T33 — Import public robot assets into Isaac Sim

## Objective

native URDF/MJCF/USD를 Isaac용 USD로 가져오고 articulation, drives, mass, collision, frame을 검증한다.

## Prerequisites

- Tutorial status: T04
- Host profile: `WS2_SIM_TRAIN`
- GPU: `required`
- Hardware access: `none`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Read first: `setup/07_WORKSTATION.md`, `setup/08_ISAAC_STACKS.md`, `setup/09_REMOTE_VISUALIZATION.md`, `runbooks/WS2_SIM_TRAIN.md`

## Concepts to explain

- USD composition
- articulation root
- drive stiffness/damping
- URDF/MJCF importer
- asset validation

## Required implementation targets

- `generated_assets/isaac/`
- `workstation/T33/`
- `tests/T33/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 공식 Isaac example로 stack을 검증한다
2. FR3는 available USD 또는 import 경로를 선택한다
3. Unitree G1 articulation을 로드하고 floating-base contract를 확인한다
4. Wuji native USD를 로드한다
5. MuJoCo와 핵심 contract를 비교한다

## Commands that must exist or be replaced by documented equivalents

- `Isaac official asset import commands`
- `custom validation script`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- isaac_asset_previews/
- cross_format_fk.png
- asset_validation.md

Persist outputs under `outputs/T33/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] FR3, Unitree G1, Wuji articulation load 성공 또는 정확한 upstream blocker 기록
- [ ] joint count/frame/limit 비교
- [ ] 파생 asset provenance 저장
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
