<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/reinforcement-learning.md" lang="ko">한국어</a> | <a href="reinforcement-learning.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Reinforcement learning: a learning run and a useful policy

## Learn from consequences

Feedback control writes a rule for acting; reinforcement learning adjusts a policy from the consequences of its actions. At time $t$, observation $o_t$ enters policy $\pi_\theta$, action $a_t$ changes the simulated state, and reward $r_t$ scores the transition. The environment also reports whether the task terminated or a time limit truncated it. A seed makes randomness reproducible within a fixed software/model environment; it is not evidence of generalization.

[Minimal PPO](../lessons/core-rl-01.md) uses a two-value pendulum observation and one action. [FR3 reach](../lessons/core-fr3-07.md) uses 17 observations: seven joint displacements from home (rad), seven joint velocities multiplied by 0.1, and three world-frame target errors multiplied by 10. These fixed numeric scales condition the policy input; they do not make the physical units disappear. A bias feature gives an 18-element input and FR3 weights of shape 18×7.

[learning.py, `Reach.step`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py) maps an unconstrained seven-vector $a$ into position targets:

$$
q_{target}=\operatorname{clip}(q+0.03\tanh(a),q_{min},q_{max}),\qquad
r=-\lVert x^*-x\rVert_2-0.001\sum_j a_j^2.
$$

Joint delta is in rad and distance is in m. Reward is a designed score with chosen numeric weights, not a physical energy. The penalty uses the pre-transform action $a$, while the robot receives a bounded delta. Ten simulator steps advance each control transition. `Reach` times out after 64 transitions; the later named-arm environment in `arm.py` allows 160. Read the actual environment before comparing episode lengths.

## Why PPO limits a policy update

A Gaussian policy samples around a mean. If a policy changes too much after one batch, the old samples cease to represent its new behavior. PPO uses the likelihood ratio $\rho_t=\pi_\theta(a_t|o_t)/\pi_{old}(a_t|o_t)$ and clips its incentive:

$$
L=\mathbb E\left[\min(\rho_t A_t,\operatorname{clip}(\rho_t,0.8,1.2)A_t)\right].
$$

$A_t$ estimates how much better an action was than expected. The clipped surrogate is an update objective, not a task success rate. The implementation normalizes advantages, performs four policy passes per rollout and clips the gradient norm. Training mean reward can fluctuate.

The advantage recursion distinguishes a genuine terminal state from a collection boundary:

$$
\delta_t=r_t+\gamma V(o_{t+1})(1-d_t)-V(o_t),\qquad
A_t=\delta_t+\gamma\lambda(1-b_t)A_{t+1}.
$$

Here $d_t$ marks task termination, $b_t$ marks termination **or** time truncation, $\gamma=0.99$ and $\lambda=0.95$. A timeout can bootstrap the next value but must not carry advantage from the reset episode. Worked calculation, **not a measured run**: reward 1, next value 2, current value 0 and illustrative $\gamma=0.5$ gives 2 for a timeout and 1 for a terminal state.

```python
import numpy as np
from pai_lab.lessons.learning import generalized_advantage
adv = generalized_advantage(
    np.array([1., 1.]), np.array([0., 0.]), np.array([2., 2.]),
    np.array([False, True]), np.array([True, True]), gamma=0.5,
)
assert np.allclose(adv, [2., 1.])
```

## Separate three claims in the saved evidence

[core-fr3-08](../lessons/core-fr3-08.md) saves `policy.npz`, `policy-contract.json`, `experiment.json` and `evaluation.json`. First inspect `parameter_delta` and `reload_max_error`: these establish an optimizer update and faithful reload. Then inspect independent evaluation, rather than treating the training reward graph as evaluation.

[arm.py, `evaluate`](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py) uses seed 10007 and twenty target episodes. Success requires ten consecutive control steps within 0.01 m; `performance_verified` requires at least 16 successes. These are simulation task criteria, explicitly `hardware_tolerance=False`. A finite changed policy can fail every target. The [public robot-path report](../../verification/robot-paths-2026-11-08.md) records such a short Enlight PPO example; it does not report a solved task.

For a one-variable comparison, change only the documented learning-rate multiplier while keeping seed, model, rollout count and evaluation targets fixed. Compare both optimizer diagnostics and independent successes. A larger learning rate can improve or damage results; do not select a claim from one favorable reward point. [Data and imitation](data-imitation.md) offers a supervised baseline, and [deployment](deployment-hardware.md) introduces further gates.

## Check your understanding

1. Is an updated weight matrix a useful policy? It proves learning code ran; usefulness requires independent task evaluation.
2. Why does truncation retain a next-state value? The task need not have ended when the collector stopped.
3. Does passing 16/20 make a physical arm ready? No; the threshold is confined to this simulated task.

For the GPU vendor lessons, `samples` can control both training iteration count and evaluation horizon. Treat a sample-count comparison as a coupled budget/horizon change and state both effects. For isolated optimization reasoning, hold those fixed and change only a supported learning-rate input. [NVIDIA ecosystem](../nvidia-ecosystem.md) separates Isaac Lab training from Sim engine checks and GR00T model experiments.
