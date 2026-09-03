# Runbook — Git Sync Across MacBook, WS2 and WS1

## 1. What Git carries

- source, tests and tutorial entry points
- Markdown instructions and lesson reports
- configs, schemas and lock/spec files
- small deterministic test vectors and small plots
- model/dataset/checkpoint manifests and SHA-256
- shared tutorial progress and gates

## 2. What Git does not carry

- `.venv`, Conda/Pixi environment
- CUDA/Isaac/model caches
- `.local/HOST_CAPABILITIES.md`
- secrets, robot credentials and private network details
- large raw datasets, checkpoints and video collections
- re-clonable pinned vendor trees

Use Git LFS/DVC/NAS/object storage for large artifacts and keep their URI/version/hash in committed manifests.

## 3. Before work on either development host

```bash
git status
git pull --rebase
```

Do not pull/rebase over uncommitted generated work. One active writer per branch is the default.

## 4. After one tutorial

```bash
git status
git diff --check
git add <focused files>
git commit -m "tutorial(Txx): complete <topic>"
git push
```

Codex may prepare these commands but must not push without explicit permission.

## 5. On a new host

- pull the same branch/commit
- run `$bootstrap-host`
- recreate local environments from committed specs
- re-clone vendor assets at pinned commit
- verify small deterministic vectors
- continue from shared progress

## 6. Portability verification

A tutorial already done globally may be rerun on another host. Store outputs under a new host-specific run ID and append verification evidence; do not rewrite the canonical run or set the status back to in-progress.
