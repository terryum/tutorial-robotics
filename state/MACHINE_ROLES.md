# Machine Roles

| Logical host ID | Default mode | OS baseline | Primary responsibilities |
|---|---|---|---|
| `MACBOOK` | `DEVELOPMENT` | macOS arm64 | Portable MuJoCo/control/ROS concepts/small RL-IL and remote cockpit |
| `WS2_WINDOWS` | host-management layer | Windows 11 | WSL2/driver/display lifecycle; do not conflate with Ubuntu readiness |
| `WS2_UBUNTU` | `DEVELOPMENT` | Ubuntu 24.04.x/Jazzy | Portable curriculum plus Isaac, MJX/mjlab, PPO, ACT/VLA and synthetic data |
| `WS1_UBUNTU` | `ROBOT_RUNTIME` | Ubuntu/vendor-supported | Rebuilt candidate bundle, offline replay, read-only and explicitly gated hardware work |

Each OS layer creates ignored host-local capability/environment state through
`$bootstrap-host`. Current non-secret handoff status is recorded in
`state/HOST_STATUS.md`; the `.local/` directory remains machine-local and must
not be committed.
