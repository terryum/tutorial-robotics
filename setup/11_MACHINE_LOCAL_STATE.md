# Host-Local State

The repository has shared tutorial progress while environments, paths and capabilities differ by host.

## Required local files

`$bootstrap-host` creates:

```text
.local/
├── HOST_CAPABILITIES.md
├── ENVIRONMENTS.md
├── MODELS.md
└── NETWORK.md
```

`.local/` is ignored by Git.

## Shared state

Committed under `state/`:

- tutorial completion and reports
- milestone/safety gates
- source commit pins and schemas
- deployment manifests and hashes

A tutorial done on WS2 stays done on MacBook and vice versa. This does not imply the new host already has the same environment or asset cache; reconstruct those from committed specs and pins.
