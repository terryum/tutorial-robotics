---
id: T35
title: "MuJoCo–Isaac sim-to-sim validation"
phase: "Sim-to-Sim"
host: "ws2-sim-train"
prerequisites: [T24, T33]
gpu: "required"
hardware: "none"
---

# T35 — MuJoCo–Isaac sim-to-sim validation

## Objective

동일 FR3 trajectory/controller 또는 policy를 MuJoCo와 Isaac에서 실행해 차이를 정량화한다.

## Prerequisites

- Tutorial status: T24, T33
- Host profile: `WS2_SIM_TRAIN`
- GPU: `required`
- Hardware access: `none`
- Gate: `MACBOOK_FOUNDATION_COMPLETE`
- Read first: `setup/07_WORKSTATION.md`, `setup/08_ISAAC_STACKS.md`, `setup/09_REMOTE_VISUALIZATION.md`, `runbooks/WS2_SIM_TRAIN.md`

## Concepts to explain

- physics backend gap
- controller semantics
- contact solver differences
- parameter identification target

## Required implementation targets

- `workstation/T35/`
- `reports/T35_sim2sim.md`
- `tests/T35/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 동일 initial state/target/control rate를 정의한다
2. 가능한 공통 high-level action을 사용한다
3. free-space tracking부터 비교한다
4. 그 다음 단순 contact 실험을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal sim2sim T35 --task free-space`
- `pal sim2sim T35 --task contact`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- backend_tracking_comparison.png
- contact_difference.png
- paired_rollouts.mp4

Persist outputs under `outputs/T35/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] backend별 timestep/controller 기록
- [ ] 숫자만 맞춰 동일하다고 가정하지 않음
- [ ] 차이를 parameter-identification backlog로 변환
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
