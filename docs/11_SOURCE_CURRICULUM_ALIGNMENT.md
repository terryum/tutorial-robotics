# Source and curriculum alignment

| Public source family | Role | Catalog tracks | Boundary |
|---|---|---|---|
| MuJoCo / Menagerie FR3 | control and portable simulation | `core-fr3-*`, `sim-cross-01`, `hw-fr3-01` | model/source pin only; no assumed real dynamics |
| Unitree G1 | humanoid playback and imitation | `core-g1-01`, `sim-g1-01` | public vendor source, GPU evidence separate |
| Wuji Hand 2 Beta 2 | dexterity, tactile contract, hardware | `core-wuji-*`, `sim-wuji-*`, `hw-wuji-*` | Beta 2 pins only; simulation tactile is not sensor force |
| Sharpa Wave | dexterity comparison | `core-dexterity-*` | public models; no cross-robot gain reuse |
| ALOHA / LeRobot | episode data, BC, ACT, VLA | `core-data-*`, `core-il-*`, `core-aloha-*`, VLA tracks | large artifacts belong on HF with cards and checksums |
| Flexiv Enlight | second manipulator, ROS fake hardware, read-only-first runtime | `core-enlight-*`, `sim-enlight-*`, `hw-enlight-*` | public Git sources; Hub downloads never redistributed without permission |
| Isaac Sim workspace | USD import and sim-to-sim | `sim-isaac-*`, `sim-cross-01` | pinned source; installation/EULA remain manual |

`assets/sources.json` is the revision authority. `pal sources check` detects missing/mutable fields but never changes pins. Private-robot implementation and organization data are excluded by the public boundary validator.
