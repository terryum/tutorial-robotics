<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/control-contact.md" lang="ko">한국어</a> | <a href="control-contact.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Control and contact: error, effort and constraints

## Why an arm needs feedback

A target is a request; it does not specify the effort needed to reach it. A joint displaced from its target behaves intuitively like a spring: the larger the error, the larger the restoring torque. A damper resists velocity, reducing oscillation. Gravity and contact add forces even when the target is stationary. This chapter connects those ideas to [joint PD](../lessons/core-fr3-02.md), [gravity compensation](../lessons/core-fr3-03.md), [task-space control](../lessons/core-fr3-05.md) and [contact](../lessons/core-fr3-06.md).

Start with joint position $q$ and target $q^*$, both seven-element vectors in radians. Joint velocity $\dot q$ has units rad/s. The simple controller assumes a stationary target:

$$
\tau_{raw}=K_p(q^*-q)-K_d\dot q,\qquad
\tau=\operatorname{clip}(\tau_{raw},\tau_{min},\tau_{max}).
$$

Torque is in N m; $K_p$ is N m/rad and $K_d$ is N m s/rad. In the first teaching experiment one scalar gain is applied to every joint. Clipping acts element by element. It keeps the requested effort inside model limits but does not prove stability or physical safety. A derivative term on error would additionally require target velocity; this implementation damps measured velocity.

For an isolated joint with inertia $I$, ideal critical damping is $K_d=2\sqrt{I K_p}$. The code's numerical rule $2\sqrt{K_p}$ uses a reference inertia of 1 kg m². A coupled seven-joint arm has configuration-dependent inertia, so that rule is a teaching choice rather than a general robot tuning law.

## A calculation you can follow into code

Worked calculation, **not a measured result**: with error 0.18 rad, zero velocity and $K_p=120$, raw torque is $120\times0.18=21.6$ N m. With $K_d=21.9089$ and velocity 0.1 rad/s it becomes 19.40911 N m. Saturation may reduce the applied value.

```python
import numpy as np
error_rad = np.array([0.18])
velocity_rad_s = np.array([0.1])
raw_nm = 120.0 * error_rad - 21.9089 * velocity_rad_s
applied_nm = np.clip(raw_nm, -15.0, 15.0)  # illustrative limit
assert np.allclose(applied_nm, [15.0])
```

The 15 N m limit above is an illustrative arithmetic limit, not the FR3 limit. [physics.py, `arm_control`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/physics.py) reads actual clipping bounds from `model.jnt_actfrcrange`, disables model actuation and writes `qfrc_applied`. This avoids adding a second actuator controller. `control.csv` records target, position, velocity, raw torque and applied torque **before** each integration step. The plotted whole-arm error is sampled after each group of 25 steps. Do not combine a post-step position with a pre-step torque to check the equation.

## Gravity, coordinates and contact

<a id="gravity-and-bias" name="gravity-and-bias"></a>

### From holding torque to the equation of motion

An arm held still in the air has $\dot q=\ddot q=0$. Ignoring contact and passive torque, the motors must supply the gravity term $g(q)$ at that configuration. As in the PD calculation above, position error produces proportional torque. Position error can persist when this torque alone balances gravity. When the arm moves or experiences an external load, additional terms enter the joint equation of motion.

$$
M(q)\ddot q+c(q,\dot q)+g(q)=\tau+\tau_{\mathrm{other}}.
$$

