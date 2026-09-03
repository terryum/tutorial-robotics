# Hardware and Simulation Safety

## Simulation is not a safety proof

A policy stable in MuJoCo or Isaac may fail because of wrong inertia, friction, latency, joint order/sign, frame convention, actuator semantics, saturation, sensor timing or model conversion.

## Cross-machine gates

Real-hardware work cannot start from tutorial code alone.

```text
GPU_CURRICULUM_READY
→ CANDIDATE_DEPLOYMENT_BUNDLE_READY
→ RUNTIME_OFFLINE_VALIDATED
→ robot-specific READ_ONLY_VALIDATED
→ separately approved low-energy command
→ separately approved contact/task evaluation
```

## Hardware gates

### Gate 0 — bundle and documentation

- deployment manifest/hash and rollback verified
- robot type, serial, hardware revision, firmware, SDK/driver recorded
- joint/frame/action schema reviewed
- payload/tool/mounting recorded
- offline deterministic inference and command-sink shadow test passed

### Gate 1 — physical readiness

- vendor E-stop procedure completed
- workspace cleared and bounded
- robot mechanically secured
- cables/adapters checked
- operator and observer roles assigned
- WS2 integration mode has no active training jobs

### Gate 2 — read-only

- connect without torque/motion
- inspect state topics/SDK streams and rates
- verify joint order, units, signs, timestamps and zero/reference pose
- verify safety/fault/watchdog state
- compare with simulation registry

### Gate 3 — low-energy free-space command

Requires explicit approval for the current run and exact robot/action.

- low speed, acceleration, current/force and workspace limits
- one subsystem, one joint, or small Cartesian displacement
- no object contact
- watchdog, command timeout and stop path verified

### Gate 4 — contact task

Requires a separate approval.

- calibrated tool/payload
- force/impedance limits
- collision/workspace boundaries
- recovery and retry budget
- human exclusion or collaborative-safety assessment
- failure capture and rollback

## Machine rules

- `DEVELOPMENT`: no real hardware command.
- `ROBOT_RUNTIME`: all training/Isaac batch processes stopped; one robot at a time.
- `ROBOT_RUNTIME`: validated bundle only; no large retraining.
- MacBook remote access does not bypass the hardware gate.

## Prohibited autonomous actions

Codex must not autonomously update firmware, enable torque, bypass interlocks, raise limits, disable collision checks, issue unapproved motion, or promote a policy to production.
