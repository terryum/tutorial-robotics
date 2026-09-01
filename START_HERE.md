# Start Here

## Machine sequence

Use one Git repository and one shared progress history across all machines:

```text
MacBook (`MACBOOK_FOUNDATION`)
  -> WS2 (`WS2_SIM_TRAIN`)
  -> WS1 (`WS1_ROBOT_RUNTIME`)
```

1. On the MacBook, run `uv sync --group dev` and `uv run pal doctor`.
2. Register machine-local facts under ignored `.local/`.
3. Run the first eligible tutorial shown by `uv run pal tutorial list`.
4. Commit code, reports, output manifests, and shared progress after each
   completed tutorial.
5. Transfer the same commit to WS2; do not copy individual Markdown files.
6. Promote a verified candidate bundle before moving to WS1.

Public users need only this repository and its public dependencies. Authorized
private-platform work uses `../tutorial-robotics-private`, which validates and
extends this checkout without changing the public workflow.

Run one tutorial at a time unless the user explicitly requests more.
