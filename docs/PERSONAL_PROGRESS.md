# Optional personal progress bridge

`pal course summary --json` reports the entire current catalog, including electives.
Existing `course list/status/next` JSON stays unchanged for unregistered learners.
A fresh learner starts at zero; these commands perform no Git/network operations.

A learner can explicitly enable an external, trusted helper in ignored
`.local/personal-progress.json`:

```json
{
  "enabled": true,
  "registered_root": "/absolute/path/to/this/checkout",
  "helper": ["/absolute/path/to/python", "/absolute/path/to/helper.py"]
}
```

The helper is an argument list executed without a shell. It receives a single
JSON object on stdin (`schema_version: 1`, `operation: "sync"`, `root`, `scope`)
and returns a version-1 JSON summary containing `lessons` and `sync` on stdout.
Lesson rows contain canonical `id`, `scope`, `completed`, `needs_review`,
`current_version_verified`, `completed_on`, and optional `verified_digests`.
The helper owns destination validation, durable queueing, evidence verification,
catalog freshness, conflict resolution and account-specific configuration.
The public package does not install or import a private robot SDK.

The CLI calls the helper before course queries and learning, and after durable
run/review/feedback/finish updates. A helper failure leaves local completion
intact and reports pending sync using its last cached summary. The next query
rescans durable local completion, so a failed notification loses no completion.
No completion is produced by `run` alone; `finish` still verifies artifacts,
review, feedback and readiness. Helpers must independently validate imports.

Shared completion is historical learning evidence. Current platform, packages,
models, implementation status and hardware approvals remain separate gates.
A remote completion has no `run_dir`. Lessons that consume actual data/policies
require locally validated source artifacts. Code changes can require review
without deleting completion. The full summary explains catalog growth.

Any `PAL_LOCAL_DIR`, `PAL_PRIVATE_LOCAL_DIR` or `PAL_PUBLIC_LOCAL_DIR` override
disables the personal bridge, even when its value happens to match a registered
path. Use those overrides for tests, development and installation checks.
Remove `enabled` or set it to false to return to local-only progress. The helper
and cache remain ignored local files; never commit personal configuration here.
