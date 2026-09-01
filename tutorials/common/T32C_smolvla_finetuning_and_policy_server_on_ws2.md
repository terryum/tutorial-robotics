---
id: T32C
title: "SmolVLA fine-tuning and policy server on WS2"
phase: "VLA"
host: "ws2-sim-train"
prerequisites: [T32A]
gpu: "required"
hardware: "none"
---

# T32C — SmolVLA fine-tuning and policy server on WS2

## Objective

WS2에서 language-conditioned simulation dataset으로 SmolVLA 계열의 reproducible smoke fine-tuning과 inference server를 실행하고, T32A Mac client contract와 연결한다.

## Prerequisites

- Tutorial status: T32A, 
- Host profile: `WS2_SIM_TRAIN`
- GPU: required
- Hardware access: none
- Read first: `runbooks/WS2_SIM_TRAIN.md`, `setup/06_LEROBOT.md`

## Concepts to explain

- VLA processor/model/action head
- language and multi-camera ordering
- embodiment statistics and normalization
- fine-tuning versus inference
- synchronous versus asynchronous serving
- policy latency budget and action chunk continuity

## Required implementation targets

- `src/pai_lab/vla/server_contract.py`
- `workstation/T32C/`
- `tests/T32C/`
- `reports/T32C_smolvla.md`

## Execution procedure

1. pinned LeRobot/SmolVLA stack을 별도 환경에 설치·검증한다
2. pretrained load/inference smoke test를 수행한다
3. small simulated dataset fine-tuning을 실행한다
4. checkpoint와 processor/normalization을 함께 저장한다
5. local server round-trip을 검증한다
6. 가능하면 Mac client에서 network round-trip을 측정하되, 불가능하면 재현 명령을 제공한다

## Visualization contract

- `vla_training_curve.png`
- `server_latency_timeline.png`
- `language_conditioned_rollout.mp4`
- `instruction_failure_gallery.png`

## Acceptance criteria

- [ ] actual model load와 smoke fine-tuning을 검증한다
- [ ] mock과 actual server 결과를 구분한다
- [ ] camera/order/normalization mismatch를 검출한다
- [ ] checkpoint만이 아니라 processor와 schema를 versioning한다
- [ ] 실물 command는 실행하지 않는다
