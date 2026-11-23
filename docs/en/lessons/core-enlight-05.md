<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-enlight-05.md" lang="ko">한국어</a> | <a href="core-enlight-05.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-enlight-05 — Enlight PPO candidate and independent evaluation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / enlight` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-04, core-rl-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Measure joint/TCP error from the actual MuJoCo arm state. Learning uses arm demonstrations or rollouts and evaluates twenty independent targets.

Read the prerequisite [concept chapter](../concepts/reinforcement-learning.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which independent criterion can an Enlight PPO candidate fail?

## Learning goals

PPO adjusts a Enlight policy using actual MuJoCo rollouts, not prerecorded reward numbers.

Which independent criterion can an Enlight PPO candidate fail?

## Preflight

Prerequisites: core-enlight-04, core-rl-01. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-enlight-05 --headless --seed 7 --samples 64 --output-dir .local/runs/core-enlight-05/baseline-01 --json
```

## Expected

Inspect `enlight-ppo.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `policy.npz`, `training-contract.json`, `evaluation.json` and epoch checkpoints. Training identity binds model, source, engine, normalization, RNG, optimizer and data. `evaluation.json` records twenty independent target episodes (seed 10007), individual `errors_m` and successes. Success requires ten consecutive steps within 0.01 m; at least 16/20 is `performance_verified`. This is not hardware tolerance. Finite changed weights and exact reload may coexist with 0/20. The update plot is mean rollout reward; neither one favorable point nor falling optimizer loss certifies task performance. `candidate.json` keeps hardware compatibility false and forbids cross-model transfer.

## How it works

### Intuition

PPO adjusts a Enlight policy using actual MuJoCo rollouts, not prerecorded reward numbers. Policy updates and an independent performance pass are separate claims. The task rewards small world-frame TCP distance while penalizing large pre-transform action. Model-specific dynamics and actuator semantics remain part of the environment.

### Calculation and units

$$
L=\mathbb E[\min(\rho A,\operatorname{clip}(\rho,0.8,1.2)A)],\qquad r=-\|x^*-x\|_2-0.001\sum_j a_j^2
$$

The likelihood ratio ρ and clip interval are dimensionless; advantage A has reward-score scale. Observation has 17 values and seven actions map through 0.03 tanh(a) to rad. Reward is a designed score, not joules. Worked calculation, not rollout data: distance 0.02 m and action-squared sum 2 give reward −0.022.

```python
import numpy as np
reward = -0.02 - 0.001 * 2
assert np.isclose(reward, -0.022)
```

## Code connection

### Source trace

[`src/pai_lab/training.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py)

`examples/core-enlight-05/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Keep model, seed, samples and independent target set fixed; change only `variant` 1→0.8, which sets learning rate 0.01→0.008. Compare training diagnostics and held-out rollout success separately. Keep old checkpoints immutable. Resume requires the same engine/data/source/configuration; increasing the total epoch target is a different explicit operation.

```bash
pal lesson run core-enlight-05 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-enlight-05/comparison-01 --json
pal lesson check core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --json
pal lesson check core-enlight-05 --run-dir .local/runs/core-enlight-05/comparison-01 --json
pal lesson compare core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --comparison-run-dir .local/runs/core-enlight-05/comparison-01 --output-dir .local/comparisons/core-enlight-05/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-enlight-05 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why evaluate unseen targets after optimizer checks? Weight updates prove execution, while task success must be measured independently. Is 16/20 a physical robot acceptance criterion? No, it is this simulated reach task's gate.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --comparison-run-dir .local/runs/core-enlight-05/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-enlight-05 --run-dir .local/runs/core-enlight-05/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-enlight-03](./sim-enlight-03.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
