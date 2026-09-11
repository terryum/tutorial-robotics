# sim-isaac-01 — Import public robot assets into Isaac Sim

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / isaac` |
| Legacy alias | `T33` |
| Platforms | `ubuntu-24.04-x86_64` |
| Capabilities | `isaac-sim` |
| Prerequisites | `core-04` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Import the pinned public Wuji URDF into an actual Isaac articulation.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

Read the [WS1 environment/input handoff](../../verification/ws1-handoff.md). External-stack execution remains reader_test_required until measured on a suitable host.

```bash
pal host detect --json
pal lesson check sim-isaac-01 --json
```

## Action

```bash
pal lesson run sim-isaac-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-isaac-01/baseline-01 --json
```

## Expected

Require twenty matching joint names and inspect imported.usda and isaac-frame.png. Count agreement is only the first import check; inspect orientation and scale visually.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check sim-isaac-01 --run-dir .local/runs/sim-isaac-01/baseline-01 --json
```

## How it works

URDF import converts joints, inertia and geometry into USD/PhysX. The adapter uses the documented Isaac Sim 5.1 importer API. Mesh paths are resolved in a local derived URDF; the vendor files stay unchanged. Version compatibility still requires WS1 execution evidence.

```text
URDF joint names → USD articulation DOF map
```

## Code connection

`examples/sim-isaac-01/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/isaac.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Dome light intensity: 1000 → 1500 renderer units; imported asset and camera remain fixed.

```bash
pal lesson run sim-isaac-01 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-isaac-01/comparison-01 --variant 1.5 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review sim-isaac-01 --run-dir .local/runs/sim-isaac-01/baseline-01 --comparison-run-dir .local/runs/sim-isaac-01/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish sim-isaac-01 --run-dir .local/runs/sim-isaac-01/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[sim-isaac-02](./sim-isaac-02.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
