# Learner progress moved to `.local/`

Shared per-learner completion is no longer committed. Run `pal course init`, `pal course status`, and `pal course next`; the CLI stores progress in ignored `.local/progress.json` and evidence under `.local/runs/`.

Repository maintainers track implementation and publication evidence in [PUBLISHING.md](PUBLISHING.md).

User-requested progress synchronization can record a reviewed summary in a private
handoff. See [Cross-host continuation](../README.md#cross-host-continuation) for
discovery and fresh-host verification. Raw learner state remains local.
