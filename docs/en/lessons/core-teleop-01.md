<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-teleop-01.md" lang="ko">한국어</a> | <a href="core-teleop-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-teleop-01 — Bimanual input, clutch and replay

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

This optional route preserves the existing VR-free lessons. Synthetic replay is labelled synthetic and does not verify physical input. The entry point writes into a fresh run directory. Inspect raw device clocks, xyz+xyzw in meters/radians, explicit left/right identity, calibration ID, clutch and deadman. At 100 ms without valid input the sink latches hold; release both switches, rearm locally, then press again. A reconnect or tracking loss requires the same procedure.

Three saved synthetic episodes are reloaded; discarded and aborted episodes remain distinct. Split entire episodes into train/validation/test. Try --variant 0.8 to change only left wrist translation.

## Learning goals

Understand source selection, calibrated coordinates, local hold and episode integrity.

## Preflight

Use `pal setup verify --profile core --json`. See [Ubuntu VR setup](../setup/vr-teleop.md). Mac supports contracts, transforms, replay and small MuJoCo examples; WS2 Ubuntu owns input/simulation/learning. WS1 Ubuntu applies verified collection to hardware in a separate approved run. Windows is an optional vendor recovery path. Preserve calibration and data under ignored `.local/`.

## Action

```bash
pal lesson run core-teleop-01 --samples 16 --json
```

## Expected

Inspect `teleop-contract.json`, `experiment.json`, `trace.csv` and episode manifests when available. Device input requires actual 60-second rate, maximum gap, tracking validity, occlusion, release, reconnect and 100 ms timeout evidence.

## Observe

Inspect recorded input and applied targets separately; synthetic timestamps are generated test clocks.

## How it works

The common contract uses receiver monotonic freshness and explicit source identities. Device clocks are preserved without cross-host subtraction.

## Code connection

`pai_lab.teleop`, `teleop_sources`, `teleop_recording` and `lessons.teleop`.

## Try it

```bash
pal lesson run core-teleop-01 --samples 16 --variant 0.8 --json
pal lesson check core-teleop-01 --run-dir BASE --json
```

## Recovery

Keep interrupted episodes; saved, discarded and aborted states are distinct. Never overwrite an existing episode or resume control after reconnect without local rearm.

## Checkpoint

Compare numeric artifacts and replay before review. Development tests never create learner completion. Hardware teleoperation requires simulation completion and separate safety review and per-run approval.

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-01](./core-fr3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
