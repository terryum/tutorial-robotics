<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/setup/enlight.md" lang="ko">한국어</a> | <a href="enlight.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

<p align="right"><a href="../../ko/setup/enlight.md">한국어</a> | <a href="../../en/setup/enlight.md">ENGLISH</a></p>

# Enlight — Setup review

**Verification: `reader_test_required` for every physical step.** This guide prepares a model-specific installation review. A simulated robot does not identify your equipment. Record model, side, revision, firmware, controller and SDK locally; keep serials, addresses and calibration out of Git.

Before physical work, read [hardware safety](../../07_SAFETY.md). Prepare the matching manuals, manufacturer-specified fixture and power supply, protective-earth provisions, stop device, isolated network and an operator. Installation, calibration, enabling control and motion require the appropriate device procedure and per-run approval. The commands below only inspect synthetic data.

## Preparation and installation review

Use the supplied **Enlight Series User Manual V0.1** with the matching Orion controller and Aegis safety documents. The series guide is not a substitute for those controller manuals.

| Action to review | Expected evidence | Source |
|---|---|---|
| Check foundation, fasteners, lifting and base flatness | Stable supported arm; matching mounting drawing | V0.1 §4.3.2–4.3.3, printed pp.26–29 |
| Confirm grounding through the controller | Correct arm/controller connection and protective-earth method | §4.3.3.1.5 p.29; Orion required |
| Match installation orientation to gravity | Elements Robot Installation agrees with floor, inverted or tilted mounting | §4.3.4 pp.29–30 |
| Review tool mass, center of gravity and inertia | Payload definition includes the entire tool and workpiece | §4.3.5 pp.30–32 |
| Review cable routing and connectors before power | No strain, pinching or connector mismatch | §4.4 pp.33–36; Orion required |

**Unresolved base-fastener torque conflict:** V0.1 states 36 Nm on printed p.27, 22 Nm on p.29 and 32 Nm on p.41 (each ±10%). Ask Flexiv for the applicable fastener, mounting revision and corrected value. This guide deliberately specifies no executable base torque. PDF viewer indices differ from printed page labels.

## Software and status

