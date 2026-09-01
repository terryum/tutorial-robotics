---
id: T16
title: "Wuji versus Sharpa model comparison"
phase: "Dexterous Hand"
host: "mac/either"
prerequisites: [T14]
gpu: "none"
hardware: "none"
---

# T16 — Wuji versus Sharpa model comparison

## Objective

Wuji와 Sharpa의 DoF, joint range, frame, actuator, tactile geometry, model formats를 동일 도구로 비교한다.

## Prerequisites

- Tutorial status: T14
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- cross-embodiment comparison
- morphology
- action-space mismatch
- benchmark vs target platform

## Required implementation targets

- `examples/T16/compare_hands.py`
- `tests/T16/test_hand_comparison.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 두 모델 inventory를 동일 schema로 변환한다
2. fingertip workspace를 sample한다
3. named pose를 morphology별로 정의한다
4. 공통 task와 비공통 action을 구분한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T16`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- hand_comparison.md
- fingertip_workspace.png
- side_by_side.mp4

Persist outputs under `outputs/T16/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 두 모델의 source commit 기록
- [ ] joint를 단순 index로 직접 대응하지 않음
- [ ] task-level transfer와 policy-level transfer 구분
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
