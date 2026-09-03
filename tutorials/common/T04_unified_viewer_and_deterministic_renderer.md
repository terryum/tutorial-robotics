---
id: T04
title: "Unified viewer and deterministic renderer"
phase: "Visualization"
mode: "development"
requires: [dev_core, mujoco_supported, rendering_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T03]
gpu: "none"
hardware: "none"
---

# T04 — Unified viewer and deterministic renderer

## Objective

모델 ID 하나로 interactive viewer와 offscreen PNG/MP4를 실행하는 공통 시각화 CLI를 만든다.

## Prerequisites

- Tutorial status: T03
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `setup/04_MODEL_VALIDATION.md`, `docs/06_VISUALIZATION_STANDARD.md`

## Concepts to explain

- scene wrapper
- camera pose
- physics time vs render FPS
- deterministic replay

## Required implementation targets

- `src/pai_lab/visualization/viewer.py`
- `src/pai_lab/visualization/render.py`
- `tests/T04/test_render.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. vendor XML을 수정하지 않고 wrapper scene을 만든다
2. `pal model view`와 `pal model render`를 구현한다
3. camera와 keyframe을 metadata로 저장한다

## Commands that must exist or be replaced by documented equivalents

- `pal robot view fr3`
- `pal robot view wuji_hand2`
- `pal robot view unitree_g1`
- `pal model render franka_fr3_v2 --duration 3`
- `pytest tests/T04 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- 각 모델 preview PNG
- 짧은 deterministic MP4

Persist outputs under `outputs/T04/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 출력 해상도와 FPS 기록
- [ ] vendor 파일 미수정
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
