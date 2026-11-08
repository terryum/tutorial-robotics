# Start here

Choose a scope, not a machine sequence.

```bash
pal host detect --json
pal setup plan --profile core --out .local/setup-plan.json --json
pal setup verify --profile core --json
pal course runnable --without-hardware --json
pal course init --through core --json
pal course next --json
```

Read the [English](docs/en/index.md) or [한국어](docs/ko/index.md) page for the returned lesson. Run its check, execute it headlessly, and inspect `summary.json`, `trace.csv`, and `lesson-report.md`.

For Simulation, initialize `--through sim` on Ubuntu and install only the capabilities needed by the selected track. For Hardware, select one or more `--robot` values, complete the common runtime lessons, and stop at read-only preflight until a fresh motion approval exists.

For the WS2 development handoff, say **“튜토리얼 업데이트 해줘”**. Follow the [WS2 update runbook](setup/WS2_TUTORIAL_UPDATE.md) for repository sync, real Isaac/PhysX verification, fixes and publication. This is separate from ordinary learner progress and hardware operation. An existing clone must first receive these instructions through its normal repository update.
