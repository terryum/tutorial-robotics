# MacBook compatibility redirect

MacBook is one supported Stage 1 host, not a prerequisite or a phase gate. Use [Portable Development](PORTABLE_DEVELOPMENT.md), then let `pal course next --json` select lessons from actual capabilities.

```bash
pal host detect --json
pal setup plan --stage core --out .local/setup-plan.json --json
pal course init --through core --json
pal course next --json
```
