# Environment Matrix

## Principle

Use one repository with machine-specific isolated environments. Never solve dependency conflicts by repeatedly upgrading one environment, and never copy a virtual environment between MacBook, WS2 and WS1.

| Environment | Logical host/profile | Main purpose | Baseline policy |
|---|---|---|---|
| `mac-core` | MACBOOK / MACBOOK_FOUNDATION | MuJoCo, control, Gymnasium, small PPO, rendering | macOS arm64; Python 3.12; pinned MuJoCo |
| `mac-ros2` | MACBOOK / MACBOOK_FOUNDATION | ROS 2 concepts, messages, TF, rosbag | Pixi + RoboStack Jazzy; CycloneDDS preferred |
| `mac-lerobot` | MACBOOK / MACBOOK_FOUNDATION | dataset, BC, ACT smoke, VLA mock client | separate Python/PyTorch/LeRobot lock |
| `ws2-ros2-sim` | WS2 / WS2_SIM_TRAIN | Jazzy, fake hardware, MoveIt/description parity | Ubuntu 24.04.x + ROS 2 Jazzy |
| `ws2-isaac-vendor` | WS2 / WS2_SIM_TRAIN | reproduce Unitree/Sharpa/Wuji vendor examples | exact vendor-compatible Isaac pair; no in-place upgrade |
| `ws2-isaac-modern` | WS2 / WS2_SIM_TRAIN | current Isaac research and custom USD scenes | separate from vendor stack |
| `ws2-mjlab` | WS2 / WS2_SIM_TRAIN | MuJoCo Warp/mjlab large PPO | pinned Python/CUDA per Unitree/Wuji requirements |
| `ws2-lerobot` | WS2 / WS2_SIM_TRAIN | ACT/VLA scale-up and policy server | pinned GPU PyTorch/LeRobot stack |

## Machine role boundary

### MacBook

- local MuJoCo and small learning experiments
- no local Isaac Sim
- no hardware low-level runtime
- remote SSH/WebRTC/dashboard client

### WS2_SIM_TRAIN

- Isaac, MJX/mjlab, PPO, ACT/VLA, synthetic data, model selection
- no real hardware command

### WS2_ROBOT_INTEGRATION

- all training and Isaac batch jobs stopped
- robot-specific wired NIC and runtime environment

### WS1_ROBOT_RUNTIME

- validated deployment bundle only
- target runtime rebuild, offline replay, shadow, read-only, gated motion
- no large-scale retraining or experimental Isaac upgrade

## Host selection rules

- `.local/HOST_PROFILE.md` is mandatory and machine-local.
- Never infer WS1 versus WS2 from similar GPU/CPU specs; use the explicit logical host ID.
- `T35A` must create `WS2_DEPLOYMENT_BUNDLE_READY` before hardware phases.
- `T35B` must create `RUNTIME_OFFLINE_VALIDATED` before read-only hardware access.
- Never run real-time hardware control from an ML/Isaac environment.
- Do not use Ubuntu 26.04 for vendor robot runtimes unless each relevant vendor explicitly supports it.

## Version snapshot policy

Exact versions in documents are starting hypotheses, not floating dependencies. Each machine audit records:

- OS and kernel
- NVIDIA driver/CUDA
- Python and package lock
- ROS distro/RMW
- Isaac Sim/Lab pair
- vendor SDK/driver commit
- source asset commit
- container digest where used

Shared pins are stored in committed state/configs; local paths and caches stay under `.local/`.
