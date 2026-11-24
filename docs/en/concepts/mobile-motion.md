<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/mobile-motion.md" lang="ko">한국어</a> | <a href="mobile-motion.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Mobile robots and motion: playback, dynamics and coordinated reach

## Watching movement is not the same as controlling it

A motion file can prescribe a body's joint positions without explaining the effort, balance or contacts that would produce them. [G1 playback](../lessons/core-g1-01.md) deliberately teaches this boundary. [G1 GPU learning](../lessons/sim-g1-01.md) requires a separate runtime, optimizer and independent evaluation. [Stretch 3 introduction](../lessons/core-stretch3-01.md) instead steps simulated dynamics with named wheel, lift and arm actuators.

A free base adds global translation and orientation to joint state. It is not another motor array. In MuJoCo a free joint contributes seven position coordinates (three position and four quaternion entries) and six velocity coordinates. Use `jnt_qposadr`, `jnt_dofadr` and actuator names to address the right arrays. Assigning a seven-value free-base state to wheel controls confuses state representation with action semantics.

## A bounded cycle is a data example

The G1 teaching trajectory adds a sinusoid to hinge coordinates:

$$
q_j(\phi)=q_{home,j}+0.08\,v\sin\phi,\qquad \phi\in[0,2\pi].
$$

$q_j$ and amplitude 0.08 have units rad, $v$ is dimensionless `variant`, and $\phi$ is a dimensionless phase. The implementation clips to joint limits and calls `mj_forward`; it does not solve a walking controller or integrate torque-driven locomotion. `motion.npz` holds `qpos` of shape `(samples, nq)`, `dt=0.02` s and joint names. Replaying those same coordinates can be exact even when the motion is physically unbalanced.

Worked calculation, **not a measured walking result**: at $\phi=\pi/2$ and $v=1$, the displacement is 0.08 rad; at $v=0.8$ it is 0.064 rad.

```python
import numpy as np
phase = np.pi / 2
baseline_rad = 0.08 * np.sin(phase)
comparison_rad = 0.08 * 0.8 * np.sin(phase)
assert np.isclose(comparison_rad, 0.064)
assert comparison_rad < baseline_rad
```

[Hands and motion implementation](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/hands.py) reports `replay_max_error` and `loop_error`. A zero replay error demonstrates exact saved-state playback. The first and final phase produce a closed cycle; neither observation establishes balance, foot clearance, power use or learned walking performance.

## Coordinate base and arm without mixing their roles

A mobile manipulator can move the base to improve an arm's reach. [embodiments.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/embodiments.py) names Stretch controls `left_wheel_vel`, `right_wheel_vel`, `lift`, `arm`, wrist actuators and `gripper`. Wheel controls are velocity commands; arm/lift controls follow their model actuator semantics. The base remains free state influenced by dynamics and contact.

For intuition only, an ideal differential-drive base satisfies

$$
v_{body}=\frac r2(\omega_R+\omega_L),\qquad
\dot\psi=\frac rL(\omega_R-\omega_L).
$$

$r$ is wheel radius in m, $L$ wheel separation in m, $\omega$ wheel angular velocity in rad/s, $v_{body}$ forward speed in m/s and yaw rate $\dot\psi$ in rad/s. This ideal no-slip model explains same-sign motion versus opposite-sign turning; the lesson does not estimate $r$ and $L$ from these equations.

The final phase creates a world target from the simulated gripper position and base forward axis. It corrects planar error with wheel commands and vertical error with lift. Read `groups`, `free_base`, `actuator_names`, `commands`, `tcp_positions_m`, `reach_target_m` and `reach_errors_m` in `experiment.json`. The plot changes interpretation from TCP height to reach error after the reach target exists; do not call the entire trace one stationary-goal error curve.

<a id="differential-drive-motion-order" name="differential-drive-motion-order"></a>

## Differential-drive motion depends on the order of moves

Assume a level surface and wheels that roll without slipping. The body frame's $x$-axis points forward and its $y$-axis points left. Take the midpoint of the axle as the base position. Its instantaneous velocity in the body frame is $(v_{body},0)$ m/s. For heading $\psi$ measured counterclockwise from the world $x$-axis, the velocity in the world frame is

$$
\begin{bmatrix}\dot x\\\dot y\end{bmatrix}
= v_{body}\begin{bmatrix}\cos\psi\\\sin\psi\end{bmatrix}.
$$

For a worked calculation, start at the origin facing world $+x$. Apply each move once: turn in place $90^\circ$ counterclockwise and travel 1 m straight ahead.

| Order of moves | Final world position | Final heading |
|---|---|---|
| Turn, then drive forward | $(0,1)$ m | $90^\circ$ |
| Drive forward, then turn | $(1,0)$ m | $90^\circ$ |

After turning first, the world $x$ displacement is $(1\,\mathrm m)\cos 90^\circ=0$ and the world $y$ displacement is $(1\,\mathrm m)\sin 90^\circ=1\,\mathrm m$. The final point is to the left of the original base position as viewed from its starting heading. The base still drives along its own forward axis, with zero lateral velocity in the body frame. [Modern Robotics covers the wheel constraint and instantaneous velocity in more detail](https://modernrobotics.northwestern.edu/nu-gm-book-resource/13-3-1-modeling-of-nonholonomic-wheeled-mobile-robots/).

In the [Stretch 3 lesson](../lessons/core-stretch3-01.md), MuJoCo computes wheel–floor contacts and updates the free base's state. The table is an idealized calculation comparing the two orders of motion. Use the run records to check how far and in what direction the base moved and where the TCP was.

## Comparison and evidence boundary

For G1, change only `variant` to reduce amplitude while preserving sample count, seed and model. Expect smaller hinge displacement but still exact replay; that is the intended invariant. For Stretch, `variant` changes parts of the prescribed schedule and the resulting state, so treat it as the documented schedule experiment rather than one isolated controller-gain test. The [public report](../../verification/robot-paths-2026-11-08.md) describes modest reach-error reduction, not millimetre accuracy or a trained mobile policy.

1. Can exact playback prove dynamic feasibility? No; forward kinematics can display prescribed states without a balance controller.
2. Why use actuator names? Free-base and joint-state layouts differ from control layouts.
3. Does decreasing a simulated target error authorize physical base movement? No; [hardware gates](deployment-hardware.md) remain separate.
