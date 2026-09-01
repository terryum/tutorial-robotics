---
id: T29
title: "Behavioral cloning baseline"
phase: "Imitation Learning"
host: "mac/either"
prerequisites: [T28]
gpu: "optional"
hardware: "none"
---

# T29 — Behavioral cloning baseline

## Objective

작은 MLP 또는 CNN+MLP BC를 학습해 데이터 파이프라인과 closed-loop compounding error를 이해한다.

## Prerequisites

- Tutorial status: T28
- Host: `mac/either`
- GPU: `optional`
- Hardware access: `none`
- Read first: `setup/06_LEROBOT.md`

## Concepts to explain

- supervised action prediction
- open-loop loss vs closed-loop success
- covariate shift
- normalization

## Required implementation targets

- `src/pai_lab/il/bc.py`
- `examples/T29/train_bc.py`
- `tests/T29/test_bc_smoke.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. state-only BC부터 시작한다
2. validation loss와 rollout success를 분리한다
3. action noise 또는 off-distribution start를 평가한다
4. CPU와 MPS tiny run을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal train T29 --device cpu`
- `pal eval T29 --episodes 20`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- bc_loss.png
- closed_loop_success.png
- bc_rollout.mp4

Persist outputs under `outputs/T29/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] training loss 감소
- [ ] closed-loop success 별도 보고
- [ ] device별 numerical 차이 기록
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
