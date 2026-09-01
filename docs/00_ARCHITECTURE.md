# System Architecture

## 1. Host architecture

```text
┌───────────────────────────────────────────────────────────┐
│ MacBook Pro M4 Pro                                        │
│ Codex · Git · Jupyter · MuJoCo · ROS 2 concepts · client │
└──────────────────────┬────────────────────────────────────┘
                       │ same Git repo / SSH / outputs
                       ▼
┌───────────────────────────────────────────────────────────┐
│ WS2 — Primary Simulation and Training                     │
│ Ubuntu 24.04.x · ROS 2 Jazzy cells · RTX                  │
│ mjlab · Isaac · ACT/VLA · synthetic data · model select  │
└──────────────────────┬────────────────────────────────────┘
                       │ deployment bundle + verified tag
                       ▼
┌───────────────────────────────────────────────────────────┐
│ WS1 — Default Real Robot Runtime                          │
│ Ubuntu 24.04.x · ROS 2 Jazzy · vendor drivers · safety   │
│ teleop · recorder · inference · gated autonomy            │
└──────────────────────┬────────────────────────────────────┘
                       ▼
```

Allowed alternative:

```text
WS2 → exclusive HARDWARE mode → real robots
```

In that mode, WS2 becomes the sole active command host. WS1 must be disabled or read-only for the same robot.

## 2. Target and reference embodiments

```text
Reference learning models             Real target platforms
G1 ────── whole-body concepts only ───→ system-level reasoning
Sharpa ── dexterous/tactile comparison → Wuji Hand 2

```

Reference models are not dynamically equivalent to the targets. Transfer occurs through common task, observation, action, evaluator, dataset, and deployment interfaces—not by blindly copying gains or policies.

## 3. Runtime layers

```text
[Native assets]
URDF / MJCF / USD / meshes / vendor metadata
        ↓
[Asset adapters]
path resolution, wrappers, joint maps, frame maps
        ↓
[Backends]
MuJoCo | Isaac Lab | ROS 2 fake | ROS 2 real | vendor SDK
        ↓
[Embodiment API]
reset / observe / step / stop / capabilities
        ↓
[Tasks]
reach, pick-place, carton pack, handover, reorientation
        ↓
[Policies]
scripted | PID/impedance | PPO | BC | ACT | VLA
        ↓
[Evaluation]
success, tracking error, force, cycle time, retries, safety
```

## 4. Generated source layout

```text
src/pai_lab/
├── assets/
├── backends/
├── control/
├── embodiments/
├── tasks/
├── data/
├── rl/
├── il/
├── vla/
└── visualization/
```

## 5. Host handoff boundary

WS2 does not send a bare checkpoint to the runtime host. The deployment artifact contains:

- checkpoint and rollback checkpoint
- model/policy config
- normalization statistics
- camera set/order
- state/action dimension and units
- policy/action frequency and horizon
- preprocessing/postprocessing code revision
- robot asset revision
- calibration requirement/version
- dataset manifest
- Git commit/tag
- environment lock/container digest
- simulation/sim-to-sim results
- expected test vectors and abort conditions

## 6. Important boundaries

- Asset conversion does not imply physical equivalence.
- A policy action rate does not replace a high-rate servo controller.
- ROS 2 message compatibility does not imply identical actuator semantics.
- A visually correct mesh does not imply correct inertia or contact.
- A training success curve does not imply manufacturing readiness.
- A network-reachable host does not automatically have command authority.
- A previous motion approval does not approve a new trajectory.
