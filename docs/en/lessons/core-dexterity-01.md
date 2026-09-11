# core-dexterity-01 — Wuji and Sharpa model comparison

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / dexterity` |
| Legacy alias | `T16` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-wuji-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Compare Wuji and Sharpa using measured model properties.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch wuji-description-beta2
pal assets fetch mujoco-menagerie
```

```bash
pal host detect --json
pal lesson check core-dexterity-01 --json
```

## Action

```bash
pal lesson run core-dexterity-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-dexterity-01/baseline-01 --json
```

## Expected

Read the dimension labels before comparing values; mass is kg and counts are dimensionless. Both models must provide five fingertips.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --json
```

## How it works

Joint counts, actuator counts, fingertip counts and total masses are distinct comparison dimensions. Different joint names cannot be equated by index. A count ratio is a structural summary, not dexterity or grasp performance.

```text
count ratio = min(n_Wuji,n_Sharpa) / max(n_Wuji,n_Sharpa)
```

## Code connection

`examples/core-dexterity-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/hands.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

```bash
pal lesson run core-dexterity-01 --headless --samples 64 --output-dir .local/runs/core-dexterity-01/comparison-01 --seed 8 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --comparison-run-dir .local/runs/core-dexterity-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-dexterity-01 --run-dir .local/runs/core-dexterity-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-data-01](./core-data-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
