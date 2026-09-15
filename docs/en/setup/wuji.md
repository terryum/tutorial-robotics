<p align="right"><a href="../../ko/setup/wuji.md">한국어</a> | <a href="../../en/setup/wuji.md">ENGLISH</a></p>

# Wuji Hand 2 Beta 2 — Setup review

**Verification: `reader_test_required` for every physical step.** This guide prepares a model-specific installation review. A simulated robot does not identify your equipment. Record model, side, revision, firmware, controller and SDK locally; keep serials, addresses and calibration out of Git.

Before physical work, read [hardware safety](../../07_SAFETY.md). Prepare the matching manuals, manufacturer-specified fixture and power supply, protective-earth provisions, stop device, isolated network and an operator. Installation, calibration, enabling control and motion require the appropriate device procedure and per-run approval. The commands below only inspect synthetic data.

## Identify Beta 2 and prepare the installation

Use **Version Identification and Compatibility** to identify Beta 2 locally (the vendor uses hardware revision markers; never publish the serial). Prepare a matching left/right mounting interface, strain relief, a **11–13 V DC** supply, and separate XT30 power/RJ45 communication cables. **Hardware Integration → Power Supply** specifies at least 200 W, with a supplied 12 V 20 A adapter. Check polarity and wiring with power off; never hot-plug during operation. **Palm Mounting Interface** and **Coordinate Frames and Models** define the mechanical review.

The repository profile records firmware v2.6.0 and SDK v2026.8.31. The captured compatibility page still labels v2.5.1 current and requires firmware/SDK release-note matching. This discrepancy is unresolved device compatibility, not authority to upgrade. Verify the actual installed versions and matching release notes before connecting. The description commit is `c003186833616b23c06784ebefe442474cc5f4b5` (v2026.8.19), matching both existing locks; it is independent of firmware identity.

## State, units and tactile metadata

`joint_states` is the joint-angle stream; diagnostics do not contain joint angles. Incoming frames can contain only online joints in any order. Index by **`nid`**, with thumb 0–3, index 4–7, middle 8–11, ring 12–15, pinky 16–19. A missing joint stays explicitly missing. Position is rad, velocity rad/s, and **`effort` is current in A, not N·m**.

The control guide explicitly leaves SDK `S1..S4` to model actuator `J0..J3` axis order unavailable. Matching joint counts and names does not verify that mapping. Keep it unresolved until vendor evidence and a separately approved physical check exist.

The reviewed fingertip example obtains each sensor's format/digest before decoding. Preserve point count, field units, geometry and sensor frame. That source distinguishes normalized point force in newer firmware from N in older firmware; aggregate force remains N and temperature C. Do not treat normalized taxels as Newtons or hard-code their dimensions. The exercise uses one synthetic point, not a physical sensor layout. `timestamp_us` requires the SDK's clock/synchronization interpretation; the exercise uses a documented synthetic clock, not a real UTC claim.

## Offline action, expected result and recovery

Expect 20 ordered positions. Removing ID 0 with `allow_partial=True` returns `complete=false`, `missing_ids=[0]` and `None` at position 0; it does not shift the other fingers or invent a zero reading. Unknown IDs, duplicates, stale data, firmware/SDK mismatch or changed tactile metadata fail. Restore a consistent fixture or reacquire the exact format metadata. Do not use `clear_fault`, origin setting, torque enable or firmware update as an automatic recovery.

## Sources

- [Beta 2 compatibility](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility/), [hardware integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration/).
- [Control guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide/), [SDK reference](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/): units, joint numbering, variable-length frames, timestamps.
- Pinned `wuji-sdk/examples/python/wuji_hand_2/3.fingertip_typed.py` and `0.subscribe_callback.py` in the code reference manifest.

## Run the synthetic check

```bash
python -m pai_lab.manual_examples wuji
python -m pai_lab.manual_examples hands
```

[Manual library and verification workflow](index.md). These checks never update hardware readiness or learner progress.
