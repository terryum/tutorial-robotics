---
id: T24
title: "PPO on FR3 reach"
phase: "RL"
mode: "development"
requires: [dev_core, mujoco_supported, small_ml_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T23]
gpu: "none"
hardware: "none"
---

# T24 — PPO on FR3 reach

## Objective

직접 구현한 PPO를 FR3 reach에 적용하고 reward/observation 설계가 학습에 미치는 영향을 비교한다.

## Prerequisites

- Tutorial status: T23
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- sample efficiency
- reward scale
- normalization
- domain randomization
- policy evaluation

## Required implementation targets

- `examples/T24/train_fr3_ppo.py`
- `configs/rl/fr3_reach_ppo.yaml`
- `tests/T24/test_training_smoke.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 작은 환경 수와 짧은 smoke training을 먼저 수행한다
2. baseline config를 고정한다
3. reward term 하나의 ablation을 수행한다
4. 5개 seed full run은 workstation 옵션으로 둔다

## Commands that must exist or be replaced by documented equivalents

- `pal train T24 --config configs/rl/fr3_reach_ppo.yaml --smoke`
- `pal eval T24 --checkpoint <path>`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- fr3_learning_curve.png
- seed_table.md
- ppo_rollout.mp4

Persist outputs under `outputs/T24/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] scripted/random/PPO 비교
- [ ] smoke training 재현
- [ ] checkpoint normalization metadata 저장
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
