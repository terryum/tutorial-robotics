<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-wuji-02.md" lang="ko">한국어</a> | <a href="sim-wuji-02.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-wuji-02 — Wuji dexterity candidate bundle

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / wuji` |
| Legacy alias | `T42A` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `sim-wuji-01, sim-deploy-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the prerequisite [concept chapter](../concepts/deployment-hardware.md) and [equipment progression](../equipment-stages.md). This lesson addresses: Which model and policy identities belong in a dexterity candidate? Follow the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) where relevant; the actual producer below identifies which engine/framework this lesson uses.

## Learning goals

The dexterity candidate consumes an actual completed `sim-wuji-01` checkpoint, loads it into the same pinned registered vendor task in play mode, evaluates it, then copies exact policy bytes.

Which model and policy identities belong in a dexterity candidate?

## Preflight

Device setup and manual references: [Wuji Hand 2 Beta 2](../setup/wuji.md).

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-wuji-02 --json
```

## Action

Activate the prepared environment and use a fresh output directory. Preserve the returned run path; execution does not mark completion.

```bash
pal lesson run sim-wuji-02 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-wuji-02/baseline-01 --json
```

## Expected

Read mean reward, evaluation-actions.npz, evaluation.png and candidate/manifest.json. Require actual checkpoint reload and finite evaluation; leave performance_verified false.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-wuji-02/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-wuji-02/baseline-01/experiment.json
```

### Reading the artifacts

Read `candidate/manifest.json`: `task`, `policy_sha256`, `mean_reward`, `candidate_only=True`, `hardware_compatible=False`, `performance_verified=False`, `rollback=command-sink`. `evaluation-actions.npz` holds sampled actions and `evaluation.png` actual rendering. The finite/reload checks establish execution, not a solved in-hand task.

## How it works

### Intuition

The dexterity candidate consumes an actual completed `sim-wuji-01` checkpoint, loads it into the same pinned registered vendor task in play mode, evaluates it, then copies exact policy bytes. This is checkpoint reload and task rollout, not a new training run. A vendor task model is not automatically Beta 2 physical-hand equivalence.

### Calculation and units

$$
\bar r=\frac1N\sum_{i=1}^N r_i
$$

N is evaluation steps, r is vendor-task reward and the mean has task-defined score units. Action shape follows that vendor task, not a universal 20-joint array. Worked calculation, not policy evaluation: rewards [1,2,3] give mean 2.

```python
import numpy as np
assert np.mean([1.0, 2.0, 3.0]) == 2.0
```

## Code connection

### Source trace

[`src/pai_lab/lessons/gpu.py`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/gpu.py)

`examples/sim-wuji-02/run.py` delegates to the common runner, which checks catalog implementation and capabilities before dispatch. The source above computes the quantities described here; metadata filenames do not establish the calculation by themselves.

## Try it

### Controlled comparison

Change `samples` 64→96 with fixed checkpoint/seed/task. Only evaluation horizon changes here; no optimizer is called. Compare reward distributions over the declared horizon and keep model provenance visible. `variant` is unused for this candidate.

```bash
pal lesson run sim-wuji-02 --headless --seed 7 --samples 96 --output-dir .local/runs/sim-wuji-02/comparison-01 --json
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
pal lesson check sim-wuji-02 --run-dir .local/runs/sim-wuji-02/comparison-01 --json
pal lesson compare sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --comparison-run-dir .local/runs/sim-wuji-02/comparison-01 --output-dir .local/comparisons/sim-wuji-02/comparison-01 --json
```

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

### Check understanding

Does a matching policy hash prove a better grasp? No; it identifies bytes. Why is `performance_verified` false? This short task rollout does not implement a task-solving performance gate.

Inspect actual values, axes and images from both runs. Replace the notes below with measured values and your interpretation, resolve feedback, then review/finish one lesson. Missing capability remains unavailable; a publication badge is not your local completion.

```bash
pal lesson review sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --comparison-run-dir .local/runs/sim-wuji-02/comparison-01 --notes "REPLACE with actual measured values and interpretation" --json
pal lesson finish sim-wuji-02 --run-dir .local/runs/sim-wuji-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[hw-common-01](./hw-common-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
