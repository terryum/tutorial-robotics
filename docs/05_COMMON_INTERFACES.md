# Common Interfaces

## 1. Embodiment backend

```python
class RobotBackend(Protocol):
    @property
    def capabilities(self) -> RobotCapabilities: ...
    def reset(self, seed: int | None = None) -> Observation: ...
    def observe(self) -> Observation: ...
    def step(self, action: Action) -> StepResult: ...
    def stop(self) -> None: ...
```

Expected concrete boundaries:

```text
MujocoBackend
IsaacBackend
Ros2Backend
WujiBackend
```

Policies must not import vendor SDKs directly.

## 2. Canonical observations

```text
timestamp_ns
joint.position [rad or m]
joint.velocity [rad/s or m/s]
joint.effort [N·m or N]
base.pose
ee.left.pose
ee.right.pose
camera.front.rgb
camera.left_wrist.rgb
camera.right_wrist.rgb
camera.<name>.depth
tactile.left
tactile.right
safety.*
language.instruction
```

Every feature declares shape, order, dtype, unit, frame, rate, timestamp source, normalization and validity mask. A robot that lacks a feature declares it absent in the schema; it is not silently filled with zeros.

## 3. Canonical high-level actions

Initial common actions:

- `joint_position`
- `joint_delta`
- `ee_delta_pose`
- `base_twist`
- robot-specific hand synergy or named hand pose

Raw torque is not a universal high-level action. It requires robot-specific safety, control rate, gravity semantics and limits.

## 4. Rate boundary

A learned policy or VLA commonly produces a target/action chunk at roughly 10–30 Hz. The robot adapter converts that output to the vendor trajectory/impedance interface. The policy never replaces the robot's high-rate servo, which may run at hundreds of Hz or around 1 kHz.

```text
VLA / ACT / learned policy       10–30 Hz typical
        ↓ action chunk / target
robot-specific adapter           interpolation, limits, watchdog
        ↓
vendor controller / servo        high-rate closed loop
```

Every adapter must reject stale timestamps, wrong action dimensions, NaN/Inf, out-of-range targets and mode mismatches.

## 5. Dataset policy

The episode schema separates raw and derived data.

- `raw/`: synchronized sensor and command values
- `derived/`: FK poses, contact labels, task phase, normalized tensors
- `metadata/`: model commit, hardware revision, firmware, calibration, units, camera intrinsics

A policy-specific processor and normalization transform must be versioned with the checkpoint.
