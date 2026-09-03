# Migration from v3 to v4

## Removed assumptions

- no `MacBook foundation` prerequisite before WS2
- no host-specific shared status
- no machine-exclusive development profile
- no one-way handoff from Mac to WS2

## New model

- both MacBook and WS2 use `DEVELOPMENT`
- tutorials declare `requires` capabilities
- WS2 is the full superset development host
- MacBook continues any compatible pending branch
- Git sync is bidirectional
- real hardware requires a separate `ROBOT_RUNTIME` mode

## Existing v3 progress

When migrating an already-started repository, preserve every `done` tutorial and its evidence. Rename old gates as follows:

```text
MACBOOK_FOUNDATION_COMPLETE   → CORE_CURRICULUM_READY
WS2_SIM_TRAIN_COMPLETE          → GPU_CURRICULUM_READY
WS2_DEPLOYMENT_BUNDLE_READY     → CANDIDATE_DEPLOYMENT_BUNDLE_READY
```

Do not copy `.local/` or virtual environments into v4.
