<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/core-fr3-10.md" lang="ko">한국어</a> | <a href="core-fr3-10.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# core-fr3-10 — FR3 demonstrations, BC and independent reach evaluation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-09` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Measure joint/TCP error from the actual MuJoCo arm state. Learning uses arm demonstrations or rollouts and evaluates twenty independent targets.

Read the prerequisite [concept chapter](../concepts/data-imitation.md) and [equipment progression](../equipment-stages.md). This lesson addresses: How do held-out episodes and independent reach tests constrain BC claims?

## Learning goals

Behavioral cloning learns FR3's observation-to-action mapping from demonstrations generated on its own MuJoCo environment.

How do held-out episodes and independent reach tests constrain BC claims?

## Preflight

Prerequisites: core-fr3-09. Inspect `pal course next --json`. Evidence and progress stay in ignored `.local/`.

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run core-fr3-10 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-10/baseline-01 --json
```

## Expected

Inspect `arm-learning.json`, `trace.csv`, `plot.png` and `experiment.json`. The performance_verified field in `evaluation.json`, when present, describes policy performance only.

## Observe

Read axes, units, initial/final error and extrema. Inspect rendering and compare named joints, groups and contacts in the payload with the measurements.

### Reading the artifacts

Inspect `policy.npz`, `training-contract.json`, `evaluation.json` and epoch checkpoints. Training identity binds model, source, engine, normalization, RNG, optimizer and data. `evaluation.json` records twenty independent target episodes (seed 10007), individual `errors_m` and successes. Success requires ten consecutive steps within 0.01 m; at least 16/20 is `performance_verified`. This is not hardware tolerance. Finite changed weights and exact reload may coexist with 0/20. The epoch plot is training action MSE; it is not the independent reach-error plot. `candidate.json` keeps hardware compatibility false and forbids cross-model transfer.

## How it works

### Intuition

Behavioral cloning learns FR3's observation-to-action mapping from demonstrations generated on its own MuJoCo environment. Thirty full episodes are split 20/5/5 into train/validation/test, so neighboring transitions never leak across those boundaries. The robot-specific expert solves damped IK; it does not import another arm's weights.

### Calculation and units

$$
L=\frac{1}{Nd_a}\|XW-A\|_F^2,\qquad \Delta q=0.03\tanh(a)
$$

X has shape (N,18): 17 stored observation values plus bias. W is 18×7; A has N×7 expert pre-transform actions. Action MSE is in the chosen normalized-action scale squared. The simulator applies a bounded joint delta in rad. Worked calculation, not learned output: a=0.5 produces 0.03 tanh(0.5)≈0.0138635 rad.

```python
import numpy as np
assert np.isclose(0.03 * np.tanh(0.5), 0.013863514717800292)
```

## Code connection

### Source trace

[`src/pai_lab/training.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py)

`examples/core-fr3-10/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

The [public robot-path verification](../../verification/robot-paths-2026-11-08.md) separates historical simulation evidence from unverified external/device execution.

## Try it

### Controlled comparison

Keep model, seed, samples and independent target set fixed; change only `variant` 1→0.8, which sets learning rate 0.01→0.008. Compare training diagnostics and held-out rollout success separately. Keep old checkpoints immutable. Resume requires the same engine/data/source/configuration; increasing the total epoch target is a different explicit operation.

```bash
pal lesson run core-fr3-10 --headless --seed 7 --samples 64 --variant 0.8 --output-dir .local/runs/core-fr3-10/comparison-01 --json
pal lesson check core-fr3-10 --run-dir .local/runs/core-fr3-10/baseline-01 --json
pal lesson check core-fr3-10 --run-dir .local/runs/core-fr3-10/comparison-01 --json
pal lesson compare core-fr3-10 --run-dir .local/runs/core-fr3-10/baseline-01 --comparison-run-dir .local/runs/core-fr3-10/comparison-01 --output-dir .local/comparisons/core-fr3-10/comparison-01 --json
```

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run core-fr3-10 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check understanding

Why evaluate unseen targets after optimizer checks? Weight updates prove execution, while task success must be measured independently. Is 16/20 a physical robot acceptance criterion? No, it is this simulated reach task's gate.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review core-fr3-10 --run-dir .local/runs/core-fr3-10/baseline-01 --comparison-run-dir .local/runs/core-fr3-10/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish core-fr3-10 --run-dir .local/runs/core-fr3-10/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-fr3-01](./sim-fr3-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
