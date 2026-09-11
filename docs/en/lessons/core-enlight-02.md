# core-enlight-02 — Enlight MuJoCo draft and cross-format validation

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / enlight` |
| Legacy alias | `T10A` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-enlight-01` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Compare independent vendor forward kinematics against compiled MJCF.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch flexiv-description
```

```bash
pal host detect --json
pal lesson check core-enlight-02 --json
```

## Action

```bash
pal lesson run core-enlight-02 --headless --seed 7 --samples 64 --output-dir .local/runs/core-enlight-02/baseline-01 --json
```

## Expected

For sampled configurations, maximum tool-position disagreement must be below 1e-9 m. variant 1.5 expands only the sampled angle range.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-enlight-02 --run-dir .local/runs/core-enlight-02/baseline-01 --json
```

## How it works

The reference path multiplies homogeneous transforms using vendor xyz/rpy values. The other path asks MuJoCo for attachment_site. Agreement checks conversion of joint axes and frame order, while dynamics and contact still require separate calibration.

```text
e_FK = ‖p_vendor(q) − p_MJCF(q)‖₂
```

## Code connection

Visual OBJ files contain multiple objects. The local adapter retains every vertex/face in one derived object for MuJoCo and preserves the vendor files; collision geometry and full inertia remain separate.

`examples/core-enlight-02/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Random joint interval: ±0.4 → ±0.6 rad using the same seed. Compare two independent FK evaluations at every resulting configuration.

```bash
pal lesson run core-enlight-02 --headless --seed 7 --samples 64 --output-dir .local/runs/core-enlight-02/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-enlight-02 --run-dir .local/runs/core-enlight-02/baseline-01 --comparison-run-dir .local/runs/core-enlight-02/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-enlight-02 --run-dir .local/runs/core-enlight-02/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-wuji-01](./core-wuji-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
