# Learner experience verification

Verified locally on macOS arm64 from source `0004b7d830eb7bd0758aff9865d3d0216bb5ab1c` after integrating WS1 main `aa86de5`. Runtime: Python 3.12.13, MuJoCo 3.12.0, NumPy 2.5.2. The implementation digest and measured baseline/comparison values are in [the evidence record](reader-experience.json).

All 25 Core lessons, the generated FR3 candidate and the offline inference/sink lesson passed actual baseline execution, the documented one-variable experiment, artifact validation, review and finish in a separate development session. That session does not become learner progress. The candidate uses the trained policy bytes, processor contract and deterministic test vectors; zero physical commands were emitted.

88 regression tests passed, including interrupted execution, legacy progress preservation, concurrent feedback, malformed/blank artifacts, damaged comparison evidence, GAE termination semantics, PPO parameter update/reload and complete multi-object OBJ conversion. Ruff, strict mypy (51 source files), repository/release/public-boundary validators and strict MkDocs passed. Generator tests preserve authored text, entry points and tests, and verify both language navigation sequences. GitHub CI has been updated but was not run remotely in this task.

A fresh temporary checkout with Python 3.12 and uv absent from PATH completed the shell bootstrap, using local uv and managed Python 3.12.14. Core installation, T00 baseline/comparison/check/review/finish, bootstrap reapplication and course reinitialization passed without deleting completion. This separate bootstrap test used the integrated `ea1d5d7` source; later changes concern experiment rendering and comparison validation, covered by the regression suite and final 27-lesson run.

## Measured portable experiments

Baseline seed 7, 64 samples, variant 1. Each comparison changes the single documented CLI input. Learning is a short optimizer/reload test: it does not establish task performance or safe deployment.

| Lesson | Metric | Baseline | Comparison | Unit |
|---|---|---:|---:|---|
| core-00 | available_capability_count | 5 | 5 | count |
| core-01 | energy_drift | 6.510348e-13 | 3.260592e-11 | joule |
| core-02 | valid_source_ratio | 1 | 1 | ratio |
| core-03 | valid_model_ratio | 1 | 1 | ratio |
| core-04 | rendered_joint_count | 7 | 7 | count |
| core-fr3-01 | joint_count | 7 | 7 | count |
| core-fr3-02 | tracking_error | 0.3376263 | 0.2131057 | rad |
| core-fr3-03 | tracking_error | 0.002480475 | 0.001059313 | rad |
| core-fr3-04 | ik_residual | 1.387779e-16 | 1.387779e-16 | meter |
| core-fr3-05 | pose_error | 0.005604573 | 0.003203821 | meter |
| core-fr3-06 | mean_normal_force | 5.961403 | 5.961403 | newton |
| core-rl-01 | objective_gain | 0.1280098 | 0.1278821 | reward |
| core-fr3-07 | terminal_distance | 0.00774507 | 0.007837086 | meter |
| core-fr3-08 | reward_gain | 0.01863665 | 0.01813922 | reward |
| core-enlight-01 | frame_count | 9 | 9 | count |
| core-enlight-02 | max_fk_error | 6.760705e-16 | 5.673898e-16 | meter |
| core-wuji-01 | pose_count | 3 | 3 | count |
| core-wuji-02 | mean_contact_force | 5.849245 | 12.62195 | newton |
| core-dexterity-01 | shared_joint_ratio | 0.9090909 | 0.9090909 | ratio |
| core-data-01 | transition_count | 512 | 512 | count |
| core-dexterity-02 | retarget_error | 0.00557916 | 0.0146751 | meter |
| core-g1-01 | loop_error | 0 | 0 | rad |
| core-il-01 | loss_reduction | 0.1864599 | 0.1885216 | loss |
| core-aloha-01 | action_dimension | 14 | 14 | count |
| core-vla-01 | schema_fields | 10 | 10 | count |
| sim-deploy-01 | test_vector_error | 0 | 0 | normalized |
| hw-common-01 | emitted_command_count | 0 | 0 | count |

## Image review and interpretation

Reviewed examples are linked from the corresponding bilingual lessons. FR3 tracking plots distinguish residual PD error from gravity compensation. PPO reward curves are measured and need not improve monotonically. Wuji contact and Sharpa retargeting show actual geometry. G1 is prescribed kinematic playback, not learned locomotion. ALOHA contains real simulated actuator state and an ACT-shaped contract, without ACT training.

Visual inspection found that MuJoCo read only part of the multi-object Enlight visual OBJ exports. The adapter now retains every vertex and face in a single derived local object, with a regression test. The vendor checkout remains unchanged. Enlight frame agreement verifies transform conversion; it does not calibrate physical inertia or contact.

## Remaining external verification

The other 14 software lessons remain `reader_test_required`: ROS/DDS/rosbag, MJLab GPU training/evaluation, local/remote VLA and Isaac. Their real adapters have no synthetic success fallback. Follow [the WS1 handoff](ws1-handoff.md) at this same source revision and return measured evidence before changing badges. Existing WS1 installation evidence is retained and does not validate these new experiments.

The ROS Enlight adapter teaches simulated DDS state/service contracts, not the production Flexiv driver. The Isaac adapter targets the documented 5.1 API and needs compatibility testing on the installed WS1 version. A vendor Wuji training task does not establish Beta 2 hardware equivalence. All eight device lessons remain scaffolded and unverified; no hardware operation was attempted.

## Figure provenance

Figures are rendered from pinned public assets and measured local traces, with no personal run files or policy checkpoints committed. FR3 and Sharpa: Apache-2.0; Enlight: Apache-2.0; Wuji description: MIT; G1 and ALOHA: BSD-3-Clause. Exact source revisions, license files and model bytes are locked in `assets/sources.json` and `assets/model-lock.json` at the source commit above.
