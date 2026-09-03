---
id: T34
title: "Isaac camera, lighting, and synthetic manufacturing dataset"
phase: "Isaac"
mode: "development"
requires: [dev_core, ubuntu_24_04_x86_64, nvidia_cuda, isaac_sim_supported]
preferred_execution: "full-gpu-linux-host"
prerequisites: [T33]
gpu: "required"
hardware: "none"
---

# T34 — Isaac camera, lighting, and synthetic manufacturing dataset

## Objective

화장품 캡·용기·단상자 scene에서 RGB/depth/segmentation과 domain variation을 생성한다.

## Prerequisites

- Tutorial status: T33
- Host profile: `WS2_SIM_TRAIN`
- GPU: `required`
- Hardware access: `none`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Read first: `setup/07_WORKSTATION.md`, `setup/08_ISAAC_STACKS.md`, `setup/09_REMOTE_VISUALIZATION.md`, `runbooks/WS2_SIM_TRAIN.md`

## Concepts to explain

- camera intrinsics/extrinsics
- RTX rendering
- domain randomization
- segmentation labels
- synthetic-to-real limits

## Required implementation targets

- `workstation/T34/`
- `assets/manufacturing/isaac_scene/`
- `tests/T34/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 작은 table scene을 만든다
2. front/wrist camera를 배치한다
3. lighting/material/object pose를 분리 randomize한다
4. dataset sample과 metadata를 저장한다

## Commands that must exist or be replaced by documented equivalents

- `Isaac headless dataset generation command`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- rgb_grid.png
- depth_grid.png
- segmentation_grid.png

Persist outputs under `outputs/T34/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] camera calibration metadata 존재
- [ ] seed 재현
- [ ] label/object correspondence 검증
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
