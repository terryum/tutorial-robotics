<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/deployment-hardware.md" lang="ko">한국어</a> | <a href="deployment-hardware.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Deployment and hardware: evidence changes authority in stages

## A policy file is one part of a contract

Deploying a policy means preserving what its numbers mean: model identity, observation order, scaling, action units, frame, timing, dependency versions and rollback behavior. A seven-number output is ambiguous without that contract. A FR3 joint vector is not an Enlight vector merely because both arms have seven joints.

[Candidate packaging](../lessons/sim-deploy-01.md) records trained policy bytes and deterministic test vectors. [Offline runtime and sink](../lessons/hw-common-01.md) repeats inference without emitting commands. These are portable software activities. The later [read-only gate](../lessons/hw-common-02.md) and [Enlight probe preparation](../lessons/hw-enlight-05.md) require independent physical evidence and remain scaffolded where that evidence is missing.

For the portable candidate, let $o$ be the 17-value normalized-by-fixed-scales observation, $\tilde o=[\operatorname{clip}(o,-5,5),1]$ its 18-value biased feature vector and $W$ an 18×7 weight matrix. Inference is

$$
a=\tanh(\tilde oW),\qquad \Delta q=0.03a.
$$

$a$ is bounded and dimensionless; the simulator interprets $\Delta q$ in rad. Bounding a position delta does not bound every velocity, torque or contact force. The manifest's `rate_hz=50` describes the contract; offline test-vector iteration is not a real-time scheduling test.

Worked calculation, **not a robot measurement or command**: a pre-transform value 0.5 gives $a=0.462117$ and $\Delta q\approx0.0138635$ rad.

```python
import numpy as np
pre_transform = np.array([0.5])
normalized_delta = np.tanh(pre_transform)
sim_delta_rad = 0.03 * normalized_delta
assert np.allclose(sim_delta_rad, [0.013863514717800292])
```

## Follow the portable evidence

[deployment.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/deployment.py) creates `sample_candidate/manifest.json`. Read `policy.sha256`, `files`, `test_vectors`, `observation_order`, `action_order`, `frame`, `units`, `normalization`, `rollback`, `promotion` and `performance_verified`. The course candidate is `candidate-only`; this packaging path explicitly records `performance_verified=False` and rollback `command-sink`. It does not promote a policy to hardware.

`validate_candidate` checks hashes, path containment and numeric test-vector agreement. This guards reproducible bytes and interface behavior, not trusted origin or task safety. The sink lesson saves `inference.json`; its payload reports `emitted_command_count=0`, `inference_count`, `replay_exact` and the manifest hash. It intentionally has no publisher, socket, vendor SDK or execution callback. A thought comparison that changes a test vector's observation may change inference; changing the legacy `variant` cannot add a transport that does not exist.

## Physical readiness is a separate progression

Read [the safety contract](../../07_SAFETY.md) before any physical work:

```text
offline replay → command sink → read-only → live shadow
→ torque-disabled replay → fresh exact-action card → one approved action
```

At each step verify exact model/device identity, disabled/error/E-stop state, joint and frame semantics, limits, watchdog, timeout, stale-state rejection, tool/payload and isolated networking. Live shadow can observe and calculate; it does not authorize actuation. A simulation badge never substitutes for these facts.

[run_card.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/hardware/run_card.py) is an exact-action gate for an **injected independently validated transport**. It supplies no vendor connection, torque-enable or controller API. Its implemented card supports one Enlight small joint move: seven finite rad targets, arm group, at most 0.02 rad change, timeout at most 1 s, validity window at most 60 s, exact approval and single-use consumption. These are this gate's software constraints, not universal safe motion limits. It requires fresh matching preflight, compatibility/tool reviews and a tested stop path. Approval is consumed before transport execution; uncertainty or failure must be reconciled rather than retried automatically.

## Contact preparation without pretending to execute

Probe plane-force preparation needs a reviewed TCP transform, calibrated plane normal, payload and separately validated force controller. A frame error rotates the meaning of desired force: if $R$ maps tool to world, $f_{world}=Rf_{tool}$, with both three-vectors in N. A paper calculation may vary one angle and inspect the changed direction; it is not permission to touch a surface. A gripper task additionally needs mounting, width conversion, status/timeout/stop behavior and load review. Description v4 versus Enlight RDK 2.1/v3E.1 compatibility remains unverified until device evidence resolves it.

## Check your understanding

1. What does a correct hash prove? The bytes match the expected digest; it does not prove a safe controller.
2. Does zero emitted commands show hardware readiness? It demonstrates the sink's software boundary only.
3. May a scaffolded lesson be finished after a paper calculation? No. Document the preparation and missing evidence; preserve its blocked state.

Optional [XR/glove/tracker/UMI collection](../equipment-stages.md) sits before actual robot authority. `CommandSink` in the teleoperation module and the deployment lesson's inference sink are distinct implementations; both keep physical publishers absent. The teleop gate latches at exactly 100 ms stale input and requires fresh release, local rearm and fresh press. Synthetic watchdog tests do not verify a real robot stop path.
