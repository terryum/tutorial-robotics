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

Keep the existing `flexiv-description` and `flexiv-ros2` pins. The reviewed RDK is the existing `ff92fe421e19daee6cdf27794a332c8fef7cf831`; use the archived RDK **Robot Software Compatibility** and **Environment Compatibility** sections to select a controller-compatible installation. A reviewed commit is not a statement that it matches the physical controller.

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
