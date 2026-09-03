# Repository Bootstrap

Codex creates the source layout only after the host audit.

## Requirements

- initialize Git only when this directory is not already in a repository
- preserve existing user files
- create a Python package using `src/` layout
- create separate environment instructions rather than one global requirements file
- create `.gitignore` for `.local/`, environments, outputs, checkpoints, large datasets, and external repositories
- add a simple CLI entry point named `pal`
- configure pytest, Ruff, and optional mypy

## Machine-local contract

Create `.local/` through `$bootstrap-host`; never commit host profile, local paths, device network details, or secrets. Shared tutorial progress remains under `state/`.

## Initial CLI contract

```bash
pal doctor
pal tutorial list
pal tutorial status
pal model list
pal model inspect <model-id>
pal model view <model-id>
```

Commands may initially return informative “not yet implemented” messages, but `pal doctor` and tutorial status must work in T00.
