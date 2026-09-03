---
id: T23
title: "Minimal continuous-action PPO from scratch"
phase: "RL"
mode: "development"
requires: [dev_core, small_ml_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T22]
gpu: "none"
hardware: "none"
---

# T23 — Minimal continuous-action PPO from scratch

## Objective

작은 continuous-control 환경에서 rollout, GAE, clipped objective, value loss, entropy를 직접 구현한다.

## Prerequisites

- Tutorial status: T22
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- actor-critic
- advantage estimation
- PPO clipping
- Gaussian action distribution
- on-policy rollout

## Required implementation targets

- `src/pai_lab/rl/ppo/`
- `examples/T23/train_minimal_ppo.py`
- `tests/T23/test_ppo_math.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. Pendulum 또는 작은 reach 환경으로 시작한다
2. GAE와 clipped loss를 unit test한다
3. training/eval seed를 분리한다
4. checkpoint와 learning curve를 저장한다

## Commands that must exist or be replaced by documented equivalents

- `pal train T23 --steps 50000`
- `pal eval T23 --episodes 10`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- learning_curve.png
- policy_std.png
- eval_rollout.mp4

Persist outputs under `outputs/T23/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] loss unit tests 통과
- [ ] random baseline보다 개선
- [ ] NaN 없이 checkpoint 저장
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
