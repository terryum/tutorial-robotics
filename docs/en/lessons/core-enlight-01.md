# core-enlight-01 — Enlight description, frames, and kinematics

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / enlight` |
| Legacy alias | `T08A` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `core-02` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Build Enlight-L frames from the public vendor parameters.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Prepare the required public models once:

```bash
pal assets fetch flexiv-description
```

```bash
pal host detect --json
pal lesson check core-enlight-01 --json
```

## Action

```bash
pal lesson run core-enlight-01 --headless --seed 7 --samples 64 --output-dir .local/runs/core-enlight-01/baseline-01 --json
```

## Expected

Read eight body frames including world, seven joints, the flange site and total mass. This is a public simulation draft, not calibrated hardware.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --json
```

## How it works

Seven revolute joints are connected by fixed origin transforms. The vendor supplies joint limits, link masses, full inertia tensors and collision meshes. Conversion writes enlight-draft.xml into this run and leaves vendor sources untouched.

```text
T_world_flange = Π T_origin,i Rz(q_i)
```

## Code connection

Visual OBJ files contain multiple objects. The local adapter retains every vertex/face in one derived object for MuJoCo and preserves the vendor files; collision geometry and full inertia remain separate.

`examples/core-enlight-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Seed: 7 → 8. Structural audits, fixed model views and deterministic inference can remain identical. A remote service may vary independently of this local seed; record that limitation.

```bash
pal lesson run core-enlight-01 --headless --samples 64 --output-dir .local/runs/core-enlight-01/comparison-01 --seed 8 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --comparison-run-dir .local/runs/core-enlight-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-02](./core-enlight-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