The **Enlight-L / Software Package v3E.1 / RDK Professional** installation
profile uses [RDK v2.1](https://github.com/flexivrobotics/flexiv_rdk/releases/tag/v2.1)
(`bfab04f4e385ca335ee3025bfefe70249b015578`) and `flexivrdk==2.1.0` in an
isolated Python 3.12 environment. Official wheels cover macOS arm64 and Linux x86_64.
Lock full commits, package SHA256 and licenses; reproduce from the lock, not moving tags.

The [frozen ROS manifest](https://github.com/flexivrobotics/flexiv_ros2/blob/a165e88a2b41cb7e09b46aa1bfb842718ee783b1/flexiv.jazzy.repos)
pairs ROS `jazzy-v2.1` (`a165e88a2b41cb7e09b46aa1bfb842718ee783b1`) with
description `jazzy-v2.1` (`54593cda75bac0251567a13db3d6862da7fe7cfb`). That
description README declares software **v4**: confirm actual v3E.1 joint/frame/limit
compatibility with Flexiv before physical use.

Public teaching pins remain description `77dd8d8ec4c48a06778ac3886569c9d24e7a977a`
and source-review RDK `ff92fe421e19daee6cdf27794a332c8fef7cf831`. Distinguish
these educational revisions from the v3E.1 operational profile. Preserve lesson
IDs; replace a model only after checking seven-joint order/axes, limits, inertia,
frames, rendering and independent FK error below `1e-9 m`. Company installers,
site configuration and device-specific models stay private.

### Application, connection and recovery

1. Use Teach Pendant **Elements** first to review mounting/gravity, tool payload,
   stop devices, manual Jog procedure and Remote Mode. Physical changes/Jog need
   the applicable procedure and fresh approval.
2. Request the v3E.1-compatible Ubuntu **Elements Studio** package from Flexiv;
   record version/hash locally. See the [official installation guide](https://github.com/flexivrobotics/flexiv_sim_plugin/blob/v2.x/docs/elements_studio_setup.md).
3. Use Mac for isolated SDK import, offline models and remote development; use
   Ubuntu 24.04/Jazzy for the first wired robot connection, C++ and ROS. Separate
   robot LAN from remote access; use one initial command sender.
4. Progress through import → offline replay → command-free state capture → a
   separately approved non-real-time action → real-time work only as needed.
   Professional licensing alone does not require a real-time kernel.
5. Check the official ROS driver with `use_fake_hardware:=true` first. This is
   separate from `sim-enlight-01`'s teaching DDS/MuJoCo adapter. Neither proves
   physical readiness. Missing host/package access stays pending.

Read-only capture selects `ARM_1`, seven ordered joints and rad/rad/s/N·m, and
retains device time plus receipt time. Reject empty/NaN/out-of-range state,
disconnects and stale/future/frozen device time. Do not refresh old device time
with reception time. `operational=False` does not prove servo-off; require explicit
disabled-state evidence. Compare Elements before/after for unchanged servo/fault.
On failure stop and use vendor recovery; no ClearFault, ServoOn, mode change or
motion belongs in a state reader.

Store snapshots under ignored `.local/`. Immediately run
`pal hardware preflight enlight --snapshot <local-snapshot.json> --read-only --json`;
old snapshots must fail freshness. Each motion needs a fresh exact robot/action
card with limits, acknowledgement, timeout, stale-state watchdog and independent
stop path, followed by explicit approval.

An external SSD uses Ubuntu 24.04 **amd64 on an x86_64 PC**, its own EFI and Ubuntu
partitions, and the same dependency lock. Review disk identity and backup before
partitioning. Recheck wired NIC/driver, isolated routing and latency on each PC.
This is not an Apple Silicon boot image. Firmware, kernel and GPU changes are
outside this setup.

V0.1 §4.5.1 p.37 maps yellow to power on/servo off, white to servo on/stopped, green to project executing, blue to Freedrive, steady/blinking red to normal/fatal faults, and orange to recovery. Read controller state as well; a lamp alone does not establish readiness.

Calibration review: §6.2 p.51 covers joint torque sensors; §6.3 pp.52–53 covers kinematics validation with a locked TCP and floor-mounted robot; §6.4 pp.54–55 covers dynamics. These procedures can move the arm or change controller parameters. Obtain the matching Orion/Aegis procedures and an approved run before executing them. A calibration menu opening is not calibration evidence.

## Offline action and recovery

Run the command below. Expect seven ordered joint values with rad, rad/s, N·m, an explicit base/TCP pose convention and a fresh synthetic reception timestamp. The teaching envelope normalizes poses to meters and `wxyz`; it is not a raw RDK packet.

The pinned `example_py/basics1_display_robot_states.py` calls **`ClearFault()` and `ServoOn()`** before displaying state. Do not use its filename as evidence that it is read-only. This exercise never imports it. A frame, unit or timestamp error rejects the fixture; correct the fixture specification before proceeding. For physical faults, stop and use the vendor recovery procedure without automatic fault clearing.

## Sources

- Local `enlight-v01`; printed pages above were checked against the supplied original.
- [Flexiv RDK manual](https://www.flexiv.com/software/rdk/manual/v2.x/index.html): robot software compatibility, state fields, error handling.
- [Flexiv resources](https://www.flexiv.com/download?type=User+Manuals) and [Flexiv Hub](https://hub.flexiv.com/login): request Elements, Orion, Aegis and Enlight Quick Start revisions when unavailable.

## Run the synthetic check

```bash
python -m pai_lab.manual_examples enlight
```

[Manual library and verification workflow](index.md). These checks never update hardware readiness or learner progress.
