<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/hw-enlight-04.md" lang="ko">한국어</a> | <a href="hw-enlight-04.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-04 — Enlight free-space joint and TCP execution cards

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-02, sim-enlight-05` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

This stage remains blocked without device evidence. The ordinary lesson command does not send hardware commands.

Read the prerequisite [concept chapter](../concepts/deployment-hardware.md) and [equipment progression](../equipment-stages.md). This lesson addresses: What must an exact free-space action card specify before approval?

## Learning goals

An exact-action card binds one reviewed device and one action to fresh state, limits and a single-use approval.

What must an exact free-space action card specify before approval?

## Preflight

Prerequisites: hw-enlight-02, sim-enlight-05. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Read [hardware safety](../../07_SAFETY.md). This chapter prepares evidence; it does not request or authorize a device action.

## Action

The canonical command `pal lesson run hw-enlight-04` is intentionally unavailable: the runner refuses this scaffold before readiness checks or output creation. Do not execute it.

This is preparation-only. Inspect the catalog and the readiness report; the current runner raises `NotImplementedError` for this scaffold and creates no successful device run. A readiness/contract check does not execute hardware or complete the lesson.

```bash
pal lesson check hw-enlight-04 --json
```

## Expected

Execution remains blocked. Do not expect a successful run directory or numeric device evidence from this scaffold.

### Reading the artifacts

No successful run artifacts are promised by this scaffold. Prepare an ignored local evidence checklist: exact model/side and firmware/SDK, `positions_rad`, `position_limits_rad`, `joint_group`, `timestamp`, `previous_timestamp`, `stale_after_s`, `enabled=False`, `error=False`, `estop_ready=True`, `command_authority_count=0`, networking and independently tested stop/watchdog/timeout. Read `ready`, `errors` and `valid_until_s` as data-check results, never execution permission. Do not publish private device identity/calibration. The card gate also requires seven finite rad targets, max change ≤0.02 rad, timeout ≤1 s, expiry ≤60 s, exact device/action and single-use consumption before transport. Those are gate bounds, not universal safe limits.

## How it works

### Intuition

An exact-action card binds one reviewed device and one action to fresh state, limits and a single-use approval. The implemented software gate supports only one Enlight small joint move through an independently validated injected transport. It supplies no vendor connection or torque-enable API. A Cartesian/TCP path needs a different reviewed controller and exact-action contract; a joint card is not TCP approval.

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

[`src/pai_lab/hardware/run_card.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/run_card.py)

`examples/hw-enlight-04/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

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

[hw-enlight-05](./hw-enlight-05.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
