---
id: T10
title: "Contact and friction laboratory with cosmetic objects"
phase: "Contact"
host: "mac/either"
prerequisites: [T09]
gpu: "none"
hardware: "none"
---

# T10 — Contact and friction laboratory with cosmetic objects

## Objective

단순화한 캡·용기·테이블 contact scene을 만들고 sliding/torsional friction과 solver 설정의 영향을 측정한다.

## Prerequisites

- Tutorial status: T09
- Host: `mac/either`
- GPU: `none`
- Hardware access: `none`
- Read first: `START_HERE.md`

## Concepts to explain

- Coulomb friction
- normal and tangential force
- contact dimension
- solver softness
- timestep sensitivity

## Required implementation targets

- `assets/manufacturing/cap_bottle_scene.xml`
- `src/pai_lab/experiments/contact_lab.py`
- `examples/T10/contact_friction.py`
- `tests/T10/test_contact.py`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 원통 캡과 fingertip/contact pusher scene을 만든다
2. 한 번에 friction 한 항만 바꾼다
3. slip distance와 angular drift를 계산한다
4. timestep/solver 변화는 별도 실험으로 분리한다

## Commands that must exist or be replaced by documented equivalents

- `pal run T10 --experiment sliding-friction`
- `pal run T10 --experiment torsional-friction`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- slip_vs_friction.png
- angular_drift.png
- contact_force.png
- rollout.mp4

Persist outputs under `outputs/T10/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 마찰 증가에 대한 물리적으로 일관된 경향
- [ ] 접촉력과 미끄럼 단위 명시
- [ ] solver/timestep confound 분리
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
