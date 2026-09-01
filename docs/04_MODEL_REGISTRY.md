# Model Registry and Upstream Sources

Codex creates a machine-readable registry during T02. This document defines the intended sources and discovery rules.

| Model ID | Official source | Expected primary asset |
|---|---|---|
| `wuji_hand2_beta2_right` | `wuji-technology/wuji-hand-description` | `mjcf/right.xml`; `usd/right/wujihand.usd`; matching URDF |
| `franka_fr3_v2` | `google-deepmind/mujoco_menagerie` | `franka_fr3_v2/scene.xml`; robot file `fr3v2.xml` |
| `unitree_g1_29dof` | `unitreerobotics/unitree_mujoco`, `unitreerobotics/unitree_rl_mjlab`, `unitreerobotics/unitree_rl_lab` | discover and pin exact G1 scene/model paths from selected stack |
| `sharpa_wave_right` | `sharpa-robotics/sharpa-urdf-usd-xml` | right-hand XML/URDF/USD, preferably flange variant for arm composition |
| `aloha_bimanual` | `huggingface/lerobot` + `gym-aloha` | installed simulation package and LeRobot environment adapter |

## Additional integration sources

- `wuji-technology/mujoco-sim` for minimal Mac-friendly Wuji playback
- `wuji-technology/isaaclab-sim` for Wuji USD/Isaac example
- `wuji-technology/wuji-mjlab` for in-hand PPO and sim-to-real
- `sharpa-robotics/sharpa-rl-lab` for Isaac Lab tactile/RL reference
- `frankarobotics/franka_ros2` for actual Franka ROS 2 concepts

## Registry requirements

Each model entry must include:

- stable ID, human name, hardware/model revision
- role: target/reference/watchlist
- source repository, branch/tag, commit SHA
- license path and redistribution note
- native asset paths by format and generated-asset provenance
- embodiment type and fixed/free/mobile base declaration
- root/base/end-effector/fingertip frames
- joint groups, expected counts, order, sign and units
- control/action modes and vendor command semantics
- observation/sensor capabilities and missing-feature declaration
- mass/inertia/contact/actuator caveats by backend
- firmware/SDK/driver compatibility where applicable
- initial/named poses and keyframes where applicable
- last validation date, asset-test result and cross-format tolerance

Do not hardcode a path from memory when upstream discovery can confirm it.
