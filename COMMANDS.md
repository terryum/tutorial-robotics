# `pal` command reference

```text
pal host detect [--json]
pal setup plan --stage core|sim|hardware [--robot ROBOT] --out PATH [--json]
pal setup apply PATH [--json]
pal setup verify --stage STAGE [--robot ROBOT] [--json]

pal course init --through core|sim|hardware [--robot ROBOT] [--include-electives] [--json]
pal course list [--json]
pal course status [--json]
pal course next [--json]

pal lesson run ID [--headless] [--seed N] [--samples N] [--output-dir PATH] [--json]
pal lesson check ID [--json]
pal assets fetch BUNDLE [--json]
pal hardware preflight fr3|wuji|enlight --read-only [--snapshot PATH] [--json]
pal sources check [--json]
```

Exit code `0` means the requested check or run succeeded. `1` means an invalid repository/lesson/source contract. `2` means prerequisite or capability unavailable. `3` means hardware preflight failed closed.

`pal doctor` and `pal tutorial list/status/next` remain deprecated aliases for v1.x. Legacy lesson IDs such as `T00` also resolve for v1.x and print a warning.
