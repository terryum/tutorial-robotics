---
id: T36
title: "Real-hardware read-only integration gate"
phase: "Hardware"
host: "ws1-robot-runtime/ws2-robot-integration"
prerequisites: [T35B]
gpu: "none"
hardware: "read-only"
repeatable: true
---

# T36 — Real-hardware read-only integration gate

## Objective

Validate an explicitly selected public robot adapter in read-only mode and
record identity, safety state, limits, timeouts, and command-sink behavior.

## Prerequisites

- Tutorial status: T35B
- Host profile: `WS1_ROBOT_RUNTIME` or `WS2_ROBOT_INTEGRATION`
- GPU: `none`
- Hardware access: `read-only`
- Gates: `WS2_DEPLOYMENT_BUNDLE_READY`, `RUNTIME_OFFLINE_VALIDATED`
- Read first: `setup/07_WORKSTATION.md`, matching runtime runbook

## Concepts to explain

- read-only driver
- watchdog
- joint contract
- timestamp integrity
- hardware run card

## Required implementation targets

- `src/pai_lab/hardware/read_only.py`
- `templates/generated_hardware_cards/`
- `tests/T36/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. 한 번에 한 로봇만 선택한다
2. hardware-gate skill을 실행한다
3. state를 10초 이상 기록한다
4. simulation registry와 joint map을 비교한다

## Commands that must exist or be replaced by documented equivalents

- `pal hardware inspect <robot-id> --read-only`
- `pal tutorial run T36 --robot <robot-id>`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- state_rate.png
- joint_order_report.md
- hardware_run_card.md

Persist outputs under `outputs/T36/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] 어떠한 motion command도 발행하지 않음
- [ ] E-stop/safety state 기록
- [ ] unit/order/timestamp 검증
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] 해당 robot-specific read-only gate와 evidence가 갱신된다.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.

## Repeatable-target rule

이 tutorial의 공통 구현이 `done`이어도 새 실물 target의 read-only gate가 없으면 같은 T36을 `--robot` 인자로 다시 실행한다. `$run-next-tutorial`은 활성 runtime plan에 필요한 robot gate가 빠져 있으면 /T38/보다 T36 재실행을 우선 제안한다.
