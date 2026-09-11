# Architecture — One Repository, Multiple Backends and Hosts

## 1. Runtime-independent stack

```text
Task / Evaluator / Policy
├─ Gymnasium adapter      PPO/RL
├─ LeRobot adapter        BC/ACT/VLA
└─ ROS 2 adapter          recorder and real robot
             │
        RobotBackend
   ┌─────────┼──────────┐
MuJoCo    Isaac Sim   Hardware
```

Host selection does not change this architecture. MacBook and WS2 operate on the same reusable modules and schemas.

## 2. Capability-first execution

```text
Git source revision + host-local learner progress
       │
       ├─ MacBook: portable subset
       ├─ WS2: portable subset + CUDA/Isaac/mjlab
       └─ WS1/isolated WS2: robot runtime
```

The same tutorial may be completed on either development host. Only simulator/vendor/hardware capability constrains placement.

## 3. Model truth separation

- URDF/Xacro: ROS tree, frames, joint limits and kinematics
- MJCF: MuJoCo dynamics, contact, actuators and sensors
- USD + Isaac config: scene composition, PhysX, camera and synthetic data
- hardware measurement: final dynamics, latency, calibration and noise evidence

Never declare automatic format conversion physically equivalent without cross-format and real validation.

## 4. Shared versus local state

Committed:

- code, tests, configs, reports
- reviewed publication evidence (never learner completion)
- source/model pins
- environment specs and hashes
- small deterministic evidence

Local only:

- virtual environments and caches
- absolute paths
- active host capability file
- secrets and robot network details

Large artifacts live outside normal Git and are referenced by manifest/hash.
