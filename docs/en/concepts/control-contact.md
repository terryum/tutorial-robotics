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

At rest a PD controller may retain error because its spring torque balances gravity. The gravity lesson adds `data.qfrc_bias`, MuJoCo's bias force term, which includes velocity-dependent effects as well as gravity. It is not a measured hardware gravity calibration. For Cartesian force $f$ in world coordinates, the translational Jacobian maps it into joint torque as $\tau=J^T f$: $J$ is 3×7 with units m/rad, $f$ is a three-vector in N. Task-space control also uses the mass matrix; it is not simply the same scalar PD law applied to Cartesian position.

Contact changes the problem: penetration and relative motion produce constraint forces. A useful dry-friction model is $\lVert f_t\rVert\leq\mu f_n$, with normal force $f_n\geq0$, tangential force $f_t$ in N and dimensionless friction coefficient $\mu$. This is an explanatory bound, not a claim that every simulator uses an identical friction solver. MuJoCo contact forces are expressed in a contact frame; the first component returned by `mj_contactForce` is normal force. The lesson sums absolute normal components only for the named probe/table pair. `normal_force_N` is simulation output, not a calibrated force sensor reading.

## What to observe and change

Use `experiment.json` → `payload` → `gain`, `kd`, `target_qpos`, `qpos`, `torque_nm`, `commanded_joint_error`. Read `checks` separately at the top level of `experiment.json`, beside `payload`. Compare the first commanded joint with the whole-arm norm; they answer different questions. Existing public measurements are in the [verification report](../../verification/reader-experience.md); rerunning is required for your own evidence.

For the documented one-variable PD experiment, raise `kp` from 120 to 180 while holding `kd` fixed at 21.9089, seed and sample count fixed. Expect a stronger restoring request; you cannot assume proportional error improvement once saturation or gravity matters. The legacy `variant` changes both gains and is a different comparison. For contact, changing friction may leave normal force nearly unchanged when sliding friction is not the dominant effect. Invariance can be the correct result.

## Check your understanding

1. Why can zero velocity coexist with nonzero position error? Gravity can balance the proportional torque.
2. Why compare raw and applied torque? Clipping can make the applied command smaller than the feedback calculation.
3. Does a low contact error authorize a probe on hardware? No. [Deployment and hardware](deployment-hardware.md) requires separate tool, frame, controller and per-run gates.
