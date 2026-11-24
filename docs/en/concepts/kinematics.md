<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/kinematics.md" lang="ko">한국어</a> | <a href="kinematics.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Kinematics: from joints to points and back

## Positions need a frame

A seven-number joint vector does not tell a beginner where the gripper is. Forward kinematics answers that question: $x=f(q)$ maps joint angles $q\in\mathbb R^7$ in rad to a tool point $x\in\mathbb R^3$ in m. The point is expressed in a named coordinate frame, usually world in these lessons. Tool orientation is a separate quantity; a position-only solution does not solve a six-dimensional pose task.

A rigid transform combines rotation $R$ (3×3, dimensionless) and translation $p$ (three elements, m):

$$
T=\begin{bmatrix}R&p\\0&1\end{bmatrix},\qquad
\begin{bmatrix}x_A\\1\end{bmatrix}=T_{AB}\begin{bmatrix}x_B\\1\end{bmatrix}.
$$

Here $T_{AB}$ maps coordinates from frame B to frame A. The final homogeneous coordinate is 1 for points. A displacement has final coordinate 0, so translation does not affect it. Read transform direction before multiplying; matrix multiplication is ordered.

<a id="relative-rotation" name="relative-rotation"></a>

### Transform composition and relative rotation

Suppose the origin of arm reference frame $A$ is at $(1,0,0)$ m in world frame $W$, and the axes of $A$ are rotated by $+\pi/2$ rad about world $z$. Tool frame $B$ has axes parallel to those of $A$ and an origin 1 m along the $+x$ direction of $A$. The origin of $B$ is therefore at $(1,1,0)$ m in world coordinates. With column vectors, apply the right-hand transform first in $T_{WB}=T_{WA}T_{AB}$. The transform $T_{AB}$ expresses the 1 m offset in $A$. Then $T_{WA}$ rotates it into world $+y$ and adds the world position of the arm reference. The frame used to express the tool offset determines its effect on the result.

