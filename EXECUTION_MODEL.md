# Execution model

Catalog order, prerequisites, actual platform/dependencies/models and local learner progress select the next lesson. Machine names do not authorize or order work.

- Core: 25 lessons on Python 3.12/macOS arm64/Linux x86_64. Real MuJoCo dynamics/rendering and lightweight NumPy learning require no ROS.
- Simulation: matching Ubuntu/ROS/GPU/Isaac stacks for 14 lessons. The portable sim-deploy-01 candidate lesson consumes the actual core-fr3-08 policy.
- Offline: hw-common-01 loads that candidate and runs deterministic inference into a command sink on macOS or Linux.
- Physical: eight device lessons remain scaffolded and reader_test_required. Per-run hardware approval is mandatory.

The learner flow is selection → preflight → baseline → artifact validation → explanation/comparison → accumulated feedback fixes/reverification → review → finish. Stop after one learner lesson unless the user requested a broader batch.

Host detection and readiness verification are read-only. Actual installation/execution state belongs under ignored .local/. PAL_LOCAL_DIR separates development runs. course init preserves progress, lesson run never completes a lesson, and finish rejects corrupt, failed, unreviewed or unresolved runs.

Publication badges are independent of learner completion. A passed optimizer smoke does not verify policy performance, and a candidate does not authorize hardware. Vendor source/model hashes are checked; missing or changed dependencies are explicit gaps.

No automatic system package, driver, CUDA, ROS distribution, Isaac, firmware or large-model installation. Keep physical adapters read-only until their individual safety gates and fresh per-run approval are satisfied.
