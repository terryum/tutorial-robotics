# core-fr3-07 — FR3 reach environment without ROS

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / fr3` |
| Legacy alias | `T22` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-fr3-04` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Use reset, observation, action, reward and episode boundaries for FR3 reach.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-fr3-07 --json
```

## Action

```bash
pal lesson run core-fr3-07 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-07/baseline-01 --json
```

## Expected

Inspect every transition in transitions.json. The baseline Jacobian controller should reduce distance; count steps and distinguish success from timeout.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --json
```

## How it works

The observation concatenates seven position offsets, seven scaled velocities and three world-target errors. Seven bounded actions adjust joint position targets. A successful reach terminates; the 64-step time limit truncates. These meanings matter to later PPO bootstrapping.

```text
observation ∈ R¹⁷; action ∈ R⁷; reward = −distance − effort penalty
```

## Code connection

`examples/core-fr3-07/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/learning.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Scripted action scale: 1 → 1.5 before bounded latent-action conversion. Check the 17-observation/7-action contract and termination.

```bash
pal lesson run core-fr3-07 --headless --seed 7 --samples 64 --output-dir .local/runs/core-fr3-07/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --comparison-run-dir .local/runs/core-fr3-07/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-fr3-07 --run-dir .local/runs/core-fr3-07/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-fr3-08](./core-fr3-08.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
