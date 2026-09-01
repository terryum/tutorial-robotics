# WS2 and WS1 Workstation Audit

Do not treat all NVIDIA workstations as one generic host. Register the logical machine and profile first.

## WS2 — SIM_TRAIN

Verify:

- Ubuntu 24.04.x and architecture
- GPU/VRAM, NVIDIA driver and CUDA compatibility
- RAM, disk and dataset/checkpoint locations
- Docker/NVIDIA Container Toolkit where required
- ROS 2 Jazzy environment for fake hardware and deployment parity
- separate Isaac vendor/modern, mjlab and LeRobot environments
- SSH/WebRTC access from MacBook

Allowed:

- Isaac Sim/Lab
- MuJoCo Warp/MJX/mjlab
- G1/Wuji PPO
- ACT/VLA training and policy server
- synthetic data

Prohibited:

- real hardware command while training profile is active

## WS2 — ROBOT_INTEGRATION

Before switching:

- stop and verify all training/Isaac batch processes
- deactivate ML environments
- activate only `ws2-robot-runtime`
- configure dedicated robot NIC and routes
- verify E-stop, watchdog and command sink
- connect one robot at a time


## WS1 — ROBOT_RUNTIME

Verify:

- Ubuntu 24.04.x + ROS 2 Jazzy/vendor compatibility
- command arbitration and physical E-stop integration
- recorder and time synchronization
- policy inference runtime
- offline replay, shadow and rollback path

Do not copy WS2 binaries blindly. Rebuild target-specific native/TensorRT/ROS artifacts from the deployment bundle when required.

## Required outputs

Each machine creates `.local/HOST_PROFILE.md`, `.local/CAPABILITIES.md`, `.local/ENVIRONMENTS.md` and updates shared non-secret status in `state/ENVIRONMENTS.md`.
