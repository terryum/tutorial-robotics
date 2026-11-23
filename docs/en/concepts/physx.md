<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/physx.md" lang="ko">한국어</a> | <a href="physx.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# PhysX: a second engine needs its own evidence

## Import is the beginning of a comparison

Two pictures of the same robot can conceal different mass, joint, actuator and contact models. A second-engine experiment asks whether a task behaves similarly after those contracts are checked. MuJoCo output renamed as PhysX output cannot answer that question. [Isaac asset import](../lessons/sim-isaac-01.md) and [camera data](../lessons/sim-isaac-02.md) first establish import and rendering. [FR3 PhysX control](../lessons/sim-fr3-01.md) exercises actual physics; [matched FR3 comparison](../lessons/sim-fr3-04.md) consumes two completed runs.

The adapter must map joints by name, rather than assuming exported arrays retain their order. If $q_A$ is an $n$-vector in engine A and $P$ is the name-based permutation matrix, then $q_B^{aligned}=Pq_B$. Angles are in rad for revolute joints; prismatic coordinates are in m. Free-base position, quaternion and velocity do not form a generic motor command vector. Match axis signs, limits, base fixation, collision, inertia, drive gains and coupling semantics before interpreting errors. An unverified mimic/tendon conversion is a blocking gap.

## Define the quantity before comparing it

For sample $i$, let $e_i^A=\lVert x_i^*-x_i^A\rVert_2$ and $e_i^B=\lVert x_i^*-x_i^B\rVert_2$, both in m, with world-frame targets. The FR3 comparison reports

$$
D=\sqrt{\frac1N\sum_{i=1}^N(e_i^A-e_i^B)^2}.
$$

$D$ is the RMS **difference between error magnitudes**. It is not the RMS vector distance between the two TCP trajectories: opposite direction errors can have equal magnitude and give $D=0$. Do not call agreement in this scalar proof of identical dynamics.

Worked calculation, **not a measured engine result**: errors [0.01, 0.02] m and [0.012, 0.018] m give $D=0.002$ m.

```python
import numpy as np
error_a_m = np.array([0.01, 0.02])
error_b_m = np.array([0.012, 0.018])
difference_rmse_m = np.sqrt(np.mean((error_a_m - error_b_m)**2))
assert np.isclose(difference_rmse_m, 0.002)
```

[comparison.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/comparison.py) obtains actual completed `core-fr3-09` and `sim-fr3-01` evidence using `previous_run`. It rejects unequal `frame`, `initial_q_rad`, `tcp_targets_m`, `control_dt_s`, or sample counts. Catalog capability metadata for the comparison permits portable analysis; producing its PhysX input still requires a separate installed, verified Isaac/GPU environment. Machine names such as WS1 or WS2 do not supply that capability.

## Trace the output back to its producer

The comparison payload in `experiment.json` contains `engine_a`, `engine_b`, `tcp_error_difference_rmse_m`, `joint_errors_a_rad`, `joint_errors_b_rad`, `contacts_a_N`, `contacts_b_N`, `control_dt_s` and `hardware_tolerance=False`. Plot x is seconds and the two curves are TCP error magnitudes in m. The current producer creates its trace time labels at 0.02 s spacing; the input timing contract must still match. Inspect the source run timestamps when interpreting timing.

The contact arrays are inherited from the source runs. In the MuJoCo trajectory producer, `contact_force_norms_N` sums absolute normal components over all contacts; despite the field name it is not a full six-dimensional contact wrench norm. Do not infer matched physical contact simply from an array name. Inspect named bodies and each producer's force calculation. Camera images and finite numbers are necessary artifacts, but neither alone demonstrates correct drives.

For one-variable reasoning, fix the two input runs and change only the comparison lesson's legacy `variant`. This producer does not use `variant`, so the result should be invariant. To investigate a controller gain, produce a new matched pair with only that gain changed under the same target/frame/timing contract; do not silently compare mismatched tasks.

## Verification boundary and questions

The [public path verification record](../../verification/robot-paths-2026-11-08.md) explicitly separates Mac simulation checks from unavailable Isaac runtime verification. Preserve `reader_test_required` where actual evidence is missing. A strict docs build or adapter unit test does not execute PhysX.

1. Can a portable computer analyze existing PhysX evidence? Yes, but it must obtain genuine validated input; it cannot manufacture missing runs.
2. Does $D=0$ ensure the TCP positions coincide? No, equal error magnitudes may point in different directions.
3. Does engine agreement authorize hardware? No. Continue to [deployment and hardware](deployment-hardware.md) for independent gates.

## Where the NVIDIA tools fit

Use the [NVIDIA ecosystem guide](../nvidia-ecosystem.md) to connect Isaac Sim scene/PhysX verification, Isaac Lab task and training interfaces, Isaac teleoperation input/retargeting, and GR00T data/model experiments. These are separate contracts and environments; installation or import of one does not verify the others. Move from GPU simulation to optional collection before requesting physical robot gates.
