---
id: T38
title: "Wuji Hand 2 Beta 2 hardware adapter and tactile calibration"
phase: "Hardware"
host: "ws2-robot-integration/ws1-robot-runtime"
prerequisites: [T15, T27, T36]
gpu: "optional"
hardware: "motion-approval"
---

# T38 — Wuji Hand 2 Beta 2 hardware adapter and tactile calibration

## Objective

Wuji joint와 tactile stream을 공통 schema에 연결하고, 승인 후 제한된 named pose와 가벼운 접촉을 검증한다.

## Prerequisites

- Tutorial status: T15, T27, T36
- Host profile: `WS2_ROBOT_INTEGRATION` preferred; `WS1_ROBOT_RUNTIME` allowed
- GPU: `optional`
- Hardware access: `motion-approval`
- Gates: `RUNTIME_OFFLINE_VALIDATED`, `ROBOT_READ_ONLY_VALIDATED_WUJI`
- Read first: `setup/07_WORKSTATION.md`, matching runtime runbook

## Concepts to explain

- Beta 2 revision
- tactile point layout
- normalization and units
- calibration
- joint/tactile synchronization

## Required implementation targets

- `src/pai_lab/hardware/wuji.py`
- `configs/hardware/wuji_hand2_beta2.yaml`
- `tests/T38/`

Codex may adjust filenames after inspecting the repository, but it must preserve the same separation of reusable module, thin example, test, output, and report.

## Execution procedure

1. serial/revision/firmware를 기록한다
2. read-only joint+tactile를 동기 기록한다
3. zero/contact calibration과 metadata를 저장한다
4. 승인 시 open→pinch named pose만 저속 수행한다

## Commands that must exist or be replaced by documented equivalents

- `pal hardware inspect wuji_hand2_beta2_right --read-only`
- `approved named-pose command only`

Every replacement command must be copied verbatim into the lesson report.

## Visualization contract

- tactile_baseline.png
- finger_contact.png
- sync_timeline.png

Persist outputs under `outputs/T38/<run-id>/` according to `docs/06_VISUALIZATION_STANDARD.md`. For GUI-limited sessions, create an offscreen artifact and provide the interactive command separately.

## Required explanation

The report must cover:

1. a concise mental model
2. equations, frame conventions, units, tensor shapes, or message semantics relevant to this lesson
3. source-code flow by file and symbol
4. one controlled parameter modification and the observed result, unless the lesson is pure setup
5. limitations and what cannot be inferred from simulation
6. direct relevance to FR3, Unitree G1, Wuji Hand 2, Sharpa Wave, or ALOHA

## Acceptance criteria

- [ ] Beta 2 sensor 존재 확인
- [ ] firmware별 scale/unit 기록
- [ ] approval 없이는 motion 없음
- [ ] Tests or smoke tests pass.
- [ ] Actual execution is verified.
- [ ] Persistent outputs and a Korean report exist.
- [ ] 승인된 named-pose/교정 범위가 완료된 경우 `WUJI_LOW_RISK_VALIDATED` gate와 evidence가 기록된다.
- [ ] `state/PROGRESS.md` and related state files are updated.

## Failure handling

Do not mark the tutorial complete when a dependency, GUI, GPU, or hardware is absent. Record the exact blocker and either leave it `pending-host` or mark it `blocked-retry`. Preserve partial code and failed output only when it helps reproduce the issue.

## Completion note

After completion, report the exact rerun command, output directory, key result, and next eligible tutorial. Do not automatically start the next tutorial in the same request unless the user explicitly asked for multiple steps.
