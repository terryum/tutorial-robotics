---
id: T42B
title: "Wuji cosmetics dexterity shadow and gated real evaluation"
phase: "Manufacturing Deployment"
host: "ws2-robot-integration/ws1-robot-runtime"
prerequisites: [T38, T42A]
gpu: "optional"
hardware: "motion-approval"
---

# T42B — Wuji cosmetics dexterity shadow and gated real evaluation

## Objective

T42A candidate를 Beta 2 실물 손에서 read-only tactile replay, no-motion shadow, approved named pose, calibration contact, one-object grasp/regrasp 순으로 평가한다.

## Mandatory sequence

1. verify hardware revision, firmware, tactile layout/unit/normalization and bundle hash
2. replay an offline episode
3. live-state/no-command shadow
4. named-pose approval
5. separate calibration-contact approval
6. separate single-object grasp/regrasp approval
7. record tactile, joint, visual, slip, retry and stop events

## Acceptance criteria

- [ ] each motion/contact scope has a separate run card
- [ ] tactile metadata is sufficient to reproduce normalization
- [ ] slip/regrasp outcome is labeled and synchronized with video
- [ ] no threaded screw-cap task is attempted under this initial gate
- [ ] failures return to WS2 for retraining; no runtime-host training
