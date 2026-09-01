---
id: T22
title: "Gymnasium FR3 reach environment"
phase: "RL"
host: "mac/either"
prerequisites: [T08, T21]
gpu: "none"
hardware: "none"
---

# T22 — Gymnasium FR3 reach environment

## Objective

FR3 reach를 명시적인 observation, action, reward, termination을 갖는 Gymnasium 환경으로 만든다.

## Prerequisites

- Tutorial status: T08, T21
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- MDP
- observation/action spaces
- reward shaping
- termination vs truncation
- evaluator

## Required implementation targets

- `src/pai_lab/rl/envs/fr3_reach.py`
- `examples/T22/fr3_reach_env.py`
- `tests/T22/test_env_checker.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 환경 계약과 seed reset을 구현한다
2. joint-delta action과 Cartesian goal observation을 정의한다
3. reward term을 분해해 로그한다
4. random/scripted policy baseline을 평가한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T22 --policy random`
- `pal run T22 --policy scripted`
- `pytest tests/T22 -q`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- reward_components.png
- success_distribution.png
- scripted_rollout.mp4

Persist outputs under `outputs/T22/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] Gymnasium checker 통과
- [ ] seed reproducibility
- [ ] success 정의가 evaluator와 일치
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
