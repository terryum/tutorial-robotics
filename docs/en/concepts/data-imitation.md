<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/data-imitation.md" lang="ko">한국어</a> | <a href="data-imitation.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Data and imitation: learn a mapping, then test its consequences

## A demonstration is a timed transition

Imitation learning fits a policy to example actions. The usefulness of the result depends on what each row means: observation before action, action units, next observation after stepping, episode boundaries, timing and source identity. A random table of joint numbers cannot substitute for a demonstrated task.

[Episode recording](../lessons/core-data-01.md) stores a real simulated pendulum in `episode.jsonl`. Each row has `episode`, `step`, `time_s`, `observation`, `action`, `next_observation`, `terminated` and `truncated`. Observation has shape (2,) with units [rad, rad/s]; action has shape (1,) with units N m. In [learning.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py), observation is read before the control, ten physics steps follow, and `time_s` labels the resulting state. Remember that timing convention when aligning logs.

Eight episodes and `samples` transitions per episode give $N=8\times samples$. With 64 samples, the expected count is 512. This count is a contract calculation, not a new measurement. Each episode starts with its own seeded initial angle; adjacent rows in an episode are strongly related.

## Behavioral cloning is supervised regression

For observation matrix $X\in\mathbb R^{N\times3}$, append a constant 1 to the two pendulum observation values. Targets $Y\in\mathbb R^{N\times1}$ hold demonstrated torques. [The BC baseline](../lessons/core-il-01.md) fits $W\in\mathbb R^{3\times1}$ with

$$
\hat Y=XW,\qquad L=\frac1N\sum_{i=1}^N(\hat Y_i-Y_i)^2,\qquad
\nabla_W L=\frac2N X^T(XW-Y).
$$

Loss has units (N m)². Weight units depend on the corresponding feature. A scalar loss reduction is not a physical displacement improvement. Worked calculation, **not measured training**: predicted torques [0.2, 0.4] N m versus targets [0.1, 0.6] N m give MSE 0.025 (N m)².

```python
import numpy as np
predicted_nm = np.array([0.2, 0.4])
target_nm = np.array([0.1, 0.6])
mse_nm2 = np.mean((predicted_nm - target_nm)**2)
assert np.isclose(mse_nm2, 0.025)
```

The pendulum lesson trains on episodes 0–5 and holds out episodes 6–7. Do not randomly mix adjacent steps from the same episode into both sets and call that an independent episode test. Inspect `training_rows`, `heldout_rows`, `heldout_mse`, `weights`, `source_sha256` and `reload_max_error` in `experiment.json`. `policy.npz` contains the actual learned matrix. Small held-out action error says the policy approximated this data distribution; running the policy can reach unfamiliar states and requires separate rollout evaluation.

## Keep the arm and chunk contracts distinct

[FR3 demonstrations and BC](../lessons/core-fr3-10.md) and [Enlight demonstrations and BC](../lessons/core-enlight-04.md) use separate model-specific datasets. [arm.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/arm.py) labels thirty episodes: 20 train, 5 validation, 5 test. Its observation is 17 values and its seven actions become bounded joint deltas. [training.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/training.py) saves identity, fixed normalization, optimizer, RNG and data digest for exact-contract resume. The separate twenty-target evaluator checks task success; its `performance_verified` is not inferred from BC loss.

[ALOHA and ACT contract](../lessons/core-aloha-01.md) instead builds an action tensor with shape `(samples, 16, 14)`: sample, chunk horizon, dual-arm actuator. The code creates prescribed chunks and applies only the first action of each chunk. `contract_only=True` and `ACT_trained=False` are essential. This teaches storage and interface shape; no ACT network is trained by this lesson.

For one-variable reasoning, change only the BC learning-rate multiplier with fixed input data, split, seed and step budget. Compare training loss, held-out MSE and reload agreement; for arms additionally inspect independent rollout success. Changing a chunk horizon would alter a different contract and must not be described as the same BC learning-rate experiment.

<a id="task-symmetry" name="task-symmetry"></a>

## Does rotating the scene preserve the task?

Suppose you push an object along a straight line from the origin to $(1,0)$ m on an obstacle-free plane. Rotate the object and the goal $90^\circ$ counterclockwise about the world origin. The rotated goal is $(0,1)$ m. Rotate the world coordinates and goal displacement in the observation, along with the Cartesian motion command. The demonstration that pushes 1 m east now corresponds to pushing 1 m north. This calculation assumes the motion conditions and the success criterion are the same in both directions.

Now place a fixed wall at $y=0.5$ m over $-0.25\le x\le 0.25$ m. The wall stays in place as the object rotates. Model the object as a point. The eastward path clears the wall, and the northward path meets it at $(0,0.5)$ m. Rotating the observations and commands together still changes which path is feasible, so the task lacks that rotational symmetry.

[Independent FR3 reach evaluation](../lessons/core-fr3-10.md) runs the policy on separately sampled goals in the same simulated scene. It checks closed-loop reach on that separate goal sample. Using rotated demonstrations in a new scene with a fixed obstacle requires a separate check of collisions and success conditions.

## Check your understanding

1. Why split by episode? Nearby steps share trajectories, so row-level mixing can leak nearly identical states into evaluation.
2. Does small action MSE guarantee closed-loop success? No. A policy can drift into states absent from the demonstration distribution.
3. Does an ACT-shaped batch mean ACT was trained? No; the contract lesson explicitly records otherwise.

Continue with [reinforcement learning](reinforcement-learning.md) to learn from interaction or [VLA](vla.md) to inspect multimodal policy interfaces.

## Optional collection without live-device claims

After the laptop and GPU stages, [optional collection](../equipment-stages.md) introduces Quest 3, MANUS, VIVE or UMI workflows where their actual capabilities exist. `core-teleop-01` creates synthetic episodes; `sim-teleop-02` combines synthetic VIVE wrist, MANUS fingers and Quest switch data through calibrated transforms; `sim-enlight-06` records synthetic Enlight MuJoCo camera/state/action episodes. Their `provenance`, episode status and split fields must remain visible. The [VR verification record](../../verification/vr-teleop-2026-11-13.md) reports software tests and synthetic data, with actual USB devices absent and no human collection acceptance. A three-episode synthetic split is a software contract example, not a sufficient human demonstration dataset. External BC requires compatible model/action/observation contracts and disjoint episodes; its separate evaluation may fail. Connect processors and dataset semantics to the [NVIDIA ecosystem](../nvidia-ecosystem.md) before GR00T experiments; a compatible-shaped export alone is not model performance.
