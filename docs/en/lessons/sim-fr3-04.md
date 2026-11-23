<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/lessons/sim-fr3-04.md" lang="ko">한국어</a> | <a href="sim-fr3-04.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# sim-fr3-04 — FR3 matched-engine evidence comparison

<!-- pal:metadata:start -->
| Field | Value |
|---|---|
| Stage / track | `sim / fr3` |
| Legacy alias | `None` |
| Platforms | `macos-arm64, linux-x86_64` |
| Capabilities | `python-3.12, numpy, mujoco` |
| Prerequisites | `sim-fr3-01` |
| Safety | `simulation` |
| Verification | `reader_test_required` |
| Implementation | `implemented` |
<!-- pal:metadata:end -->

## Reader route

Read the [PhysX chapter](../concepts/physx.md) for the boundary between importing a model and comparing engines. This lesson analyzes completed MuJoCo and PhysX records; it does not run PhysX here. First check whether “the same targets” actually describes the inputs.

## Learning goals

Match target arrays, initial pose, world frame and control period in two completed runs. Compare TCP error RMS difference, joint errors and measured contact forces. Investigate import, drive and engine differences without inferring hardware safety.

## Preflight

The catalog prerequisite is `sim-fr3-01`; the actual consumer also requires verified completed runs of both `core-fr3-09` and `sim-fr3-01`. Read the remaining Isaac/PhysX scope in the public [environment verification](../../verification/robot-paths-2026-11-08.md). Running analysis on a Mac does not establish PhysX verification on that Mac.

Read `pal course next --json` and both original `experiment.json` files. `frame`, `initial_q_rad`, `tcp_targets_m` and `control_dt_s` must match exactly, with equal sample counts. Missing or damaged PhysX evidence cannot be filled with invented numbers or another MuJoCo execution. Wait for the external capability and evidence.

## Action

Run the analysis only after both originals are completed, hash-verified and matched. This does not execute hardware or GPU training.

```bash
pal lesson run sim-fr3-04 --headless --seed 7 --samples 64 --output-dir .local/runs/sim-fr3-04/baseline-01 --json
```

Record this directory as BASE. `previous_run` selects each lesson's current completion record; inspect `run.json`'s `inputs` and original records to identify the selected runs. Do not mark personal progress complete merely to provide analysis inputs.

## Expected

Inspect `engine-comparison.json`, `trace.csv`, `plot.png`, `experiment.json` and `run.json`. This analysis does not train a policy or create `evaluation.json`. Any policy performance result from a producer is separate from engine agreement and hardware safety.

Current checks validate matching fields and finite numbers; there is no numerical pass threshold for the engine difference. A small difference does not establish a physical-device tolerance. Editing this document does not change the catalog's `reader_test_required` badge.

## Observe

### Two curves and their RMS difference

The second `trace.csv` column is measured MuJoCo TCP error(m); the third is PhysX TCP error(m). Although named `reference`, the second column is the first engine's measured error, not a zero target line. Distinguish the curves in `plot.png`.

`tcp_error_difference_rmse_m` in `engine-comparison.json` summarizes differences between error magnitudes. Compare `joint_errors_a_rad`/`joint_errors_b_rad` in rad and `contacts_a_N`/`contacts_b_N` in N as well. The metric does not directly compare TCP position vectors or prove identical contact models.

Current output time is reconstructed as `i * 0.02`. Check it against original `control_dt_s` and time arrays. If the original period differs from 0.02 s, do not treat this axis as evidence of physical time alignment or use it to claim a latency analysis.

## How it works

### Fix the comparison conditions first

Match initial joint pose(rad), target position arrays(m), world frame and control period(s). Let $e_i^M,e_i^P$ be the TCP error magnitudes at the same sample index. The code computes:

$$
D=\sqrt{\frac{1}{N}\sum_{i=0}^{N-1}(e_i^M-e_i^P)^2}.
$$

$N$ is the shared sample count; each $e$ and $D$ has units m. Worked calculation, not measurements: error differences [0.003, 0.004] m give $D\approx0.0035355$ m. If both engines miss by 20 mm in the same direction, D can be zero. D=0 therefore does not establish target success.

### Do not assign a cause too early

Different curves can arise from integration/contact as well as model conversion, inertia, actuator/drive or coordinate handling. Current matching checks do not cover every joint name, drive setting or tool calibration. Review those separately. Claiming “only the engine changed” requires more evidence than equality of four target-contract fields.

## Code connection

[`runner.py`](../../../src/pai_lab/lessons/runner.py) dispatches this ID to [`comparison.run`](../../../src/pai_lab/lessons/comparison.py). [`learning.previous_run`](../../../src/pai_lab/lessons/learning.py) finds the completed runs, validates their artifacts and records input identity. The comparison reads column three from the MuJoCo `trace.csv` and `tcp_errors_m` from the PhysX payload.

This branch does not use `seed`, `samples` or `variant` as new experiment conditions. Adding `--variant 0.8` with unchanged producers does not change the engine, targets or controller. This is also separate from the training checkpoint path.

## Try it

### One-variable calculation: change one error difference

Without external execution evidence, perform only a calculation. Change the first difference in the example from 0.003 to 0.006 m, retaining the second at 0.004 m. Then $D=\sqrt{(0.006^2+0.004^2)/2}\approx0.0050990$ m. Explain why squaring gives larger deviations more weight. This varies one input to the analysis equation; it is not a new engine execution, policy evaluation or lesson-completion record.

For an actual engine-condition experiment, produce fresh records with the same conditions on both producer lessons, then analyze them. If their targets differ, failure is the correct result. Do not report `--variant` as a change to analysis inputs.

## Recovery

Preserve interrupted evidence. `pal course pause`, `pal course resume` and `pal lesson run sim-fr3-04 --resume-from BASE --json` inspect saved state without automatic motion. Restart short simulations in a fresh run. Follow [path guidance](../paths.md) for training resume and host transfer.

## Checkpoint

### Check your understanding

1. Why can both engines be far from the target despite a small D?
2. What does `reference` mean in this lesson's CSV?
3. Why review models and drives beyond the four matching fields?
4. Which parts can you study on a Mac without PhysX records, and what verification remains?

Record the two original runs, matched fields, D(m), joint/contact comparisons and unresolved conditions. Do not finish from calculations alone. Measured inputs, comparison and review must satisfy the common learning workflow before completion.

Answer guide: Two equally large errors can have zero difference. Reference holds MuJoCo measurements. Matching target fields does not prove matching drives or inertia. A Mac can analyze the equation and saved records, while genuine PhysX production and rendering verification require the corresponding runtime.

<!-- pal:navigation:start -->
## Next lesson

[core-enlight-03](./core-enlight-03.md)

This is catalog order. Use `pal course next --json` to select an eligible lesson.
<!-- pal:navigation:end -->
