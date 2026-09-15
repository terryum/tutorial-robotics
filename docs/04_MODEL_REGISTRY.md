# Model Registry and Upstream Sources

`assets/sources.json`, `assets/model-lock.json` and `src/pai_lab/lessons/models.py`
are the current authority. Paths below are relative to the named bundle under
`.cache/assets/`; vendor caches are pinned and read-only.

| Model | Pinned bundle | Current primary asset |
|---|---|---|
| Wuji Hand 2 Beta 2 | `wuji-description` | `hand2/hand2_beta2/body/mjcf/right.xml` and `left.xml`; matching `urdf/` and `usd/` directories |
| FR3 | `mujoco-menagerie` | `franka_fr3/scene.xml`, `franka_fr3/fr3.xml` |
| G1 | `mujoco-menagerie` | `unitree_g1/scene.xml`; 29 actuators and floating base |
| Sharpa Wave | `mujoco-menagerie` | `sharpa_wave/scene_right.xml`, `scene_left.xml` |
| ALOHA 2 simulation | `mujoco-menagerie` | `aloha/scene.xml`, `aloha/aloha.xml`; nq=16, nu=14 |
| Enlight | `flexiv-description` | `urdf/common/flexiv_arm.xacro`, `config/Enlight-L/`; lesson conversion writes only to its run directory |

Wuji description v2026.8.19 is pinned at
`c003186833616b23c06784ebefe442474cc5f4b5`. The previous acceptance document's
`b13f7d...` value was stale; both existing source/model locks and the inspected cache
agree on `c003186...`. No vendor pin was updated in this correction.

## Setup and manuals

- [한국어 자료실과 setup](ko/setup/index.md)
- [English manual library and setup](en/setup/index.md)

Hardware revision, firmware and installed SDK must be identified independently.
A model's actuator count or successful simulation does not establish device identity,
SDK axis correspondence, safe limits or readiness.

## Code references

Existing `unitree-mjlab`, `wuji-mjlab`, `lerobot`, `flexiv-description` and
`flexiv-ros2` references remain pinned in `assets/sources.json`.
New SDK reading references have exact commits, files, SHA-256 and license findings
in `assets/manual-code-refs.json`. They are source reviews, not installed runtime
dependencies. Sharpa's public SDK repository provides a README; its binary package
and implementation license must be obtained from the vendor before integration.

## Registry requirements

Record model ID/revision, source commit, per-model license, native paths, any derived
asset provenance, base/frame names, joint groups/counts, action and observation units,
missing sensor or axis mappings and the validation method. Keep device identifiers,
calibration and execution data only under ignored `.local/`.
