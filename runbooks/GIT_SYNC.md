# Git synchronization across hosts

Git carries source, bilingual teaching, tests, pinned manifests and reviewed publication evidence. Environments, vendor checkouts, learner progress, feedback, runs, checkpoints and private robot configuration stay local. A new host starts its own learner state.

Before integration, inspect `git status --short --branch`, fetch the remote, and inspect the incoming diff. Preserve unfinished changes in focused commits or an isolated worktree before merging. Never replace another host's report when resolving a conflict; merge historical ledger rows by stable host ID.

After a lesson, `pal lesson finish` records local completion only after artifact validation, comparison review and feedback resolution. No automatic commit or push follows a lesson. Development changes can be committed when requested; push and merge to shared branches require authorization.

For cross-host verification, check out the same source commit, run `sh bootstrap.sh --plan`, prepare only the required capabilities, and use a separate `PAL_LOCAL_DIR`. Follow [the WS1 handoff](../setup/WS1_HANDOFF.md). Keep old learner records readable, but rerun stale code or invalid evidence before selecting dependent lessons.

`state/HOST_STATUS.md` is historical installation evidence. `state/PUBLISHING.md` records reviewed publication badges; neither is learner progress or current hardware authorization.
