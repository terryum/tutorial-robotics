---
id: T35B
title: "Robot runtime bootstrap, offline replay, and shadow dry-run"
phase: "Runtime Handoff"
host: "ws1-robot-runtime/ws2-robot-integration"
prerequisites: [T35A]
gpu: "optional-for-inference"
hardware: "none-or-read-only"
---

# T35B — Robot runtime bootstrap, offline replay, and shadow dry-run

## Objective

WS2 candidate bundle을 WS1 또는 WS2 robot-integration profile에서 target runtime으로 재구축하고, 실제 command sink를 차단한 상태에서 offline replay와 shadow dry-run을 검증한다.

## Prerequisites

- Tutorial status: T35A
- Gate: `WS2_DEPLOYMENT_BUNDLE_READY`
- Host profile: `WS1_ROBOT_RUNTIME` or `WS2_ROBOT_INTEGRATION`
- Read first: matching runtime runbook and `runbooks/HANDOFF_AND_SYNC.md`

## Concepts to explain

- target-runtime rebuild
- artifact integrity
- offline replay
- shadow mode and command sink
- schema/rate/timestamp validation
- rollback

## Required implementation targets

- `src/pai_lab/deployment/bundle_loader.py`
- `src/pai_lab/deployment/command_sink.py`
- `tests/T35B/`
- `reports/T35B_runtime_validation.md`

## Execution procedure

1. manifest와 모든 hash를 검증한다
2. WS2 native binary를 그대로 신뢰하지 않고 target 환경에서 필요한 component를 rebuild한다
3. deterministic test vector inference를 비교한다
4. recorded episode offline replay를 수행한다
5. hardware command publisher를 sink/mock으로 대체한 shadow dry-run을 실행한다
6. 성공 시 `RUNTIME_OFFLINE_VALIDATED` gate를 갱신한다

## Visualization contract

- `expected_vs_runtime_output.png`
- `latency_budget.png`
- `shadow_command_trace.png`
- `runtime_environment.json`

## Acceptance criteria

- [ ] bundle hash와 runtime environment가 기록된다
- [ ] expected output tolerance를 만족한다
- [ ] command가 실제 hardware topic/SDK로 전달되지 않는다
- [ ] rollback load test가 통과한다
- [ ] `RUNTIME_OFFLINE_VALIDATED` gate가 evidence와 함께 갱신된다
