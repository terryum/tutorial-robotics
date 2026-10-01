# Shared Environment Status

> Local paths, activation state and caches remain under `.local/`. This file records semantic environment roles, committed specs and non-secret validation evidence.

| Environment role | Supported host class | Status | Exact lock/digest | Validation evidence | Notes |
|---|---|---|---|---|---|
| `core-dev` | MacBook or Linux development host | not-created | — | — | MuJoCo/control/Gym; per-platform lock allowed |
| `ros2-dev` | MacBook RoboStack or Ubuntu Jazzy | not-created | — | — | core ROS concepts and bridge |
| `lerobot-dev` | MacBook or Linux development host | not-created | — | — | dataset/BC/ACT/small VLA |
| `gpu-mjlab` | Linux NVIDIA CUDA | not-created | — | — | G1/Wuji PPO |
| `gpu-isaac-vendor` | Linux NVIDIA CUDA | not-created | — | — | vendor-compatible pair |
| `gpu-isaac-modern` | Linux NVIDIA CUDA | not-created | — | — | custom USD/synthetic data |
| `gpu-lerobot` | Linux NVIDIA CUDA | not-created | — | — | ACT/VLA scale-up/server |
| `robot-runtime` | isolated WS1 or WS2 | not-created | — | — | no concurrent development batch |

These semantic roles and historical status placeholders do not inventory the
current machine. Audit actual environments before installation. Learner progress
follows the configured local/private progress workflow; readiness remains local.
Never copy a virtual environment between hosts. See the
[remote development guide](en/setup/remote-development/index.md).


## Capability mapping

| Host | Core | ROS 2 | Small ML/LeRobot | CUDA/mjlab | Isaac | Robot runtime |
|---|---|---|---|---|---|---|
| MacBook | yes | optional RoboStack | yes, CPU/MPS | no | remote client | no |
| WS2 development | yes | native Jazzy | yes | yes | yes | disabled in development mode |
| WS1 development | yes | native Jazzy | yes | if compatible GPU verified | optional, separately verified | disabled in development mode |
| WS2 runtime | limited runtime tools | native Jazzy | inference only | batch stopped | batch stopped | yes |
| WS1 runtime | limited runtime tools | native Jazzy | inference only | batch stopped | batch stopped | yes |

Either development workstation may cover portable and GPU content when its
actual capabilities are verified. Neither requires prior MacBook completion.
Mac-specific portability checks remain optional; training is not concurrent
with robot-runtime operation on either workstation.
