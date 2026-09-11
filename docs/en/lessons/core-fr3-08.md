# core-fr3-08 — PPO on FR3 reach

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T24` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-07, core-rl-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Train, save and reload PPO on the actual FR3 reach environment.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-08 --json
```

## Action

```bash
pal lesson run core-fr3-08 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-08/baseline-01 --json
```

## Expected

Inspect policy-contract.json, parameter change and rollout rewards. Compare learning rate only. Rewards may fluctuate; keep performance_verified false until a separate evaluation establishes a threshold.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-fr3-08 --run-dir .local/runs/core-fr3-08/baseline-01 --json
```

## How it works

The same PPO implementation now sees the 17-value reach observation and emits seven Gaussian latent actions. tanh bounds the simulator command. The saved contract includes observation scaling and action semantics so deployment cannot silently reinterpret weights.

```text
a = tanh(Wᵀ[obs,1]); q* = q + 0.03 a rad
```

## Code connection

`examples/core-fr3-08/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

```bash
pal lesson run core-fr3-08 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-08/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-fr3-08 --run-dir .local/runs/core-fr3-08/baseline-01 --comparison-run-dir .local/runs/core-fr3-08/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-fr3-08 --run-dir .local/runs/core-fr3-08/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-01](./core-enlight-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
