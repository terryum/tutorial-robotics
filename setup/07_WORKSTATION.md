# WS2 and WS1 Workstation Audit

Inspect the actual host and current mode before changes. Both WS1 and WS2 can
use DEVELOPMENT; their names do not authorize work or imply installed tools.
Use the [remote setup guide](../docs/en/setup/remote-development/index.md)
([한국어](../docs/ko/setup/remote-development/index.md)) for incremental installation.
Historical SIM_TRAIN and ROBOT_INTEGRATION labels are replaced by the
current DEVELOPMENT and ROBOT_RUNTIME modes.

## WS1 or WS2 — DEVELOPMENT

Verify:

- Ubuntu 24.04.x and architecture
- GPU/VRAM, NVIDIA driver and CUDA compatibility
- RAM, disk and dataset/checkpoint locations
- Docker/NVIDIA Container Toolkit where required
- ROS 2 Jazzy environment for fake hardware and deployment parity
- separate Isaac vendor/modern, mjlab and LeRobot environments
- SSH/VS Code access from MacBook; optional GUI/Isaac streaming separately tested

Allowed:

- Isaac Sim/Lab
- MuJoCo Warp/MJX/mjlab
- G1/Wuji PPO
- ACT/VLA training and policy server
- synthetic data

Prohibited:

- real hardware command while training profile is active

## WS1 or WS2 — switching to ROBOT_RUNTIME

Switch only for a separately authorized runtime task. Do not terminate another
user's jobs or existing robot services during an installation audit. Before switching:

- stop and verify all training/Isaac batch processes
- deactivate ML environments
- activate only the selected host's isolated robot-runtime environment
- configure dedicated robot NIC and routes
- verify E-stop, watchdog and command sink
- connect one robot at a time


## WS1 or WS2 — ROBOT_RUNTIME

Verify:

- Ubuntu 24.04.x + ROS 2 Jazzy/vendor compatibility
- command arbitration and physical E-stop integration
- recorder and time synchronization
- policy inference runtime
- offline replay, shadow and rollback path

Do not copy WS2 binaries blindly. Rebuild target-specific native/TensorRT/ROS artifacts from the deployment bundle when required.

## Required outputs

Read-only audits do not create files. Authorized remote setup records belong in
`.local/remote-development/ws1/` or `.local/remote-development/ws2/`; maintain
existing local environment/capability records without overwriting learner state.
Publish only sanitized, actually measured evidence when publication is requested;
other hosts' ledger rows and historical reports remain unchanged.
