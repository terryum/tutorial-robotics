[한국어](../../../ko/setup/remote-development/index.md) | [ENGLISH](../../../en/setup/remote-development/index.md)

# Remote robotics development: MacBook, WS1 and WS2

Written and official sources checked: 2026-10-01. **These are incremental setup instructions, not an installation report.** On each machine, inspect the actual state and install only what is needed.

## Roles and sequence

| Target | Guide | Role and boundary |
|---|---|---|
| MacBook | [MacBook setup](macbook.md) | SSH/VS Code client and result review; preserve existing local Core development |
| WS1 Ubuntu | [Ubuntu setup](ubuntu.md), role `ws1` | Independent GPU development/training in DEVELOPMENT; stop training for ROBOT_RUNTIME |
| WS2 Ubuntu | [Ubuntu setup](ubuntu.md), role `ws2` | Independent GPU development/training in DEVELOPMENT; stop training for ROBOT_RUNTIME |

Machine names establish neither authority nor readiness. Each WS can be prepared independently of the MacBook or the other WS. Distributed training, shared storage and physical robot connections are outside this guide.

1. Inspect existing settings and installation history. The MacBook can prepare apps and a public key before server details are available.
2. Follow the Ubuntu procedure on each WS and create a local `CLIENT-CONNECTION.md`. A server without SSH needs a local terminal or an already working remote desktop for initial setup.
3. Transfer the connection details securely to the MacBook and verify SSH → VS Code → remote Python/Codex → GPU tests separately for each WS.
4. Test GUI access and post-reboot access separately. Prepare recovery and resume records before a necessary reboot.

Code launched in the WS terminal uses the WS GPU. This does not run Codex's own inference on the RTX GPU. Files on the MacBook are not automatically available to remote Codex.

## Copyable prompts for each machine

Start Codex in that machine's `tutorial-robotics` checkout. First confirm these documentation changes are present there. Unpublished local changes cannot be received through `git pull`: securely transfer only the documentation bundle, or synchronize after a separately requested publication. Do not copy `.local/`, authentication files or virtual environments.

### MacBook

```text
Read docs/en/setup/remote-development/index.md and macbook.md, then actually add, configure and verify the missing remote robotics development tools on this MacBook. Preserve AGENTS.md and existing settings, and show the necessary changes first. If WS details are missing, finish app and SSH public-key preparation first. Record results under .local/remote-development/macbook/ and distinguish unverified items for WS1 and WS2. Do not claim lesson completion or installation on a remote machine.
```

### WS1 Ubuntu

```text
Read docs/en/setup/remote-development/index.md and ubuntu.md. Audit this machine as logical role ws1 for DEVELOPMENT, then add and verify the missing remote robotics development tools. If ROBOT_RUNTIME work is active, defer conflicting changes without stopping it or switching modes automatically. Reuse existing ROS/GPU/Isaac environments and locks. Record results under .local/remote-development/ws1/. Prepare impact, recovery and resume records before any reboot and stay within its approval. Do not connect to or control physical robots.
```

### WS2 Ubuntu

```text
Read docs/en/setup/remote-development/index.md and ubuntu.md. Audit this machine as logical role ws2 for DEVELOPMENT, then add and verify the missing remote robotics development tools. If ROBOT_RUNTIME work is active, defer conflicting changes without stopping it or switching modes automatically. Inspect this machine's GPU, driver, disk and environments instead of copying WS1 settings. Record results under .local/remote-development/ws2/. Prepare impact, recovery and resume records before any reboot and stay within its approval. Do not connect to or control physical robots.
```

## When Codex is not installed yet

Inspect and reuse an existing installation with `command -v codex` and `codex --version`. Only if absent, a person performs the [official installation](https://developers.openai.com/codex/cli/) in a local terminal or authenticated SSH session. The macOS/Linux standalone example is below. Do not duplicate npm/Homebrew installations or use `sudo codex`.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
# Apply the installer's PATH instructions or open a new terminal, then:
codex --version
codex login status
```

For remote login, use `codex login --device-auth` when allowed by the account/workspace and complete authentication personally in the MacBook browser. Otherwise use the [official SSH callback forwarding flow](https://developers.openai.com/codex/auth/): for example, connect from the MacBook with `ssh -L 127.0.0.1:1455:localhost:1455 ws1` and run `codex login` in that session. Check for port conflicts first. Never print or copy tokens/auth caches between machines.

Preserve models, MCP, skills, accounts, permission policies and existing user/managed settings. Setup does not require disabling the sandbox or changing global model/effort settings.

## Records and acceptance

Paths are relative to each machine's checkout. After setup is authorized, create `.local/remote-development/<host>/` with owner-only access; `<host>` is `macbook`, `ws1` or `ws2`. Read-only audits do not create files. On rerun, read the existing records and retain logs in separate per-run subdirectories.

- `RESULT.md`: actual host/OS, retained/installed/changed/deferred items, exact versions and environment paths, statuses below and evidence logs.
- `CLIENT-CONNECTION.md`: WS user, address, port, public host-key SHA256 fingerprint, absolute project/Python paths. Keep actual connection details out of Git.
- `RESUME.md`: pending reasons, next commands, user actions, backup/recovery paths and the actual guide path to reopen.
- `gpu-smoke-result.json` and logs: chosen environment/GPU, FP32/BF16, optimizer changes and checkpoint continuation. On MacBook, record only observed remote evidence.

| Item | Evidence required for PASS |
|---|---|
| SSH_READY | Active server plus actual MacBook key-authenticated connection |
| REMOTE_DEV_READY | Remote folder, WS Python and WS Codex CLI verified |
| GPU_READY | Finite loss/gradients and optimizer update on the actual GPU |
| CHECKPOINT_READY | A new process loads a checkpoint and advances training steps |
| GUI_READY | Actual client display/input, including license and login conditions |
| REBOOT_READY | Changed boot ID, reconnect without local login, GPU retest |

Use `PASS / FAIL / PENDING / NOT_APPLICABLE`. Server-only checks are `PENDING: CLIENT_TEST_PENDING`; an untested reboot is `PENDING: REBOOT_UNTESTED`. An absent GPU or intentionally omitted GUI is `NOT_APPLICABLE` with its reason; missing required authentication, license or address is `PENDING: NEEDS_INPUT`. One WS cannot supply evidence for the other.

These results establish environment readiness only. They do not complete lessons, verify Isaac execution/policy performance or authorize hardware. Do not overwrite historical installation/host ledgers with unmeasured success or change learner progress.

## Source integration

The supplied 2026-10-01 `00-START-HERE.md` maps to this index; `01-MACBOOK-SETUP.md` maps to the MacBook guide; `02-WS1-UBUNTU-SETUP.md` and `03-WS2-UBUNTU-SETUP.md` map to the common Ubuntu procedure with separate roles. OCR competition paths, data and dedicated packages are excluded. The originals remain unchanged.

This repository owns generic setup. Robot-specific private overlays link here from their own documentation; private implementation and machine details never enter the public guide.

If a private overlay pins an earlier public commit exactly, separate current documentation from the runtime checkout. Read this guide in a browser or a separate documentation checkout; run private code against its pinned checkout. Receiving newer main does not justify bypassing pin checks or changing locks. Adopting a new runtime base requires separate compatibility validation.
