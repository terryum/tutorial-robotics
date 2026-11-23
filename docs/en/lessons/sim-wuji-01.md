<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-wuji-01.md" lang="ko">한국어</a> | <a href="sim-wuji-01.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-wuji-01 — Wuji in-hand PPO on GPU

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / wuji` |
| Legacy alias | `T27` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `nvidia-cuda` |
| Prerequisites | `core-wuji-02, core-rl-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

Read the [robot-hands concept chapter](../concepts/robot-hands.md), then locate this lesson in the [equipment progression](../equipment-stages.md).

See the [NVIDIA ecosystem workbook](../nvidia-ecosystem.md) for connections to ROS, GPU, Isaac and VLA. Distinguish its extension activities from this lesson's implemented and verified scope.

## Learning goals

Train and evaluate the pinned Wuji MJLab reorientation task.

## Preflight

Device setup and manual references: [Wuji Hand 2 Beta 2](../setup/wuji.md).

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-wuji-01 --json
```

## Action

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## Expected

Require changed policy tensors, finite evaluation rewards and a nonblank image. Short-run success remains distinct from successful in-hand manipulation.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/sim-wuji-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/sim-wuji-01/baseline-01/experiment.json
```

## How it works

The vendor task registers its own hand, object, reward and PPO runner. Use its supported Pixi environment, prepared assets and a separate local output directory. The vendor training embodiment is not automatically a calibrated Beta 2 hardware model.

$$
\theta_{k+1}=\theta_k-\eta\nabla_\theta L_k
$$

Symbols, units and assumptions: θ: learned parameters; η: learning rate; L: algorithm-specific loss; example is scalar SGD.

Worked calculation (not a measured run result): θ=1, η=0.01, gradient=2 → new θ=0.98.

Practical connection: Real training must change weights and reload them; short smoke does not establish success rate.

### From input to observation

In-hand reorientation learns with object state and contact, unlike constructing synergy poses. The vendor task defines hand, object and reward. It is not automatically equivalent to calibrated Beta2 hardware or tactile sensing.

## Code connection

`examples/sim-wuji-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/gpu.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

### Read the actual producer and artifacts

Compare [`gpu.py`](../../../src/pai_lab/lessons/gpu.py) with dispatch in [`runner.py`](../../../src/pai_lab/lessons/runner.py).

`gpu.environment` registers `WujiHand_Reorient` from pinned wuji-mjlab and constructs 32 CUDA0 environments. `gpu.run` performs short optimization, save/reload and inference with that environment setup. Match task, parameter_delta, policy_sha256 and evaluation_frame_std in `experiment.json` with `evaluation-actions.npz`. Read reward interpretation and action dimensions from task definitions. Checkpoint files alone do not establish grasp success rate; payload performance remains false.

## Try it

Sample budget: 64 → 96. Training lessons derive optimizer iterations from this budget and evaluate for this many steps; candidate-only lessons change evaluation length.

```bash
pal lesson run sim-wuji-01 --headless --seed 7 --output-dir .local/runs/sim-wuji-01/comparison-01 --samples 96 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

```bash
pal lesson compare sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --comparison-run-dir .local/runs/sim-wuji-01/comparison-01 --output-dir .local/comparisons/sim-wuji-01/comparison-01 --json
```

<details>
<summary>Optional: what changes when the assumptions fail?</summary>

Choose one input in the equation and write its units. Inspect whether doubling it doubles the output or whether clipping, normalization or coordinate transforms change that relationship. Changing another assumption or model at the same time needs a separate experiment.

</details>

### Predict before changing a value

Budget64→96 changes training8→12 iterations and evaluation to96 steps together. Changed reward mixes training amount with evaluation-window changes. Do not claim general improvement without separately fixed evaluation seeds and conditions.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --comparison-run-dir .local/runs/sim-wuji-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-wuji-01 --run-dir .local/runs/sim-wuji-01/baseline-01 --json
```

### Check understanding and answer guide

Question: Is a vendor checkpoint a Beta2 hardware candidate? Answer: Embodiment, safety and sensor compatibility need additional checks. Question: Does nonblank evaluation.png prove task performance? Answer: It proves rendering. Separate learning mechanics from object-task performance.

<!-- pal:navigation:start -->
## Next lesson

[sim-vla-01](./sim-vla-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