The 7×7 joint-space inertia matrix $M(q)$ (kg·m²) depends on the current configuration. Multiplying it by $\ddot q$ (rad/s²) gives the torque needed for joint acceleration. Off-diagonal terms describe how accelerating one joint can affect the torque needed at another. The term $c$ accounts for Coriolis and centrifugal effects, and $g$ accounts for gravity. Here $\tau$ is control torque, while $\tau_{\mathrm{other}}$ includes joint torques from contact, other external loads and passive effects. Each vector term in the equation of motion has units of N·m. [MuJoCo's equation of motion](https://mujoco.readthedocs.io/en/stable/computation/index.html#general-framework)

The gravity-compensation lesson adds `data.qfrc_bias`, which contains $c+g$, to the PD request and then applies the joint torque limits. In the worked example above, at zero velocity and with 0.18 rad of error for one joint, adding 4 N·m of bias to the 21.6 N·m PD torque gives 25.6 N·m before clipping. With the same illustrative limits of ±15 N·m, both requests apply 15 N·m. This calculation shows how saturation can leave the applied torque unchanged when compensation is added.

<a id="jacobian-power" name="jacobian-power"></a>

### The Jacobian and power

The translational Jacobian $J$ (3×7, m/rad) maps joint velocity $\dot q$ (rad/s) to linear velocity $v=J\dot q$ (m/s) at the tool site. A force $f$ (N) applied at the same site and expressed in the same frame contributes power $f^\top v$ (W). This equals joint-side power $\tau_f^\top\dot q$, so $f^\top J\dot q=\tau_f^\top\dot q$ for every $\dot q$, and the torque contribution is $\tau_f=J^\top f$. The lesson's task-space controller uses $M(q)$ and $J$ at the current configuration to calculate the force for a linear acceleration request.

To include rotation, pack the force $f$ and the moment $m$ (N·m) about the same point into a six-element vector called a wrench. Express the linear velocity $v$ at that point and angular velocity $\omega$ (rad/s) in the same frame. The power is $f^\top v+m^\top\omega$. When a six-row Jacobian gives both velocities, match the order of its rows with that of the wrench components. When shifting the moment to a new reference point while keeping the axes fixed, add $r\times f$ to the original moment. Here $r$ points from the new reference point to the original one. [Modern Robotics on Jacobians and wrenches](https://modernrobotics.northwestern.edu/nu-gm-book-resource/5-2-statics-of-open-chains/)

<a id="contact-force-and-friction" name="contact-force-and-friction"></a>

### Contact forces and friction

The compressive normal force $f_n\geq0$ acts perpendicular to the contact surface. The tangential force $f_t$ acts along the surface. Both have units of N. In the ideal Coulomb model, static friction can supply $\lVert f_t\rVert\leq\mu f_n$, with dimensionless friction coefficient $\mu$. Sliding occurs if preventing it would require more tangential force. In the single-coefficient model, sliding friction has magnitude $\mu f_n$ and acts opposite the relative sliding velocity. To apply this model to a grasp, use each admissible contact force to compute its moment about a common point on the object. This lets you check whether the contacts can counter the external force and moment together. [Modern Robotics on friction cones](https://modernrobotics.northwestern.edu/nu-gm-book-resource/12-2-1-friction/)

MuJoCo solves for constraint forces according to its contact model. The first component returned by `mj_contactForce` is the normal force in the contact frame. In the probe lesson, `normal_force_N` is the simulation's sum of absolute normal components for the named probe/table pair. [MuJoCo contact-force API](https://mujoco.readthedocs.io/en/stable/APIreference/APIfunctions.html#mj-contactforce)

## What to observe and change

Use `experiment.json` → `payload` → `gain`, `kd`, `target_qpos`, `qpos`, `torque_nm`, `commanded_joint_error`. Read `checks` separately at the top level of `experiment.json`, beside `payload`. Compare the first commanded joint with the whole-arm norm; they answer different questions. Existing public measurements are in the [verification report](../../verification/reader-experience.md); rerunning is required for your own evidence.

For the documented one-variable PD experiment, raise `kp` from 120 to 180 while holding `kd` fixed at 21.9089, seed and sample count fixed. Expect a stronger restoring request; you cannot assume proportional error improvement once saturation or gravity matters. The legacy `variant` changes both gains and is a different comparison. For contact, changing friction may leave normal force nearly unchanged when sliding friction is not the dominant effect. Invariance can be the correct result.

## Check your understanding

1. Why can zero velocity coexist with nonzero position error? Gravity can balance the proportional torque.
2. Why compare raw and applied torque? Clipping can make the applied command smaller than the feedback calculation.
3. Does a low contact error authorize a probe on hardware? No. [Deployment and hardware](deployment-hardware.md) requires separate tool, frame, controller and per-run gates.
