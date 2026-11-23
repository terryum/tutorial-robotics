<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-teleop-01.md" lang="ko">한국어</a> | <a href="sim-teleop-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-teleop-01 — Ubuntu VR installation and read-only input

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / common` |
| Legacy alias | `None` |
| Platforms | `linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-teleop-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

Read-only input acceptance needs actual Quest, MANUS and VIVE identities, firmware/SDK compatibility, calibration and simultaneous stream measurements. A downloaded Linux Hub archive or parsed synthetic packet does not prove USB devices work. This lesson remains scaffolded; ordinary runner dispatch rejects execution before manufacturing device-input evidence. Preserve existing VR-free routes and vendor environments.

Read the prerequisite [concept chapter](../concepts/data-imitation.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which live-input evidence is still missing after a software protocol check?

## Learning goals

Read-only input acceptance needs actual Quest, MANUS and VIVE identities, firmware/SDK compatibility, calibration and simultaneous stream measurements.

Which live-input evidence is still missing after a software protocol check?

## Preflight

Use a host matching the catalog platforms and capabilities; computer names do not grant readiness. `core-teleop-01` supports macOS arm64 and Linux x86_64; the later optional input/collection lessons are cataloged for Linux x86_64. Read [VR setup](../setup/vr-teleop.md), [equipment stages](../equipment-stages.md) and the synthetic/live distinction in [verification](../../verification/vr-teleop-2026-11-13.md). Preserve devices, calibration and raw episodes under ignored `.local/`; no automatic vendor installation or device consent is implied.

## Action

The canonical command `pal lesson run sim-teleop-01` is intentionally unavailable: the runner refuses this scaffold before readiness checks or output creation. Do not execute it.

This is preparation-only. Inspect the catalog and the readiness report; the current runner raises `NotImplementedError` for this scaffold and creates no successful device run. A readiness/contract check does not execute hardware or complete the lesson.

```bash
pal lesson check sim-teleop-01 --json
```

## Expected

Execution remains blocked. Do not expect a successful run directory or numeric device evidence from this scaffold.

### Reading the artifacts

Prepare rate, maximum gap, tracking-valid ratio, occlusion, side identity, release/reconnect and independent 100 ms hold evidence for each stream and simultaneous operation. `rate_report` computes `full_60s`, `rate_hz`, `maximum_gap_ns`, `tracking_valid_ratio`; these fields must come from real ordered receive records before claiming live acceptance. The public VR report states actual devices were absent.

## How it works

### Intuition

Read-only input acceptance needs actual Quest, MANUS and VIVE identities, firmware/SDK compatibility, calibration and simultaneous stream measurements. A downloaded Linux Hub archive or parsed synthetic packet does not prove USB devices work. This lesson remains scaffolded; ordinary runner dispatch rejects execution before manufacturing device-input evidence. Preserve existing VR-free routes and vendor environments.

### Calculation and units

$$
f=\frac{N-1}{t_{last}-t_{first}},\qquad g_{max}=\max_i(t_{i+1}-t_i)
$$

Use one ordered source/side stream and local receive times converted from ns to s. Rate f is Hz and maximum gap g is s; elapsed duration must cover at least 60 s for the full acceptance record. Worked calculation, not device data: 6001 samples over 60 s give 100 Hz. Average rate alone can conceal a long dropout.

```python
samples, duration_s = 6001, 60.0
assert (samples - 1) / duration_s == 100.0
```

## Code connection

### Source trace

[`src/pai_lab/teleop_sources.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_sources.py)

`examples/sim-teleop-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

See also [`teleop.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop.py), [`teleop_recording.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/teleop_recording.py) and the [VR verification record](../../verification/vr-teleop-2026-11-13.md).

## Try it

### Controlled comparison

Paper-only comparison: keep hypothetical sample times fixed and change one tracking-valid flag; predict a changed validity ratio while average rate stays unchanged. No vendor installation, EULA consent, haptics or live device operation is implied. Do not save a synthetic rate report as device acceptance.

## Recovery

Preserve failed readiness records and interrupted episode evidence. If identity, freshness, tracking, disabled/error/E-stop state or network isolation fails, remain blocked. Reconnection requires new read-only checks and any applicable local rearm; it never resumes physical motion. Follow the documented vendor recovery procedure without automatic firmware, torque, limit or watchdog changes. `pal course resume --json` inspects saved teaching state only.

## Checkpoint

### Check understanding

Why measure maximum gap in addition to mean rate? A burst can mask a stale interval. Do software tests complete this live-input lesson? No; actual device evidence remains required.

Record preparation and unresolved gates locally. Keep the lesson incomplete until actual device/input evidence and applicable per-run approval exist. Stop here without physical commands.

<!-- pal:navigation:start -->
## Next lesson

[sim-teleop-02](./sim-teleop-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
