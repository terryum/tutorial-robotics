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

Learn a bimanual data contract without buying a headset. The lesson generates synthetic left/right poses and switch events, routes them through `CommandSink`, saves three episodes, then reloads them and separates saved, discarded and aborted outcomes. `provenance=synthetic` is part of the result, not an incidental label. The local receiver clock, not an unsynchronized device clock, decides freshness.

Read the prerequisite [concept chapter](../concepts/data-imitation.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do clutch, timestamps and replay keep bimanual input interpretable?

## Learning goals

Learn a bimanual data contract without buying a headset.

How do clutch, timestamps and replay keep bimanual input interpretable?

## Preflight

Use a host matching the catalog platforms and capabilities; computer names do not grant readiness. `core-teleop-01` supports macOS arm64 and Linux x86_64; the later optional input/collection lessons are cataloged for Linux x86_64. Read [VR setup](../setup/vr-teleop.md), [equipment stages](../equipment-stages.md) and the synthetic/live distinction in [verification](../../verification/vr-teleop-2026-11-13.md). Preserve devices, calibration and raw episodes under ignored `.local/`; no automatic vendor installation or device consent is implied.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-teleop-01 --headless --seed 7 --samples 16 --output-dir .local/runs/core-teleop-01/baseline-01 --json
```

## Expected

Expect synthetic replay/collection evidence, not a live-device acceptance report. Inspect the catalog artifact, `experiment.json`, `trace.csv`, `plot.png` and episode manifests. Three saved episodes plus discarded/aborted records preserve lifecycle and provenance. Actual 60-second device-rate/tracking/occlusion/reconnect acceptance belongs to the separate live-input gate.

## Observe

Inspect recorded input and applied targets separately; synthetic timestamps are generated test clocks.

### Reading the artifacts

Read `experiment.json` → `payload`: `schema_version=2`, `provenance`, three saved episodes, one discarded and one aborted, episode-level `splits`, `command_publishers=0`, `live_input_verified=False`, `watchdog_ns`. Each episode manifest hashes `frames.jsonl`; replay rejects unsaved/corrupted content. Trace values are acceptance booleans against synthetic time, not measured physical tracking quality. The source generates 10 ms frame intervals.

## How it works

### Intuition

Learn a bimanual data contract without buying a headset. The lesson generates synthetic left/right poses and switch events, routes them through `CommandSink`, saves three episodes, then reloads them and separates saved, discarded and aborted outcomes. `provenance=synthetic` is part of the result, not an incidental label. The local receiver clock, not an unsynchronized device clock, decides freshness.

### Calculation and units

$$
t_{age}=t_{poll}-t_{receive},\qquad 0\leq t_{age}<100000000\ \mathrm{ns}
$$

Poses have seven entries: xyz in m and unit quaternion xyzw, which is dimensionless; named finger angles use rad. Sequence and receive time are increasing integers. At exactly 100 ms the gate latches hold. Worked calculation, not device evidence: 100,000,000 ns is 0.1 s; an age of 99,999,999 ns is below the boundary.

```python
age_ns = 100_000_000
assert age_ns / 1e9 == 0.1
assert not (0 <= age_ns < 100_000_000)
```

## Code connection

### Source trace

[`src/pai_lab/lessons/teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/teleop.py)

`examples/core-teleop-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

See also [`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py) and the [VR verification record](../../verification/vr-teleop-2026-11-13.md).

## Try it

### Controlled comparison

Keep sample count fixed and change only `variant` 1→0.8. It scales synthetic left-wrist x displacement, not the 100 ms watchdog. Acceptance traces may remain identical while recorded poses change. After timeout/reconnect/tracking loss, require fresh release of both switches, local rearm and fresh press; an arriving pose alone cannot resume control.

```bash
pal lesson run core-teleop-01 --headless --seed 7 --samples 16 --variant 0.8 --output-dir .local/runs/core-teleop-01/comparison-01 --json
pal lesson check core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --json
pal lesson check core-teleop-01 --run-dir .local/runs/core-teleop-01/comparison-01 --json
pal lesson compare core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --comparison-run-dir .local/runs/core-teleop-01/comparison-01 --output-dir .local/comparisons/core-teleop-01/comparison-01 --json
```

## Recovery

Keep interrupted episodes; saved, discarded and aborted states are distinct. Never overwrite an existing episode or resume control after reconnect without local rearm.

## Checkpoint

### Check understanding

Can identical acceptance traces hide different poses? Yes; acceptance checks validity/freshness, not pose equality. Are these human demonstrations? No; provenance and live_input_verified explicitly say otherwise.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --comparison-run-dir .local/runs/core-teleop-01/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-teleop-01 --run-dir .local/runs/core-teleop-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-01](./core-fr3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
