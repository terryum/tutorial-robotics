# core-00 — Repository bootstrap and host audit

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `core / common` |
| Legacy alias | `T00` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12` |
| Prerequisites | `None` |
| Safety | `simulation` |
| Verification | `maintainer-checked` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Learning goals

Separate host readiness, local runs, and course completion.

## Preflight

On a fresh checkout, run `sh bootstrap.sh --plan`, read the plan, then use `--apply`. Activate `source .venv/bin/activate` before these commands. If the run directory already exists, use a new suffix such as 02.

```bash
pal host detect --json
pal lesson check core-00 --json
```

## Action

```bash
pal lesson run core-00 --headless --seed 7 --samples 64 --output-dir .local/runs/core-00/baseline-01 --json
```

## Expected

Inspect platform_id, python and capability_status in host-audit.json. Repeating with seed 8 should not change OS or installed packages.

Common artifacts are summary.json, trace.csv, experiment.json, plot.png, run.json and lesson-report.md. Model lessons also produce frame.png or the external stack's evaluation/Isaac image. Inspect axes, units and camera framing, not only file size.

```bash
pal lesson check core-00 --run-dir .local/runs/core-00/baseline-01 --json
```

## How it works

A capability is available only when its probe succeeds. Python version is a major/minor constraint; a package import is weaker evidence than rendering or device computation.

```text
available / checked
```

## Code connection

`examples/core-00/run.py` → `src/pai_lab/lessons/runner.py` → `src/pai_lab/lessons/physics.py`. The runner records the execution; the experiment module computes measurements from actual state. Match `experiment.json` payload fields to the corresponding calculations.

## Try it

Seed: 7 → 8. Structural audits, fixed model views and deterministic inference can remain identical. A remote service may vary independently of this local seed; record that limitation.

```bash
pal lesson run core-00 --headless --samples 64 --output-dir .local/runs/core-00/comparison-01 --seed 8 --json
```

Change only the indicated seed, sample count or variant. Explain differences in measurements, shape and limits. If results are invariant, explain why; do not invent a performance improvement.

The host-audit digest and available_capability_count should stay unchanged when only the seed changes. This is an installed-capability measurement, not a random simulation. Sourcing ROS can change the detected capabilities; inspect each capability’s evidence.

## Recovery

For capability-unavailable, prepare exactly the reported Python, model, platform or external stack, then rerun this lesson in a new directory. Preserve the failed run.json and numerical evidence. Do not automatically install system packages, drivers, CUDA, ROS, Isaac or large models. Resolve checksum errors by restoring a pinned cache, never by editing vendor sources.

## Checkpoint

Replace `--notes` with the concrete measurements and interpretation you observed before running this command. Save, fix and reverify received feedback first. Unresolved feedback, changed execution code or corrupt artifacts block completion. Execution alone does not complete the lesson. Stop after finishing this lesson.

```bash
pal lesson review core-00 --run-dir .local/runs/core-00/baseline-01 --comparison-run-dir .local/runs/core-00/comparison-01 --notes "Explained measured results and one-variable comparison; inspected plots and renderings." --json
pal lesson finish core-00 --run-dir .local/runs/core-00/baseline-01 --json
```

<!-- pal:navigation:start -->
## Next lesson

[core-01](./core-01.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
