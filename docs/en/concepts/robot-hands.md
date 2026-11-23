<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/robot-hands.md" lang="ko">한국어</a> | <a href="robot-hands.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Robot hands: geometry, synergy and contact observations

## Similar fingertips do not imply identical joints

An arm positions a tool; a hand must coordinate many joints around an object. Comparing hands requires more than equal-length arrays. Joint axes, ranges, actuator count, couplings, tendon behavior and fingertip frames differ. [Wuji poses](../lessons/core-wuji-01.md), [virtual tactile observations](../lessons/core-wuji-02.md), [Wuji–Sharpa comparison](../lessons/core-dexterity-01.md), [retargeting](../lessons/core-dexterity-02.md) and [Shadow Hand introduction](../lessons/core-shadow-01.md) make those distinctions observable.

A synergy reduces many joint coordinates to a few controls. For the single-amplitude Wuji teaching example,

$$
q=\operatorname{clip}(\alpha s,q_{min},q_{max}).
$$

$q,s\in\mathbb R^{20}$ have units rad, while amplitude $\alpha$ is dimensionless. In [hands.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/hands.py), abduction-named joints use synergy value 0.3 and other joints 0.6; amplitudes 0, 0.5 and 1 define open, half and closed poses before `variant` scaling. These are prescribed model poses, not a learned grasp strategy or verified grasp stability.

Worked calculation, **not measured hand data**: for a joint with $s_j=0.6$ rad and $\alpha=0.5$, its unclipped target is 0.3 rad.

```python
import numpy as np
synergy_rad = np.array([0.3, 0.6])  # illustrative two-joint subset
amplitude = 0.5
q_rad = np.clip(amplitude * synergy_rad, [-0.2, 0.0], [0.5, 0.8])
assert np.allclose(q_rad, [0.15, 0.30])
```

`experiment.json` → `payload` → `poses` contains each `qpos` vector and `tips_m`, a 5×3 array of world-frame fingertip positions. A norm of the whole joint vector has units rad but is not the angle of any one finger. Increasing a synergy amplitude can stop changing a joint once it reaches its range.

## Retarget displacement rather than copy joint indices

Retargeting asks another hand to reproduce a geometric relation. The teaching solver first aligns rest-pose fingertip clouds with an SVD-derived proper rotation. It maps source fingertip **displacements** into target world coordinates, then solves a bounded least-squares objective containing fingertip residual and a small joint regularizer:

$$
r(q)=\begin{bmatrix}\operatorname{vec}(p_{tips}(q)-p^*)\\0.002(q-q_0)\end{bmatrix}.
$$

There are five 3D tips, so the first residual has 15 elements in m. Joint differences are in rad; the numeric 0.002 factor scales them into the objective's metre-like residual scale. The reported `tip_error_m` is the norm of the **combined** residual, not a pure mean fingertip distance. Code and interpretation must keep that distinction. `retargeted-motion.npz` stores target-hand configurations; it does not certify collision-free or physical motion.

## A contact force is not a tactile calibration

MuJoCo computes contact forces from the simulated geometry and constraints. `mj_contactForce` returns six contact-frame components; force entries are in N and torque entries in N m. The Wuji virtual tactile experiment inserts a stimulus sphere, selects contacts involving that sphere, and sums absolute normal-force components. `payload.contacts` records `position_world_m` and `force_contact_N`; the latter field holds the six returned values, so do not interpret all six entries as force units solely from its name.

Changing only stimulus radius in the documented comparison may change penetration and the normal-force trace; it is not changing a physical taxel sensitivity. Shadow Hand's introductory check counts contacts involving its named `contact_object`, separating object contact from self-contact. Contact count, contact-force magnitude, and grasp success are three different observations.

The [public verification report](../../verification/reader-experience.md) contains measured Wuji/Sharpa examples. GPU in-hand PPO lessons require their actual prepared runtime and evaluation; a portable pose lesson does not establish a trained dexterous policy. Physical Wuji calibration and approved evaluation remain separate hardware stages.

## Check your understanding

1. Why not copy joint index 0 from Wuji to Sharpa? Names, axes, ranges and control meaning can differ.
2. Is one synergy as expressive as all joints? No; it restricts configurations to a low-dimensional family, which can simplify a task at the cost of expressiveness.
3. Is a virtual force sample a calibrated tactile sensor reading? No. Geometry and solver assumptions generate it.

Use [kinematics](kinematics.md) for frames and [control and contact](control-contact.md) for effort and force interpretation.

The Wuji virtual tactile scalar averages the per-time sums of absolute normal force; it is not a mean over individual contacts. For optional hand-input collection, follow [equipment stages](../equipment-stages.md). MANUS finger names and VIVE wrist frames need explicit calibration and correspondence; synthetic source labels do not establish live glove/tracker acceptance.
