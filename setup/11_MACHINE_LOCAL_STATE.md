# Machine-Local State

The repository has shared progress but environments and file-system paths differ by machine.

## Required local files

`$bootstrap-machine` creates:

```text
.local/
├── HOST_PROFILE.md
├── CAPABILITIES.md
├── ENVIRONMENTS.md
├── MODELS.md
└── NETWORK.md          # omit secrets
```

`.local/` must be in `.gitignore`.

## Shared state

Committed under `state/`:

- tutorial completion and reports
- phase gates
- source repository commit pins
- schema/config decisions
- deployment-bundle manifests and hashes

## Why both are needed

A model source pinned on Mac may still need to be cloned and load-tested on WS2. A tutorial marked done globally means the lesson and shared implementation are complete; it does not imply that every machine has the same environment or asset cache.

Before a machine executes a later tutorial, Codex performs local readiness checks and reconstructs missing pinned sources/environments on that machine.
