<p align="right"><a href="../../ko/setup/sharpa.md">한국어</a> | <a href="../../en/setup/sharpa.md">ENGLISH</a></p>

# Sharpa Wave — Setup review

**Verification: `reader_test_required` for every physical step.** This guide prepares a model-specific installation review. A simulated robot does not identify your equipment. Record model, side, revision, firmware, controller and SDK locally; keep serials, addresses and calibration out of Git.

Before physical work, read [hardware safety](../../07_SAFETY.md). Prepare the matching manuals, manufacturer-specified fixture and power supply, protective-earth provisions, stop device, isolated network and an operator. Installation, calibration, enabling control and motion require the appropriate device procedure and per-run approval. The commands below only inspect synthetic data.

## Prepare the correct hand and software package

Identify Wave side and hardware revision before choosing a mounting drawing, supply or cable. Review the archived **Overview**, **Get Started**, **User Guide → Hardware Installation** and safety sections; check mount rigidity, cable clearance, supplied electrical interfaces and cooling space with power off. The manual describes 22 active DoF. A left model cannot stand in for the right hand merely by changing a label.

The public SDK repository currently supplies installation guidance; binaries and examples are delivered in release packages. Its reviewed README distinguishes amd64 `.deb` from aarch64 `.zip`, both with `/opt/sharpa-wave-sdk/` layout. Python must match an included 3.10/3.11/3.12 extension and CPU architecture. The captured web manual contains a Python 3.13 filename example, but the reviewed SDK README explicitly says 3.13 is unsupported. Treat the actual release contents and matching README as the compatibility check; do not install a package here.

## Frames, tactile data and the Wuji comparison

| Property | Sharpa Wave model | Wuji Hand 2 Beta 2 model |
|---|---|---|
| Actuated joints per hand | 22 | 20 |
| Root body | `left_hand_C_MC` / `right_hand_C_MC` | `l_wrist` / `r_wrist` |
| Naming | `left_` / `right_` joint prefixes | `l_` / `r_` joint prefixes |
| SDK relationship | Confirm against matching release's joint table | S1–S4/J0–J3 axis order unresolved |

The comparison command loads both pinned left/right models and checks joint counts, side prefixes and root frames. It does not mirror joint signs or establish hardware axes. Sharpa's **Development** section documents joint mapping, control and tactile APIs; preserve the actual sensor/frame/units/format metadata rather than adopting Wuji's current or tactile conventions. The general synthetic Sharpa envelope uses declared teaching units only; it is not a raw SDK ABI.

## Offline action and recovery

Run `python -m pai_lab.manual_examples sharpa`, then the hand comparison below. Expect 22 joints on each Sharpa side and 20 on each Wuji side. Missing model assets must report unavailable; a modified pinned file must fail its hash check. Restore the exact vendor cache with the asset workflow, never edit the cache to make a test pass. A Python import/loader problem on a future hardware host calls for checking CPU architecture, Python minor version and matching shared library. Changing control source or issuing gestures is not a read-only recovery.

## Sources

- [Sharpa Wave manual](https://sharpa-robotics.github.io/sharpa-docs/): all section bodies and images archived, including Development/SDK and Support.
- [Wave SDK](https://github.com/sharpa-robotics/sharpa-wave-sdk): exact README commit and hash in the code reference manifest; redistribution license for the binary package is not established.
- Existing Menagerie and Wuji model locks; existing Wuji MJLab reference remains unchanged. No new Sharpa RL package was installed.

## Run the synthetic check

```bash
python -m pai_lab.manual_examples sharpa
python -m pai_lab.manual_examples hands
```

[Manual library and verification workflow](index.md). These checks never update hardware readiness or learner progress.
