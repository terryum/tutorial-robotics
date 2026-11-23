<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/hw-enlight-06.md" lang="ko">한국어</a> | <a href="hw-enlight-06.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# hw-enlight-06 — Enlight gripper pick-transfer-place preparation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `None` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-04` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

This stage remains blocked without device evidence. The ordinary lesson command does not send hardware commands.

Read the prerequisite [concept chapter](../concepts/deployment-hardware.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which tool and payload checks block a real pick-transfer-place action?

## Learning goals

Pick-transfer-place needs a width-based gripper contract, verified mount/tool/payload and task-specific stop/recovery behavior.

Which tool and payload checks block a real pick-transfer-place action?

## Preflight

Prerequisites: hw-enlight-04. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

Read [hardware safety](../../07_SAFETY.md). This chapter prepares evidence; it does not request or authorize a device action.

## Action

The canonical command `pal lesson run hw-enlight-06` is intentionally unavailable: the runner refuses this scaffold before readiness checks or output creation. Do not execute it.

This is preparation-only. Inspect the catalog and the readiness report; the current runner raises `NotImplementedError` for this scaffold and creates no successful device run. A readiness/contract check does not execute hardware or complete the lesson.

```bash
pal lesson check hw-enlight-06 --json
```

## Expected

Execution remains blocked. Do not expect a successful run directory or numeric device evidence from this scaffold.

### Reading the artifacts

No successful run artifacts are promised by this scaffold. Prepare an ignored local evidence checklist: exact model/side and firmware/SDK, `positions_rad`, `position_limits_rad`, `joint_group`, `timestamp`, `previous_timestamp`, `stale_after_s`, `enabled=False`, `error=False`, `estop_ready=True`, `command_authority_count=0`, networking and independently tested stop/watchdog/timeout. Read `ready`, `errors` and `valid_until_s` as data-check results, never execution permission. Do not publish private device identity/calibration.

## How it works

### Intuition

Pick-transfer-place needs a width-based gripper contract, verified mount/tool/payload and task-specific stop/recovery behavior. `Gripper` defines state, width/speed/force-limit/timeout command and stop interfaces without a vendor implementation. Robotiq 2F-85 is a simulation baseline, not proven Enlight electrical or mechanical compatibility. Probe approval or an arm-only joint card does not authorize closing a gripper on an object.

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

[`src/pai_lab/hardware/gripper.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/gripper.py)

`gripper.py` defines a width/speed/force-limit/timeout protocol; it does not implement a vendor controller or stale-state preflight. The paper freshness calculation refers to [`hardware/preflight.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/preflight.py). The thin entry point delegates to `runner.py`, which refuses this scaffold before readiness checks or measurement output.

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

[sim-teleop-01](./sim-teleop-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
