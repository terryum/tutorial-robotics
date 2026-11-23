<!-- pal:language:start -->
<p align="right">
  <a href="../../ko/concepts/vla.md" lang="ko">한국어</a> | <a href="vla.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Vision-language-action: a protocol, a model and a runtime

## Three words name several separate contracts

A VLA policy conditions action on visual information, language and robot state. That description leaves many practical questions: which camera, which pixel preprocessing, which state order, which action units, what time horizon, which model weights and how stale observations are rejected. A network response containing numbers is not enough to answer them.

[The portable protocol lesson](../lessons/core-vla-01.md) is a mock. [Local SmolVLA fine-tuning](../lessons/sim-vla-01.md) uses a prepared pinned checkpoint and dataset on CUDA. [Optional remote inference](../lessons/sim-vla-02.md) exercises a configured transport. These are different claims and require different evidence. None of the three paths authorizes a physical command.

Think of a policy as

$$
A=\pi_\theta(I,s,\ell),\qquad A\in\mathbb R^{H\times d_a}.
$$

$I$ is image input, $s$ is state, $\ell$ is a language instruction, $H$ is an action horizon and $d_a$ is action dimension. These symbols describe an interface family; the actual model may preprocess images as `(batch, channels, height, width)` and expose a single selected action rather than an entire chunk. Shape is not semantics: seven outputs may mean angles, deltas, velocities or normalized controls. Units and named action order must be recorded separately.

## What the portable mock can teach

[learning.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/learning.py) serializes a version-1 request with `instruction`, a seven-value zero `observation`, fixture-image digest, `timestamp_s` and `timeout_s=0.1`. It deserializes the request and returns one action row, marks `mock=True` and `command_sink=True`, and labels units rad. This verifies a JSON round trip and a bounded response. It does not load a vision encoder, understand language or execute a learned VLA policy. A timeout value in this local fixture is a schema field, not proof of enforced network timeout.

Worked shape calculation, **not a model result**: one row with seven actions has shape (1, 7). Multiplying seven zeros by 0.8 leaves zeros, so changing only the mock's `variant` is expected to be invariant.

```python
import json
import numpy as np
request = {"observation": [0.0] * 7}
decoded = json.loads(json.dumps(request))
actions = np.asarray([[0.8 * x for x in decoded["observation"]]])
assert actions.shape == (1, 7)
assert np.array_equal(actions, np.zeros((1, 7)))
```

Read `experiment.json` → `payload` → `request` and `response`, along with `schema_roundtrip`, `bounded_actions` and `sink_only` in `checks`. A zero plot here is correct fixture behavior, not policy failure or success.

## What real fine-tuning and transport add

[vla.py](https://github.com/terryum/tutorial-robotics/blob/main/src/pai_lab/lessons/vla.py) requires the pinned LeRobot checkout, an existing local pretrained checkpoint and a dataset with `meta/info.json`. It sets offline model-loading flags, constructs dataset-specific pre/postprocessors, performs AdamW updates and saves policy plus processors. The batch size is 2; action timestamps depend on dataset FPS and configured chunk size. Do not replace these with a universal camera size or robot action dimension.

Its loss trace, `parameter_delta`, saved `policy/`, `training-observation.png` and `server-response.json` establish bounded training/reload/loopback inference behavior. The code explicitly records `performance_verified=False`: a few gradient updates and finite inference do not evaluate independent robot tasks. Pixels shown in a training observation also depend on preprocessing; they are not automatically raw calibrated camera measurements.

For remote inference, the endpoint must use HTTPS or loopback HTTP. The adapter hashes a prepared request, applies a 5 s transport timeout, reads a bounded response, requires a 2D action array with configured action dimension, and checks finite values and the configured action limit. It records `model_identity` if supplied. Receiving an identity string is not cryptographic attestation of deployed weights. The measured scalar is round-trip time in seconds, while plotted values are actions in configured units: do not label the action axis as latency.

## Compare one variable at the right layer

In the mock, keep request and seed fixed and change only `variant`; zero actions remain zero. For prepared local training, a learning-rate multiplier comparison holds checkpoint, dataset, preprocessing, seed and update budget fixed. Inspect finite loss and parameter change without claiming improved task performance. A remote response is server-defined; if a local multiplier is unused, invariant output is expected. Record network and server variability instead of inventing a deterministic improvement.

The [public verification report](../../verification/reader-experience.md) leaves external VLA checks separate from portable mock verification. Missing weights, data or CUDA are capabilities to prepare explicitly, never an excuse to relabel mock output as real inference.

## Check your understanding

1. Does JSON schema success demonstrate language understanding? No; the portable fixture never runs a VLA model.
2. Why save processors with the policy? Scaling, feature order and image preprocessing determine what the weights mean.
3. Can finite remote actions be sent directly to hardware? No. [Deployment and hardware](deployment-hardware.md) requires the full reviewed contract and fresh execution authority.

The [NVIDIA ecosystem guide](../nvidia-ecosystem.md) extends the data-to-policy questions to GR00T. Model installation, dataset conversion, finite inference, fine-tuning and independently evaluated robot performance remain separate milestones; SmolVLA or mock evidence cannot stand in for GR00T execution.
