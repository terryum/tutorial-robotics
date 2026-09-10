# Model Status

| Model ID | Role | Source | Status | Commit/tag | Validated formats | Notes |
|---|---|---|---|---|---|---|
| wujihand2-beta2-left/right | target | `wuji-technology/wuji-description` | pinned, fetch-on-demand | `v2026.8.19` / `b13f7d52b23cb79e35357303c72b7f61f1d2fda2` | MJCF, URDF, USD contract | 20 joints, 5 fingertip sites and 5 tip sensor frames per side |
| flexiv_enlight_l/ll | reference and public hardware track | `flexivrobotics/flexiv_description` | pinned, fetch-on-demand | `jazzy-v3.1` | URDF/Xacro contract | RDK v2.2; ROS 2 jazzy-v2.1 |
| franka_fr3_v2 | reference | `google-deepmind/mujoco_menagerie` | pending | — | — | — |
| unitree_g1_29dof | reference | `unitreerobotics repositories` | pending | — | — | — |
| sharpa_wave_right | reference | `sharpa-robotics/sharpa-urdf-usd-xml` | pending | — | — | — |
| aloha_bimanual | reference | `huggingface/lerobot + gym-aloha` | pending | — | — | — |
| unitree_h2_plus | watchlist | `Unitree official sources` | watchlist | — | — | — |

A model becomes `validated` only after path, compile/load, inventory, and smoke simulation checks pass.
