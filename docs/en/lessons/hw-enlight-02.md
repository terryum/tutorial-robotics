# hw-enlight-02 — Enlight system identification and MuJoCo calibration

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `hardware / enlight` |
| Legacy alias | `T37A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `robot-runtime, isolated-network, enlight-hardware, read-only-preflight-enlight` |
| Prerequisites | `hw-enlight-01, core-enlight-02` |
| Safety | `motion-approval` |
| Verification | `reader_test_required` |
| Implementation | `scaffolded` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

## Learning goals

Review the observations, prerequisites and per-run safety boundary for enlight system identification and mujoco calibration.

## Preflight

This lesson remains scaffolded / reader_test_required until device evidence exists. Verify the offline candidate, common read-only gate and this robot's simulation prerequisites. A robot name or network connection does not authorize execution.

Read [hardware safety](../../07_SAFETY.md). A local snapshot must establish model/firmware identity, torque-disabled state, faults/E-stop, joint/force limits, communication timeout, fresh timestamps and isolated networking. Keep serials, private IPs and calibration only under .local/.

## Action

```bash
pal lesson check hw-enlight-02 --json
pal lesson run hw-enlight-02 --headless --json
```

The current entrypoint must return exit code 2 because an executable device adapter has not been verified. This is not completion. Do not manufacture a mock success receipt.

## Expected

Read the explicit reason that real-device verification evidence is absent. When equipment is ready, first measure identity, state rate, units/axes/joint order, freshness and stop paths read-only.

## How it works

```text
offline replay → command sink → read-only → live shadow
→ torque-disabled replay → fresh run card → one explicitly approved action
```

Each stage consumes the previous evidence without automatically granting authority for the next action. Contact, real evaluation, system identification and integrated-device work need fresh approval for the exact robot and action. An integrated task requires both devices' individual read-only gates.

Reader question: does receiving state authorize motion? No. Check timestamp age, model identity, fault/disabled state and the individual run card. For example, age 0.3 s exceeds a declared 0.1 s maximum and is stale. These illustrative numbers do not set device limits.

## Code connection

`examples/hw-enlight-02/run.py` → `src/pai_lab/lessons/runner.py`;
`src/pai_lab/hardware/preflight.py` checks supplied read-only snapshots.

## Try it

In a local copy of a snapshot, change only its timestamp to an old value and confirm stale-state rejection. Do not alter a real controller's clock, limits or watchdog. Preserve read-only check failures.

## Recovery

Stop without sending device commands if identity, disabled state, fault state, freshness or network isolation fails. Follow the vendor's E-stop and recovery procedure. Never automatically update firmware, enable torque, raise limits or bypass collision checks.

## Checkpoint

Completion criteria are currently unmet. Keep the lesson incomplete until an actual adapter, fresh evidence and applicable per-run approval exist. Personal state belongs under .local/; only publication evidence belongs in state/PUBLISHING.md.

<!-- pal:navigation:start -->
## Next lesson

[hw-enlight-03](./hw-enlight-03.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
