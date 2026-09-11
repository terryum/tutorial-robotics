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

## Reader route

Read the Expected result first. Your task is to connect the measured values to the learning goal, then explain the calculation and the code that produced them.

[Terminal setup, resuming, opening results and camera controls](../READER_GUIDE.md)

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

Measured development example. Read both axis units and the reference/measured difference first. Validate your own run separately.

![core-enlight-01 measured plot](../../assets/examples/core-enlight-01-plot.png)

Read eight body frames including world, seven joints, the flange site and total mass. This is a public simulation draft, not calibrated hardware.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --json
```

## Observe

Read the metric units, observed_first/observed_last and checks first. Inspection validates saved files, exits, and leaves completion unchanged.

```bash
pal lesson inspect core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --json
```

Open the plot on macOS (closing the image preserves the run):

```bash
open .local/runs/core-enlight-01/baseline-01/plot.png
```

On other systems, open the same PNG in your file manager. Read the raw values from this JSON:

```bash
python -m json.tool .local/runs/core-enlight-01/baseline-01/experiment.json
```

## How it works

Seven revolute joints are connected by fixed origin transforms. The vendor supplies joint limits, link masses, full inertia tensors and collision meshes. Conversion writes enlight-draft.xml into this run and leaves vendor sources untouched.

$$
{}^WT_F=\prod_{i=1}^{7}(T_{origin,i}R_z(q_i))\,T_{flange}
$$

Symbols, units and assumptions: T: 4×4 transform; translation m; rotation rad; multiply in chain order.

Worked calculation (not a measured run result): q=π/2 rad rotates local +x to local +y for Rz.

Practical connection: Fixed flange offsets matter when comparing vendor FK and tool sensors.

## Code connection

Visual OBJ files contain multiple objects. The local adapter retains every vertex/face in one derived object for MuJoCo and preserves the vendor files; collision geometry and full inertia remain separate.

`examples/core-enlight-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

This is an environment or structure audit. A seed change is not required. Compare names, units, prerequisites and the actual artifact; record specific findings in the review notes.

<details>
<summary>Optional: what changes when the assumptions fail?</summary>

Choose one input in the equation and write its units. Inspect whether doubling it doubles the output or whether clipping, normalization or coordinate transforms change that relationship. Changing another assumption or model at the same time needs a separate experiment.

</details>

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-enlight-01 --run-dir .local/runs/core-enlight-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-02](./core-enlight-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