If the current and goal rotation matrices $R_{\mathrm{cur}}, R_{\mathrm{goal}}$ each map tool coordinates to world coordinates, the relative rotation $R_{\mathrm{err}}=R_{\mathrm{cur}}^\top R_{\mathrm{goal}}$ expresses the goal axes in the current tool frame. Since $R_{\mathrm{cur}}R_{\mathrm{err}}=R_{\mathrm{goal}}$, it gives the rotation to apply to the current orientation. Keep the tool origin fixed at the position above and set the goal orientation to $+\pi$ rad about world $z$. The position error is 0 m and the relative rotation is $+\pi/2$ rad about the current tool $z$ axis. These are worked calculations for interpreting rigid transforms. [Modern Robotics, chapters 2 and 3](https://modernrobotics.northwestern.edu/nu-gm-book-resource/foundations-of-robot-motion/)

<a id="configuration-and-clearance" name="configuration-and-clearance"></a>

## Configuration space and collision clearance

For a fixed model, one joint-angle vector determines the position and orientation of every link. The set of possible robot configurations is the **configuration space**. Forward kinematics maps each configuration to a tip position. The set of those tip positions is the **position workspace**. Several points in configuration space can map to one point in the workspace.

Fix the base at the origin in a plane and join two line segments of length $l=1$ m. Measure the first joint angle $q_1$ from world $+x$ and the second angle $q_2$ from the first link. Counterclockwise is positive and both angles use rad. The elbow $E$ and tip $P$ are given by

$$
E=l(\cos q_1,\sin q_1),\qquad P=E+l(\cos(q_1+q_2),\sin(q_1+q_2)).
$$

The obstacle is a disk centered at $C=(0.5,0)$ m with radius 0.1 m. Find the closest point to $C$ **on either link segment** and subtract the radius from its distance to $C$ to get collision clearance. Positive means separation, zero means contact, and negative means part of a segment is inside the disk. In this zero-thickness link calculation, both configurations reach the same tip position.

| Joint angles $(q_1,q_2)$ (rad) | Elbow $E$ (m) | Tip $P$ (m) | Shortest distance from $C$ to the segments (m) | Clearance (m) |
| --- | --- | --- | --- | --- |
| $(0,\pi/2)$ | $(1,0)$ | $(1,1)$ | 0 | $-0.10$ |
| $(\pi/2,-\pi/2)$ | $(0,1)$ | $(1,1)$ | 0.50 | $+0.40$ |

The first configuration puts the first link through the center of the disk. In the second, the base origin is the point on the links closest to the center. The configurations are two solutions to the same position IK problem. The elbow lies in a different place in each, changing the collision clearance.

### The middle of a path can collide with both endpoints clear

Keep $q_2=0$ in the same scene and interpolate $q_1$ linearly from $-\pi/4$ rad to $+\pi/4$ rad. At both endpoints, the perpendicular projection of the obstacle center lands on the first link segment. The perpendicular distance is $0.5\sin(\pi/4)$ m, giving clearance of $0.5\sin(\pi/4)-0.10\approx+0.254$ m at each end. At the midpoint, $q_1=0$ places the first link through the center, giving clearance of $-0.10$ m. These are calculations for the planar model. Checking clearance along a robot path requires the collision geometry of each link, the obstacle locations, and a check between the endpoints. When checking samples, use a method that accounts for the intervals between them.

## The Jacobian is a local ruler

Near one configuration, small joint changes produce approximately linear point changes:

$$
\Delta x\approx J(q)\Delta q,\qquad J\in\mathbb R^{3\times7}.
$$

Each column says how that point moves when one joint changes. For revolute joints its units are m/rad. This is a local approximation, not a promise for arbitrarily large motion. [physics.py, `jacobian`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/physics.py) asks MuJoCo for the translational site Jacobian. The FR3 lesson compares it against centered finite differences:

$$
J_{:,j}\approx\frac{f(q+\epsilon e_j)-f(q-\epsilon e_j)}{2\epsilon}.
$$

$e_j$ selects joint $j$, and $\epsilon=10^{-6}$ rad at baseline. Updating positions requires `mj_forward` before reading a site position; assigning `qpos` alone does not refresh derived geometry.

### The motion direction lost at full extension

At $(q_1,q_2)=(0,0)$ the planar arm's tip is at $(2,0)$ m. An infinitesimal rotation of either joint moves the tip only in the $y$ direction to first order. The translational Jacobian there is $J=\begin{bmatrix}0&0\\2&1\end{bmatrix}$ m/rad, and its columns point in the same direction, giving rank 1. Bending the elbow so the links are no longer collinear makes the two columns independent and allows tip velocity in both planar directions. A configuration where the number of independent velocity directions drops is a **singular configuration**. Damping reduces the size of numerical updates, but cannot restore the missing direction at that configuration. [Modern Robotics, section 5.3](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-3-singularities/)

## Inverse kinematics chooses a small joint update

Seven joint variables for three position coordinates usually allow many solutions. Near a singularity, a direct inverse may not exist or may amplify noise. The lesson uses a damped least-squares step:

$$
\Delta q=J^T(JJ^T+\lambda I_3)^{-1}(x^*-x).
$$

The code uses a numerical regularizer $\lambda=10^{-4}$ for metre/radian coordinates; it has the same numerical scaling as entries of $JJ^T$. It clips each update to ±0.08 rad and then clips to model joint limits. It does not optimize collision clearance. The chapter [control and contact](control-contact.md) explains why a kinematic answer is not yet a dynamically achieved motion.

Worked calculation, **not a measured result**: a single local direction with $J=[0.2]$ m/rad and desired displacement 0.01 m gives $\Delta q=0.0498753$ rad with $\lambda=10^{-4}$, before limits. The following is the same solve pattern extended to a 3×7 toy Jacobian:

```python
import numpy as np
J = np.zeros((3, 7))
J[:3, :3] = np.diag([0.2, 0.3, 0.4])
error_m = np.array([0.01, 0.0, 0.0])
dq_rad = J.T @ np.linalg.solve(J @ J.T + 1e-4 * np.eye(3), error_m)
assert np.isclose(dq_rad[0], 0.04987531172069825)
```

## Follow the evidence

In [core-fr3-04](../lessons/core-fr3-04.md), `experiment.json` → `payload` contains `analytic`, `finite_difference` (both 3×7), `jacobian_max_error`, `target_m` and `ik_errors_m`. The plotted x-axis is **IK iteration**, not elapsed seconds. The check compares Jacobian disagreement with $10^{-6}$ and final position residual with 0.001 m. A low residual proves this solver reached this point under these model constraints; it does not establish orientation, torque limits or hardware calibration.

[Enlight model conversion](../lessons/core-enlight-02.md) compares independent vendor transforms and compiled MJCF positions. That checks conversion consistency. Agreement between two geometric descriptions does not identify true physical inertia. [FR3 trajectory tracking](../lessons/core-fr3-09.md) then connects a series of kinematic targets to actual simulated dynamics.

For one-variable reasoning, change finite-difference $\epsilon$ while preserving pose and target. Larger $\epsilon$ increases truncation error; excessively small $\epsilon$ amplifies subtraction roundoff. It may leave the separate IK residual unchanged because the analytic Jacobian still drives IK. The comparison is about the numerical check, not necessarily improved reaching.

## Check your understanding

1. Why is a 3×7 Jacobian not inverted directly? It is rectangular and can be rank deficient.
2. Why call `mj_forward` after modifying `qpos`? Site positions and other derived quantities must be recomputed.
3. Does a small position residual ensure the tool orientation? No; orientation was absent from this objective.

Optional [teleoperation](../equipment-stages.md) adds a second transform chain: device frame → calibrated world frame → mounted wrist/tool frame. `sim-teleop-02` teaches this using synthetic integrated input; live Quest/MANUS/VIVE acceptance is separate. Preserve raw frame/clock labels alongside transformed values so a plausible pose does not conceal the wrong convention.
