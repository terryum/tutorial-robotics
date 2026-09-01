---
id: T15
title: "Wuji contact sensing and virtual tactile observation"
phase: "Dexterous Hand"
host: "mac/either"
prerequisites: [T10, T14]
gpu: "none"
hardware: "none"
---

# T15 — Wuji contact sensing and virtual tactile observation

## Objective

MuJoCo contact를 fingertip별 virtual tactile observation으로 집계하고 실제 Beta 2 tactile과의 차이를 명확히 한다.

## Prerequisites

- Tutorial status: T10, T14
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- contact pairs
- normal/tangential force proxy
- sensor aggregation
- simulated vs real tactile

## Required implementation targets

- `src/pai_lab/sensors/virtual_tactile.py`
- `examples/T15/wuji_virtual_tactile.py`
- `tests/T15/test_virtual_tactile.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. fingertip body/site를 registry로 정의한다
2. contact force를 finger별로 집계한다
3. pinch force ramp와 slip event를 만든다
4. 실제 176-point tactile schema로 가는 adapter boundary를 정의한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T15 --task pinch-cylinder`
- `pal run T15 --task slip-test`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- finger_force.png
- contact_map.png
- slip_event.mp4

Persist outputs under `outputs/T15/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 접촉 없는 상태에서 near-zero
- [ ] 접촉 손가락만 force 상승
- [ ] virtual tactile이 실제 센서와 동일하지 않음을 report에 명시
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
