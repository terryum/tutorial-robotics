<p align="right"><a href="../../ko/setup/aloha.md">한국어</a> | <a href="../../en/setup/aloha.md">ENGLISH</a></p>

# ALOHA — Setup review

**Verification: `reader_test_required` for every physical step.** This guide prepares a model-specific installation review. A simulated robot does not identify your equipment. Record model, side, revision, firmware, controller and SDK locally; keep serials, addresses and calibration out of Git.

Before physical work, read [hardware safety](../../07_SAFETY.md). Prepare the matching manuals, manufacturer-specified fixture and power supply, protective-earth provisions, stop device, isolated network and an operator. Installation, calibration, enabling control and motion require the appropriate device procedure and per-run approval. The commands below only inspect synthetic data.

## Select the kit before assembling

The Trossen **2.0 documentation** covers Interbotix Stationary, Mobile and Solo kits. It explicitly redirects Trossen AI Arms users to separate documentation. This is also distinct from the course's Menagerie **ALOHA 2 simulation**; sharing an ALOHA name does not imply identical arms, cameras, wiring or software.

Review the matching **Getting Started → Hardware Setup** before assembly. Stationary preparation includes table/frame clamping, leader WidowX and follower ViperX placement, pulley/gravity compensation, camera mounts and cable routing. Mobile requires its own base/controller setup; Solo has one leader/follower arm pair. Prepare the kit's specified supplies and hubs; identify each arm and camera locally before wiring or applying power. Never copy another site's serial-based udev rules.

## Software and status inspection

The archived Stationary 2.0 software guide specifies native Ubuntu 22.04 / ROS 2 Humble. It warns that Interbotix 2.0 collection/teleoperation support does not imply ACT/ACT++ training compatibility; the document directs that workflow to 1.0. Keep the selected branch/commit, ROS distribution and training/data adapter contract explicit. The code manifest pins a reviewed repository commit, not a claim that every branch matches that installation guide.

Review **Post-Install Hardware Setup** for unique leader/follower device names and camera identities, then **Bringup & Shutdown** for the physical procedure. Launching bringup, teleoperation, recording or replay can enable torque and move arms. The offline command does none of those operations.

## Episodes and camera alignment

The official **Data Collection → Dataset Format** describes HDF5 episodes:

| Configuration | qpos / qvel / action | Cameras | Additional action |
|---|---|---|---|
| Stationary | 14 each | high, low, left wrist, right wrist | none |
| Mobile | 14 each | high, left wrist, right wrist | base_action: 2 |
| Solo | 7 each | high and selected wrist | none |

The synthetic exercise explicitly selects Stationary: two arms × (6 joints + 1 normalized gripper) = 14. The current simulation has `nq=16`, `nu=14` because each gripper has two finger coordinates; do not equate model qpos length with dataset action length. The fixture's rad/normalized units and per-camera timestamps are declared teaching metadata, not a promise that every HDF5 file contains them. Before converting HDF5 or LeRobot data, inspect actual gripper normalization, frame rate, camera names and timestamp source; a row index does not prove synchronization.

## Offline action and recovery

Expect two synthetic rows, 14-value qpos/action and four aligned camera streams. The example's 10 ms alignment budget is illustrative. Wrong dimensions, missing cameras, nonmonotonic or misaligned timestamps and format changes must fail. Fix the dataset contract or inspect acquisition timing; do not replay the data on a robot to diagnose its shape.

## Sources

- [Interbotix ALOHA 2.0](https://docs.trossenrobotics.com/aloha_docs/2.0/index.html): configuration-specific hardware/software setup.
- [Data collection and dataset format](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/data_collection.html).
- [Interbotix ALOHA](https://github.com/Interbotix/aloha): pinned `scripts/record_episodes.py`, `aloha/real_env.py`, `aloha/constants.py`; existing LeRobot/Menagerie pins remain unchanged.

## Run the synthetic check

```bash
python -m pai_lab.manual_examples aloha
```

[Manual library and verification workflow](index.md). These checks never update hardware readiness or learner progress.
