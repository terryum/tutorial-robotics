# Repository instructions for coding agents

## Mission and authority

Build and teach the public capability-first robotics curriculum. Read, in order:

1. `curriculum/catalog.json`
2. `agent/workflow.md`
3. the selected `docs/en/lessons/<id>.md` or Korean mirror
4. `docs/07_SAFETY.md` for any hardware-stage work
5. `.local/host.json`, `.local/capabilities.json`, and `.local/progress.json` when present

The catalog and `pal` CLI are authoritative. Machine names never authorize or order work. A workstation can start at Stage 1 without a MacBook. Learner state defaults to ignored `.local/`. An explicitly enabled learner-owned JSON helper may synchronize minimal completion hashes to that learner’s private store; raw evidence and hardware authority stay local. See `docs/PERSONAL_PROGRESS.md`; `state/PUBLISHING.md` records shared publication evidence.

## Execution contract

- Start guided learning by opening the current lesson's GitHub page in the reader's language. Reuse that tutorial tab for subsequent lessons and reruns; follow `agent/workflow.md` for tab selection and unavailable-browser handling.
- Initialize the lesson language from the conversation. Before subsequent navigation, preserve the language currently selected in the tutorial tab, including manual 한국어/ENGLISH switches; follow the language continuity rules in `agent/workflow.md`.
- Detect the host and show the smallest setup plan before applying it.
- Run one eligible lesson at a time unless the user asks for a broader batch.
- Every lesson uses committed English/Korean docs, a thin entry point, deterministic check, expected artifacts, and an explicit verification badge.
- Inspect numeric artifacts; process exit alone is not evidence.
- Treat a missing optional dependency or capability as `capability-unavailable`, never as success.
- Do not install `sudo` packages, GPU drivers, CUDA, ROS distributions, Isaac Sim, firmware, or large models automatically.
- Preserve vendor sources as pinned, read-only cache entries. Never edit or push them.

## Hardware safety

New adapters begin read-only. Require model identity, disabled/error/E-stop state, limits, acknowledgement, timeout, stale-state checks, and isolated networking. The progression is:

```text
offline replay → command sink → read-only → live shadow → torque-disabled replay → fresh run card → one explicitly approved action
```

Never enable torque/control, publish motion, update firmware, increase limits, or bypass watchdog/collision/E-stop without a new explicit per-run approval. Do not store serials, private IPs, calibration, credentials, raw datasets, bags, runs, or checkpoints in Git.

## Public/private boundary

FR3, Unitree G1, Wuji Hand 2 Beta 2, Sharpa Wave, ALOHA, Flexiv Enlight, generic interfaces, and public-source adapters belong here. FRIDAY-specific source, models, configuration, motion, learning data, hardware integration, and organization data stay in the private sibling overlay and must never enter public history.

## Git continuity

Inspect status before edits and preserve unrelated work. Use the personal `terryum` account and `terry.t.um@gmail.com`. Do not auto-push. Before repository creation, visibility changes, releases, or other consequential GitHub mutations, run `gh context` and verify `terryum`. Public source repositories use Apache-2.0 unless a vendor license requires a stricter boundary.

## Credential protection — all hosts

This applies equally to WS1, WS2, MacBook, Windows, Ubuntu and any future host,
and to public and private repositories. Never commit SSH private **or public**
keys, authorized_keys, known_hosts, passwords, API/GitHub/Tailscale tokens,
login/authorization links, credential stores, or remote-access configuration
containing secrets. Public keys are not cryptographic secrets, but are still
excluded from this project's Git history. Use placeholders in examples.
Keep real connection records under ignored `.local/` or outside the repository;
never force-add them. Share only the needed public key through an approved
channel; never transfer a private key. Each operator uses their own identity.

On every clone/worktree, run `git config --local core.hooksPath .githooks`
(after preserving any existing custom hooks) and
`python3 scripts/check_credentials.py --tracked`. The pre-commit hook scans
staged bytes, including force-added files. CI repeats the complete-index scan.
Never disable the guard to publish a credential. Detection is a backstop, not
proof that arbitrary text contains no secrets: inspect staged diffs before
committing and do not print credential values during audits. If a credential
was published, revoke/rotate it first and coordinate history cleanup; deleting
only the latest file does not remove it from history.
