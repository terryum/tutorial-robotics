---
id: T14
title: "Wuji Hand 2 joints, named poses, and synergies"
phase: "Dexterous Hand"
mode: "development"
requires: [dev_core, mujoco_supported]
preferred_execution: "portable-or-full-development-host"
prerequisites: [T04]
gpu: "none"
hardware: "none"
---

# T14 — Wuji Hand 2 joints, named poses, and synergies

## Objective

Wuji Hand 2 Beta 2의 20개 관절과 fingertip frame을 이해하고 open, pinch, power grasp synergy를 만든다.

## Prerequisites

- Tutorial status: T04
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- hand joint groups
- coupled motion vs independent DoF
- fingertip frames
- joint range and self-collision

## Required implementation targets

- `src/pai_lab/embodiments/wuji.py`
- `src/pai_lab/control/hand_synergy.py`
- `examples/T14/wuji_synergies.py`
- `tests/T14/test_wuji_contract.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. pinned `wuji-technology/mujoco-sim` 또는 당시 공식 minimal MuJoCo example을 먼저 재현하고 exact command와 output을 기록한다
2. right-hand Beta 2 model revision과 description commit을 확인해 joint map을 만든다
3. 손가락별 천천히 굽히기 테스트를 수행한다
4. 세 개 named pose/synergy를 정의한다
5. joint limit과 collision을 검사한다
6. official playback trajectory와 자체 synergy trajectory의 joint order와 units를 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T14 --sequence all`
- `pal model view wuji_hand2_beta2_right`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- wuji_joint_groups.md
- synergy_trajectory.png
- synergies.mp4

Persist outputs under `outputs/T14/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] official minimal Wuji MuJoCo example이 Mac에서 재현되거나 정확한 upstream blocker가 기록됨
- [ ] Beta 2 model revision/commit과 20 controllable joint 계약 확인
- [ ] 각 named pose가 limit 내
- [ ] 손가락 sign/순서 기록
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
