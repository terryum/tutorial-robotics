# Machine Roles

| Logical host ID | Default profile | OS baseline | Primary responsibilities | Status |
|---|---|---|---|---|
| `MACBOOK` | `MACBOOK_FOUNDATION` | macOS arm64 | MuJoCo/control/ROS concepts/small RL-IL/cockpit | unregistered |
| `WS2` | `WS2_SIM_TRAIN` | Windows 11 + Ubuntu 24.04.x/Jazzy | Isaac, MJX/mjlab, PPO, ACT/VLA, synthetic data | unregistered |

Each machine creates `.local/HOST_PROFILE.md` through `$bootstrap-machine`. The `.local/` directory is machine-local and must be ignored by Git.
