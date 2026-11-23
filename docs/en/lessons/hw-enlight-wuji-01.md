<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/hw-enlight-wuji-01.md" lang="ko">한국어</a> | <a href="hw-enlight-wuji-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-wuji-01 — Enlight and Wuji integrated read-only validation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight-wuji` |
| Legacy alias | `T38A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight, wuji-hardware, read-only-preflight-wuji` |
| Prerequisites | `hw-enlight-01, hw-wuji-01` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the prerequisite [concept chapter](../concepts/deployment-hardware.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How are arm and hand identity, timing and stop boundaries checked together?

## Learning goals

Combining arm and hand adds synchronization and stop-boundary questions; two independent green badges do not establish an integrated system.

How are arm and hand identity, timing and stop boundaries checked together?

## Preflight

Device setup and manual references: [Enlight](../setup/enlight.md), [Wuji Hand 2 Beta 2](../setup/wuji.md).

This lesson remains scaffolded / reader_test_required until device evidence exists. Verify the offline candidate, common read-only gate and this robot's simulation prerequisites. A robot name or network connection does not authorize execution.

Read [hardware safety](../../07_SAFETY.md). A local snapshot must establish model/firmware identity, torque-disabled state, faults/E-stop, joint/force limits, communication timeout, fresh timestamps and isolated networking. Keep serials, private IPs and calibration only under .local/.

Read [hardware safety](../../07_SAFETY.md). This chapter prepares evidence; it does not request or authorize a device action.

## Action

The canonical command `pal lesson run hw-enlight-wuji-01` is intentionally unavailable: the runner refuses this scaffold before readiness checks or output creation. Do not execute it.

This is preparation-only. Inspect the catalog and the readiness report; the current runner raises `NotImplementedError` for this scaffold and creates no successful device run. A readiness/contract check does not execute hardware or complete the lesson.

```bash
pal lesson check hw-enlight-wuji-01 --json
```

## Expected

Read the explicit reason that real-device verification evidence is absent. When equipment is ready, first measure identity, state rate, units/axes/joint order, freshness and stop paths read-only.

### Reading the artifacts

No successful run artifacts are promised by this scaffold. Prepare an ignored local evidence checklist: exact model/side and firmware/SDK, `positions_rad`, `position_limits_rad`, `joint_group`, `timestamp`, `previous_timestamp`, `stale_after_s`, `enabled=False`, `error=False`, `estop_ready=True`, `command_authority_count=0`, networking and independently tested stop/watchdog/timeout. Read `ready`, `errors` and `valid_until_s` as data-check results, never execution permission. Do not publish private device identity/calibration.

## How it works

### Intuition

Combining arm and hand adds synchronization and stop-boundary questions; two independent green badges do not establish an integrated system. Both read-only gates must describe the same session, explicit joint groups, source clocks, transforms and fault/disabled states. A stale hand alongside a fresh arm remains an integrated failure. Keep independent rollback and a reviewed coordinated stop plan before proposing any combined action.

### Calculation and units

$$
t_{age}=t_{now}-t_{snapshot},\qquad 0\leq t_{age}\leq t_{stale}
$$

All times here use the same wall-clock domain in seconds. `preflight` additionally requires a finite declared stale window in (0,1] s and an advancing timestamp if `previous_timestamp` exists. This is distinct from teleop's monotonic 100 ms sink. Paper calculation, not live evidence: snapshot age 0.3 s exceeds a declared 0.1 s window and is rejected. These illustrative numbers set no device limits.

```python
snapshot_age_s, declared_window_s = 0.3, 0.1
assert not (0 <= snapshot_age_s <= declared_window_s)
```

## Code connection

### Source trace

[`src/pai_lab/hardware/preflight.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/preflight.py)

`examples/hw-enlight-wuji-01/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

## Try it

### Controlled comparison

Paper-only comparison: keep identity, joint values and all limits fixed; increase only the hypothetical snapshot age across its declared stale window. Predict rejection and list the missing device evidence. Do not run a physical trial, change clocks/watchdogs or create a completion receipt. The lesson runner refuses scaffolded execution before a device operation.

## Recovery

Preserve failed readiness records and interrupted episode evidence. If identity, freshness, tracking, disabled/error/E-stop state or network isolation fails, remain blocked. Reconnection requires new read-only checks and any applicable local rearm; it never resumes physical motion. Follow the documented vendor recovery procedure without automatic firmware, torque, limit or watchdog changes. `pal course resume --json` inspects saved teaching state only.

## Checkpoint

### Check understanding

Why is a fresh disabled snapshot insufficient for motion? It checks one observed state; command transport, action-specific controller, physical limits and fresh per-run approval remain separate. Is the lesson complete after this paper calculation? No.

Record preparation and unresolved gates locally. Keep the lesson incomplete until actual device/input evidence and applicable per-run approval exist. Stop here without physical commands.

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-09](./core-fr3-09.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
