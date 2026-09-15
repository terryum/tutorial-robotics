<p align="right"><a href="../../ko/setup/fr3.md">한국어</a> | <a href="../../en/setup/fr3.md">ENGLISH</a></p>

# Franka Research 3 — Setup review

**Verification: `reader_test_required` for every physical step.** This guide prepares a model-specific installation review. A simulated robot does not identify your equipment. Record model, side, revision, firmware, controller and SDK locally; keep serials, addresses and calibration out of Git.

Before physical work, read [hardware safety](../../07_SAFETY.md). Prepare the matching manuals, manufacturer-specified fixture and power supply, protective-earth provisions, stop device, isolated network and an operator. Installation, calibration, enabling control and motion require the appropriate device procedure and per-run approval. The commands below only inspect synthetic data.

## Preparation and installation review

The downloaded file's URL says 1.5, but its revision page identifies **R02210, 1.5.1 (June 2025), system 5.8.0**. Match your actual system version before applying it.

| Review action | Expected evidence | Product manual reference |
|---|---|---|
| Prepare a stable foundation and bounded workspace | Mounting surface, clearances and controller ventilation meet the manual | §10.2–10.5 pp.60–68 |
| Review arm/control wiring, stop peripherals and earth connection | Correct connectors and functional earth, checked before power | §10.6 pp.69–77; §4.7 p.23 |
| Identify and mount the end effector | Tool mass, center of mass and mounting are documented locally | §10.7 pp.78–79 |
| Review start-up and stop-function tests | Qualified operator records actual results | §11.1–11.3 pp.93–103 |

## Choose the software combination

1. Read the robot system/image version in the controller interface and verify FCI availability.
2. Consult the archived **Compatibility: libfranka** matrix for that robot/server version. For example, the snapshot associates system ≥5.7.2 with libfranka ≥0.15.0 and server 9/3; system ≥5.9.0 uses server 10/3 with libfranka ≥0.18.0. Read all applicable version bounds rather than selecting the newest library automatically.
3. Intersect that choice with the **Compatibility: franka_ros2** matrix, including `franka_description`. The Jazzy guide recommends Ubuntu 24.04. Keep Humble and Jazzy workspaces separate.
4. Review FCI network setup (§11.4 pp.104–112) and the matching upstream installation page. Kernel installation, enabling FCI and control tests are physical commissioning work, not part of this offline example.

## Offline status check and recovery

`q`, `dq`, `tau_J` contain seven values in rad, rad/s, N·m. `O_T_EE` in libfranka is a column-major homogeneous transform; our synthetic pose is a separately declared meter/`wxyz` representation in O, not a direct copy of that array. Reception freshness is checked in an explicitly synthetic clock domain; robot-relative time must not be compared directly with host UTC.

Expect seven positions after ID reordering. Wrong SDK/model revision, frame, units, quaternion norm, stale timestamp or inconsistent SDK arrays must fail. An incompatible-library error on hardware calls for checking the compatibility matrices and reported server version. A timeout calls for cable, interface, routing and FCI status inspection. Do not clear faults or alter Watchman rules to make a test pass.

## Sources

- Local `fr3-product`, R02210 1.5.1: physical installation and FCI sections above.
- [libfranka compatibility](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html), [Jazzy compatibility](https://frankarobotics.github.io/docs/doc/franka_ros2_jazzy/franka_ros2/doc/compatibility_matrix.html).
- [FCI robot/network setup](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html).

## Run the synthetic check

```bash
python -m pai_lab.manual_examples fr3
```

[Manual library and verification workflow](index.md). These checks never update hardware readiness or learner progress.
