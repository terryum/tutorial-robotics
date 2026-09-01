---
id: T42A
title: "Wuji cosmetics dexterity simulation and candidate bundle"
phase: "Manufacturing Training"
host: "ws2-sim-train"
prerequisites: [T16A, T27, T32C, T35A]
gpu: "required"
hardware: "none"
---

# T42A — Wuji cosmetics dexterity simulation and candidate bundle

## Objective

Wuji Hand 2용 화장품 dexterity task를 simulation과 demonstration data로 구성하고 tactile-aware evaluator와 candidate bundle을 만든다.

## Task ladder

1. pick a cap
2. orient the cap
3. place it at a bottle opening
4. push-fit cap insertion
5. orient a pump head
6. regrasp a pouch/tube or small part
7. grasp a carton flap

A full threaded screw-cap task is deferred until grasp/regrasp/contact stages are reliable.

## Required outputs

- retargeted and scripted demonstration dataset
- visual-only versus visual+virtual-tactile ablation where feasible
- slip/regrasp/contact-state evaluator
- task-specific domain randomization
- candidate policy/config/processor/schema/rollback bundle

## Acceptance criteria

- [ ] task and tactile observation do not assume simulated force equals Beta 2 sensor output
- [ ] joint/tactile order, scale and timestamps are versioned
- [ ] regrasp and slip have explicit labels
- [ ] threaded cap closure is not silently included
- [ ] `WUJI_COSMETICS_CANDIDATE_READY` gate is created
