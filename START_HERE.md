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
