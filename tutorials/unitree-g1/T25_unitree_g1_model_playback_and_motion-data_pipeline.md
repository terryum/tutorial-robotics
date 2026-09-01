---
id: T25
title: "Unitree G1 model playback and motion-data pipeline"
phase: "Humanoid"
host: "mac/either"
prerequisites: [T03, T04]
gpu: "none"
hardware: "none"
---

# T25 — Unitree G1 model playback and motion-data pipeline

## Objective

G1 모델, floating-base state, motion file, reference pose tracking 데이터 흐름을 학습하되 대규모 PPO는 실행하지 않는다.

## Prerequisites

- Tutorial status: T03, T04
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- floating base
- root pose and IMU
- motion resampling
- reference tracking
- sim-to-sim deployment shape

## Required implementation targets

- `src/pai_lab/embodiments/unitree_g1.py`
- `examples/T25/g1_motion_playback.py`
- `tests/T25/test_motion_conversion.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 선택한 G1 모델 path와 DoF variant를 고정한다
2. reference CSV/NPZ 형식을 작은 synthetic motion으로 재현한다
3. pose sequence를 playback한다
4. observation/action tensor shape를 문서화한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T25 --motion synthetic-squat`
- `pytest tests/T25 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- root_and_joint_motion.png
- g1_playback.mp4
- tensor_schema.md

Persist outputs under `outputs/T25/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 모션 resampling 일관성
- [ ] floating-base quaternion normalization
- [ ] Mac에서 training을 시도하지 않음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
