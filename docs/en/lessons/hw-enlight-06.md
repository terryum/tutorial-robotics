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

## Learning goals

Review gripper width, speed, force, status and stop interfaces. Robotiq 2F-85 is the simulation baseline. Mount, power, communications and payload compatibility are required before unlocking.

## Preflight

Prerequisites: hw-enlight-04. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Review readiness records and unresolved gates. A run card binds exact device, action, joint group, limits, expiry within sixty seconds and single-use approval.

```bash
pal lesson run hw-enlight-06 --samples 64 --json
```

Save the returned run_dir as BASE. Execution alone does not mark completion.

## Expected

Blocked as reader_test_required. Do not finish without device evidence.

## How it works

Review gripper width, speed, force, status and stop interfaces. Robotiq 2F-85 is the simulation baseline. Mount, power, communications and payload compatibility are required before unlocking.

## Code connection

[`hardware.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/run_card.py)

`pai_lab.training` records checkpoints and independent evaluation.

## Try it

Change only variant; keep the other conditions fixed.

```bash
pal lesson run hw-enlight-06 --samples 64 --variant 0.8 --json
pal lesson check hw-enlight-06 --run-dir BASE --json
pal lesson review hw-enlight-06 --run-dir BASE --comparison-run-dir COMPARISON --notes "measured comparison and interpretation"
pal lesson finish hw-enlight-06 --run-dir BASE --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run hw-enlight-06 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

Save explanation, baseline, comparison and next action, then stop after one lesson. Unverified tools or model compatibility keep the stage blocked.

<!-- pal:navigation:start -->
## Next lesson

[sim-teleop-01](./sim-teleop-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
