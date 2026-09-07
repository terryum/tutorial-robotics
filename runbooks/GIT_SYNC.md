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
git log -1 --oneline
```

Do not pull/rebase over uncommitted generated work. One active writer per branch is the default.
After pulling, read `state/HOST_STATUS.md` and `state/PROGRESS.md`. Treat
`WS2_WINDOWS` and `WS2_UBUNTU` as separate rows even when they are layers of the
same physical workstation. Preserve reports written by other hosts.

## 4. After one tutorial

```bash
git status
git diff --check
git add <focused files> state/PROGRESS.md state/HOST_STATUS.md
git commit -m "tutorial(Txx): complete <topic>"
git push
git status --short --branch
```

The current host row in `state/HOST_STATUS.md` is mandatory whenever the push
contains a tutorial result, installation/environment change, portability
verification, blocker, handoff, mode change, lock, source pin, or candidate
bundle. Update `state/PROGRESS.md` only when shared tutorial completion actually
changed. Installation-only results must not mark a tutorial done.

Codex may prepare these commands but must not push without explicit permission.
If the user explicitly asks to complete and push the scoped work, that request
authorizes the corresponding push.

## 5. On a new host

- pull the same branch/commit
- run `$bootstrap-host`
- recreate local environments from committed specs
- re-clone vendor assets at pinned commit
- verify small deterministic vectors
- continue from shared progress
- update this host's row in `state/HOST_STATUS.md` when bootstrap or
  reconstruction evidence will be committed

## 6. Portability verification

A tutorial already done globally may be rerun on another host. Store outputs under a new host-specific run ID and append verification evidence; do not rewrite the canonical run or set the status back to in-progress.

## 7. Conflict rule

When two hosts edited `state/HOST_STATUS.md`, merge by stable host ID and keep the
newest report for each row. Never replace the entire file with one machine's
copy. Do not put hostnames, usernames, IP addresses, serial numbers, credentials,
or private robot details in the public ledger.
