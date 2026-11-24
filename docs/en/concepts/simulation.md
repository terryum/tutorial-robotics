<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/simulation.md" lang="ko">한국어</a> | <a href="simulation.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Simulation: state, time and reproducible evidence

## A model and its changing state are different objects

A simulator combines a model of the world with a numerical rule for advancing it. The model contains joint structure, geometry, mass, inertia, limits and integration settings. The state contains changing positions, velocities and other variables. MuJoCo separates `MjModel` from `MjData`; changing one joint's state does not change the robot's geometry definition.

After the host checks in setup, begin with [pendulum stepping](../lessons/core-01.md), [pinned sources](../lessons/core-02.md), [model inspection](../lessons/core-03.md) and [rendering](../lessons/core-04.md). Use the [host audit](../lessons/core-00.md) when you need a separate diagnostic. Python alone does not supply every runtime: the catalog distinguishes platform, dependencies, implementation status and verification. A valid picture does not establish correct dynamics.

For a simple revolute system, $q$ is position in rad and $v=\dot q$ is angular velocity in rad/s. A conceptual state is $s=[q,v]$. In a general robot `qpos` has `nq` elements while `qvel` has `nv`; these counts can differ because a free body's quaternion uses four position entries but three angular velocity entries. The actuator control vector has `nu` entries and is another separate object.

## What numerical stepping approximates

A dynamics equation is

$$
M(q)\dot v+b(q,v)=\tau+J(q)^Tf,\qquad E(t)=K(t)+U(t).
$$

$M$ is generalized inertia, $b$ collects bias forces, $\tau$ is applied generalized effort and $J^Tf$ maps contact forces into generalized coordinates. For a single rotation, inertia is kg m² and effort is N m; mixed rotational/translational systems need coordinate-specific units. $K$, $U$ and total energy $E$ are in joules. The simulator approximates the continuous evolution at finite time steps; it does not symbolically solve every trajectory.

The unforced, frictionless pendulum in [physics.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/physics.py) uses a distributed-mass capsule and RK4 with baseline $\Delta t=0.002$ s. Do not replace its inertia with a point-mass formula and expect identical dynamics. The lesson measures energy drift

$$
d=\max_i|E_i-E_0|.
$$

Worked calculation, **not measured output**: energies [1.000000, 1.000003, 0.999998] J give drift $3\times10^{-6}$ J.

```python
import numpy as np
energy_j = np.array([1.000000, 1.000003, 0.999998])
drift_j = np.max(np.abs(energy_j - energy_j[0]))
assert np.isclose(drift_j, 3e-6)
```

## Understand the experiment's clock

The pendulum lesson makes ten `mj_step` calls per saved row, then calls `mj_forward` to refresh derived state and records the sample. At baseline one row spans 0.02 s. With 64 rows the simulated duration is 1.28 s. A wall-clock duration on your computer is different from simulated time. A plot's row number is also different from time unless its sampling schedule is known.

The main comparison changes the release angle from 0.35 to 0.70 rad with the timestep and 1.28 s duration fixed. In the optional timestep experiment, double the integration step to 0.004 s while holding seed and sample count fixed. Saved rows now span 0.04 s and the total duration doubles. That comparison studies energy drift under the documented schedule; it does not isolate integration accuracy at equal elapsed time. To compare equal horizons, design a separate experiment and explicitly report its changed sampling schedule.

## Follow state and provenance into saved artifacts

`experiment.json` → `payload` → `state` contains rows `[time_s, q_rad, qvel_rad_s]`; `dt_s` records the integrator step. `trace.csv` contains the initial-energy reference and measured energy against time; `summary.json` reports `energy_drift` in joules. The numeric check requires drift below $10^{-5}$ J and recomputes from actual values. A success flag alone is not enough.

`run.json` and artifact hashes bind a run to source and files. [models.py, `provenance`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/models.py) checks pinned vendor bytes against `assets/model-lock.json`. Keep vendor caches read-only and derived conversions inside the ignored run directory. A fixed seed cannot compensate for changed model bytes, engine version, source or preprocessing.

The [public verification report](../../verification/reader-experience.md) labels its measured examples and source revision. They illustrate what was observed then; they are not fresh results for your checkout. Missing models or an unavailable engine must remain `capability-unavailable`, never a synthetic success.

## Check your understanding

1. Why can `nq`, `nv` and `nu` differ? Positions, velocity coordinates and actuator inputs represent different spaces.
2. Does a small energy drift establish a good controller? It checks one numerical behavior of an unforced model; no controller has been evaluated.
3. What must remain fixed for a reproducible comparison? Model/source/software identity and all declared inputs except the chosen variable.

Next connect joint positions to tool positions in [kinematics](kinematics.md), then effort to motion in [control and contact](control-contact.md).

## Equipment progression

Follow [equipment stages](../equipment-stages.md): laptop simulation first, a verified GPU runtime next, optional XR/glove/tracker/UMI collection after that, and physical robots last. The catalog lists 71 learning lessons and one Core diagnostic. The lesson counts are Core 32, Sim 27 and Hardware 12. The original portable scope is 32 Core plus deployment and offline sink; optional `core-teleop-01` adds one dependency-light synthetic-input lesson, for 35 portable lesson targets. This count does not verify native Mac live VR acceptance. Eleven physical lessons and the live-input `sim-teleop-01` remain scaffolded; the offline sink is the implemented hardware-stage exception.
