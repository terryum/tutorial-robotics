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

A tutorial completion is shared; environment readiness is local. Never copy a virtual environment between hosts.
