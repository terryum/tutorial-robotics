---
id: T27
title: "Wuji in-hand PPO on NVIDIA workstation"
phase: "Dexterous RL"
mode: "development"
requires: [dev_core, ubuntu_24_04_x86_64, nvidia_cuda, mjlab_supported]
preferred_execution: "full-gpu-linux-host"
prerequisites: [T15, T23]
gpu: "required"
hardware: "none"
---

# T27 — Wuji in-hand PPO on NVIDIA workstation

## Objective

Wuji 공식 mjlab in-hand reorientation의 pretrained play와 작은 PPO training을 재현하고 Mac virtual tactile schema와 연결한다.

## Prerequisites

- Tutorial status: T15, T23
- Host profile: `WS2_SIM_TRAIN`
- GPU: `required`
- Hardware access: `none`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Read first: `setup/07_WORKSTATION.md`, `runbooks/WS2_SIM_TRAIN.md`

## Concepts to explain

- SO(3) goal
- in-hand reward
- mass/contact randomization
- ONNX export
- sim-to-real bridge

## Required implementation targets

- `workstation/T27/`
- `reports/T27_wuji_mjlab.md`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. Wuji repo가 요구하는 Pixi/CUDA 환경을 그대로 pin한다
2. pretrained checkpoint를 play한다
3. small smoke training을 수행한다
4. observation과 action을 local common schema에 mapping한다

## Commands that must exist or be replaced by documented equivalents

- `pixi run play --task WujiHand_Reorient ...`
- `pixi run train --task WujiHand_Reorient ...`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- wuji_training_curve.png
- reorientation.mp4
- schema_mapping.md

Persist outputs under `outputs/T27/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 공식 play 재현
- [ ] 작은 training이 checkpoint 생성
- [ ] 실제 hand 배포 명령은 실행하지 않음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
