# Host-local learner state

Read-only readiness checks do not create state. Authorized installation and execution use ignored .local/:

- progress.json: selected course scope and completed lesson records
- session.json: current or most recently finished lesson and run directory
- feedback.json: original text, lesson, received time, urgency, status and resolution evidence
- runs/: immutable baseline/comparison artifacts, execution receipts and separate review records
- bootstrap-verification.json: actual installation verification

Set PAL_LOCAL_DIR to another ignored directory for development verification. Never point a developer batch at the user's .local/ root. Each worktree owns its environment and state.

Course initialization preserves completed records. Execution writes a run; review and finish separately establish completion. Old progress records remain readable. A rerun never overwrites earlier artifacts. The metadata generator cannot update learner progress.

Only publication evidence is shared in state/PUBLISHING.md. Historical host verification reports may remain in state/ and setup/ as publication history; they do not select lessons or imply current capability. Do not commit learner completion, device details, raw data, policies or checkpoints.
