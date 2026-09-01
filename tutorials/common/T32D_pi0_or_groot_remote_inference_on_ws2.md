---
id: T32D
title: "Optional π₀ or GR00T remote inference on WS2"
phase: "VLA Advanced"
host: "ws2-sim-train"
prerequisites: [T32C]
gpu: "required"
hardware: "none"
optional: true
---

# T32D — Optional π₀ or GR00T remote inference on WS2

## Objective

current official support, license and hardware requirements를 audit한 뒤 π₀/OpenPI 또는 NVIDIA GR00T 중 한 경로의 **inference-only** remote server를 WS2에서 재현하고 T32A client contract와 비교한다. 초기 커리큘럼의 필수 gate는 아니다.

## Concepts to explain

- model/processor/embodiment adapter boundary
- inference memory and latency
- action chunk semantics and normalization
- license/model-access restrictions

## Execution procedure

1. Audit only official documentation/repositories and select one feasible path.
2. Pin code/model revision and record license/access conditions.
3. Run official sample inference before any custom adapter.
5. Measure VRAM, latency and output schema.
6. Compare with SmolVLA using the same client-side timing/evaluator where possible.
7. Do not fine-tune or connect to hardware unless a later explicit project authorizes it.

## Outputs

- `advanced_vla_upstream_audit.md`
- `inference_memory_latency.json`
- `schema_comparison.md`
- `remote_inference_smoke.mp4` or deterministic trace

## Acceptance criteria

- [ ] official sample inference works, or exact access/support blocker is recorded
- [ ] no hardware command path exists
- [ ] model-specific adapter does not alter the common client contract silently
- [ ] optional status is preserved; failure does not block T35A
