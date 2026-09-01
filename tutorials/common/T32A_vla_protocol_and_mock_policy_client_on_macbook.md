---
id: T32A
title: "VLA protocol, small SmolVLA experiment, and policy client on MacBook"
phase: "VLA Foundation"
host: "macbook"
prerequisites: [T28]
gpu: "optional-mps"
hardware: "none"
---

# T32A — VLA protocol, small SmolVLA experiment, and policy client on MacBook

## Objective

language, multi-camera and robot state를 입력받아 action chunk를 반환하는 versioned policy server/client contract를 Mac에서 완성한다. 또한 현재 공식 LeRobot/SmolVLA stack을 audit하고, Mac arm64/MPS 또는 CPU에서 가능한 최소 processor/model-load/single-batch inference 실험을 실제로 시도한다. 대규모 fine-tuning은 WS2로 넘긴다.

## Concepts to explain

- language-conditioned observation
- processor/tokenizer/image ordering
- request/response schema and versioning
- asynchronous action chunking
- embodiment normalization
- timestamp, queue, timeout and stale-action rejection
- Mac inference smoke versus WS2 GPU fine-tuning

## Required implementation targets

- `src/pai_lab/vla/protocol.py`
- `src/pai_lab/vla/client.py`
- `src/pai_lab/vla/mock_server.py`
- `examples/T32A/language_task.py`
- `examples/T32A/smolvla_mac_smoke.py`
- `tests/T32A/`

## Execution procedure

1. Define versioned observation/action schema.
2. Implement a deterministic mock server and validate latency/timeout/drop behavior.
3. Audit the pinned official SmolVLA/LeRobot requirements for macOS arm64.
4. Load the official processor/config and inspect input/output tensor shapes.
5. Attempt one tiny real model inference on MPS, then CPU fallback if supported and memory-safe.
6. If official upstream cannot execute on Mac, record the exact blocker; do not substitute a mock and claim actual inference.
7. Connect the same client contract to the mock or verified real local endpoint.

## Commands

- `pal vla serve --mock`
- `pal run T32A --instruction "place the red cap in the left tray"`
- `pal vla smoke --model smolvla --device auto --max-memory-gb 18`

## Visualization contract

- `latency_timeline.png`
- `request_response_shapes.md`
- `processor_tensor_shapes.md`
- `mock_rollout.mp4`
- `mac_model_smoke.json`

## Acceptance criteria

- [ ] mock round-trip is deterministic and schema/version mismatch is rejected
- [ ] official SmolVLA processor/config path is audited and pinned
- [ ] real Mac inference result or exact reproducible upstream blocker is recorded without overclaiming
- [ ] memory use stays within the configured limit
- [ ] actual fine-tuning is explicitly deferred to T32C on WS2
- [ ] tests, report, outputs and state update exist
