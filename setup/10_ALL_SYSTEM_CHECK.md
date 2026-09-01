# Whole-System Check

Create one report per machine plus one shared phase-gate summary.

## MacBook

| Capability | Expected evidence | Status |
|---|---|---|
| model registry | 7 active entries + H2 watchlist | |
| control | PD/gravity/IK/OSC outputs | |
| ROS 2 | pub/sub/TF/rosbag and MuJoCo bridge | |
| RL/IL | small PPO, BC, ACT smoke | |
| VLA protocol | T32A mock/client validation | |
| remote cockpit | SSH aliases and remote artifact access | |

## WS2 SIM_TRAIN

| Capability | Expected evidence | Status |
|---|---|---|
| G1 PPO | official play + small train + metrics | |
| Wuji PPO | official play + small train + metrics | |
| ACT scale-up |  checkpoint/evaluation | |
| SmolVLA | T32C actual model/server | |
| synthetic data | calibrated metadata/labels | |
| sim-to-sim | MuJoCo–Isaac comparison | |
| promotion | T35A deployment bundle | |

## Runtime — WS1 or WS2 integration

| Capability | Expected evidence | Status |
|---|---|---|
| target rebuild | bundle manifest/hash and deterministic test | |
| offline replay | expected versus runtime output | |
| command sink shadow | no real command path | |
| read-only hardware | robot-specific T36 evidence | |
| low-risk motion | explicit approved run card | |
| rollback/stop | verified path | |

Do not mark an unavailable future host as failed. Mark it `not-present` or `pending-host` with the required next action.
