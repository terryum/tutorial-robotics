# Architecture Decision Log

## ADR-001 — One repository, multiple environments

- Date: 2026-09-01
- Status: accepted
- Decision: MuJoCo, ROS 2, LeRobot, Isaac, mjlab, and hardware runtimes remain isolated.
- Reason: incompatible Python/CUDA/ROS/vendor dependencies and different safety properties.

## ADR-002 — G1 is the active humanoid reference

- Date: 2026-09-01
- Status: accepted
- Decision: use Unitree G1 29-DoF for tutorials; keep H2 Plus on watchlist.
- Reason: G1 currently has the more mature public training and deployment examples.

## ADR-003 — Wuji Beta 2 is the target hand revision

- Date: 2026-09-01
- Status: accepted
- Decision: model and hardware adapters must carry revision/firmware/tactile metadata.

Append new decisions rather than rewriting old ones. Mark superseded decisions explicitly.

## ADR-004 — Explicit MacBook → WS2 → runtime phase gates

- Date: 2026-09-01
- Status: accepted
- Decision: Mac foundations complete before WS2 training; WS2 candidate bundle and target-runtime offline validation complete before any real-hardware tutorial.
- Reason: shared progress alone does not prove local environment, reproducibility, runtime compatibility or safety.

## ADR-005 — WS2 has mutually exclusive SIM_TRAIN and ROBOT_INTEGRATION profiles

- Date: 2026-09-01
- Status: accepted
- Reason: one machine can serve both roles, but not concurrently without avoidable timing, dependency and safety risk.


- Date: 2026-09-01
- Status: accepted
- Reason: separate stable runtime from experimental training and simulation changes.
