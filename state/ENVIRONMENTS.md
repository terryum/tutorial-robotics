# Shared Environment Status

> Local paths, local caches and active profile belong in `.local/`. This committed file records desired/shared locks and non-secret validation summaries only.

| Environment | Logical host/profile | Status | Exact version/lock | Validation evidence | Notes |
|---|---|---|---|---|---|
| mac-core | MACBOOK / MACBOOK_FOUNDATION | not-created | — | — | MuJoCo/control/Gym |
| mac-ros2 | MACBOOK / MACBOOK_FOUNDATION | not-created | — | — | Pixi/RoboStack Jazzy |
| mac-lerobot | MACBOOK / MACBOOK_FOUNDATION | not-created | — | — | BC/ACT/VLA protocol |
| ws2-ros2-sim | WS2 / WS2_SIM_TRAIN | host-not-present | — | — | fake hardware/deployment parity |
| ws2-isaac-vendor | WS2 / WS2_SIM_TRAIN | host-not-present | — | — | vendor-compatible |
| ws2-isaac-modern | WS2 / WS2_SIM_TRAIN | host-not-present | — | — | modern research isolated |
| ws2-mjlab | WS2 / WS2_SIM_TRAIN | host-not-present | — | — | G1/Wuji PPO |
| ws2-lerobot | WS2 / WS2_SIM_TRAIN | host-not-present | — | — | ACT/VLA scale-up/server |
| ws2-robot-runtime | WS2 / WS2_ROBOT_INTEGRATION | inactive | — | — | no simultaneous training |
| ws1-robot-runtime | WS1 / WS1_ROBOT_RUNTIME | host-not-present | — | — | stable robot runtime |

Codex records actual resolved versions and commit/container digests. It must not treat a desired baseline as verified installation.
