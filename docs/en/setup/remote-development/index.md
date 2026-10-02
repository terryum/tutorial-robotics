[한국어](../../../ko/setup/remote-development/index.md) | [ENGLISH](../../../en/setup/remote-development/index.md)

# Remote robotics development: MacBook, WS1 and WS2

Updated: 2026-10-02; new network/RDP sources checked on this date. **These are incremental setup instructions, not an installation report.** On each machine, inspect the actual state and install only what is needed.

The default is **Tailscale + OpenSSH/VS Code + GNOME RDP**, with tmux and task checkpoints. This update delivers published preparation documents only; app installation, WS configuration and actual access tests remain unverified. Next execution order: **MacBook → WS1 → WS2**, returning to MacBook to verify each WS after its setup. Preserve the installed NoMachine client without using it by default.

- [Common network, RDP, software choices and performance tests](network-rdp.md)
- [Windows / Ubuntu laptop clients and their execution prompts](laptops.md)
- [Local connection, result and recovery templates](records.md)

## Roles and sequence

| Target | Guide | Role and boundary |
|---|---|---|
| MacBook | [MacBook setup](macbook.md) | SSH/VS Code client and result review; preserve existing local Core development |
| Windows / Ubuntu laptop | [Client setup](laptops.md) | Future clients; validate each independently |
| WS1 Ubuntu | [Ubuntu setup](ubuntu.md), role `ws1` | Independent GPU development/training in DEVELOPMENT; stop training for ROBOT_RUNTIME |
| WS2 Ubuntu | [Ubuntu setup](ubuntu.md), role `ws2` | Independent GPU development/training in DEVELOPMENT; stop training for ROBOT_RUNTIME |

Machine names establish neither authority nor readiness. Each WS can be prepared independently of the MacBook or the other WS. Distributed training, shared storage and physical robot connections are outside this guide.

1. Inspect existing settings and installation history. The MacBook can prepare apps and a public key before server details are available.
2. Follow the Ubuntu procedure on each WS and create a local `CLIENT-CONNECTION.md`. A server without SSH needs a local terminal or an already working remote desktop for initial setup.
3. Transfer the connection details securely to the MacBook and verify SSH → VS Code → remote Python/Codex → GPU tests separately for each WS.
4. Test GUI access and post-reboot access separately. Prepare recovery and resume records before a necessary reboot.

Code launched in the WS terminal uses the WS GPU. This does not run Codex's own inference on the RTX GPU. Files on the MacBook are not automatically available to remote Codex.

## Copyable prompts for each machine

Start the next session in that machine's `tutorial-robotics` checkout and confirm it contains this revision. Inspect local changes before syncing; use `git pull --ff-only` only on a clean matching branch, and preserve divergence for deliberate integration. Never copy `.local/`, credentials or environments. For a private overlay with a pinned runtime base, read the published guide or a separate documentation checkout without changing the runtime pin.

### MacBook

```text
Read docs/en/setup/remote-development/index.md, macbook.md, network-rdp.md and records.md, then actually add, configure and verify the missing remote robotics development tools on this MacBook. Preserve AGENTS.md and existing settings, and show the necessary changes first. Prepare Tailscale and Windows App after checking Personal plan eligibility and company permission. Retain the installed NoMachine client unused, and add no laptop server. Prepare separate Remote Login/Desktop Sharing profiles per WS. If WS details are missing, finish app and SSH public-key preparation first. Record results under .local/remote-development/macbook/ and distinguish unverified items for WS1 and WS2. Do not claim lesson completion or installation on a remote machine.
```

### WS1 Ubuntu

```text
Read docs/en/setup/remote-development/index.md, ubuntu.md, network-rdp.md and records.md. Audit this machine as logical role ws1 for DEVELOPMENT, then add and verify the missing remote robotics development tools. If ROBOT_RUNTIME work is active, defer conflicting changes without stopping it or switching modes automatically. Reuse existing ROS/GPU/Isaac environments and locks. Check company permission and Personal eligibility, configure OpenSSH over Tailscale and both GNOME RDP modes, and retain existing SSH recovery. Do not add exit nodes/subnet routes, terminate sessions, enable automatic login or install an alternative desktop/server. Verify both modes from MacBook on an external network after setup; leave absent evidence pending. Record results under .local/remote-development/ws1/. Prepare impact, recovery and resume records before any reboot and stay within its approval. Do not connect to or control physical robots.
```

### WS2 Ubuntu

```text
Read docs/en/setup/remote-development/index.md, ubuntu.md, network-rdp.md and records.md. Audit this machine as logical role ws2 for DEVELOPMENT, then add and verify the missing remote robotics development tools. If ROBOT_RUNTIME work is active, defer conflicting changes without stopping it or switching modes automatically. Inspect this machine's GPU, driver, disk and environments instead of copying WS1 settings. Check company permission and Personal eligibility, configure OpenSSH over Tailscale and both GNOME RDP modes, and retain existing SSH recovery. Do not add exit nodes/subnet routes, terminate sessions, enable automatic login or install an alternative desktop/server. Verify both modes from MacBook on an external network after setup; leave absent evidence pending. Record results under .local/remote-development/ws2/. Prepare impact, recovery and resume records before any reboot and stay within its approval. Do not connect to or control physical robots.
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

Paths are relative to each machine's checkout. After setup is authorized, create `.local/remote-development/<host>/` with owner-only access; `<host>` is `macbook`, `ws1`, `ws2`, `windows-laptop` or `ubuntu-laptop`. Read-only audits do not create files. On rerun, read the existing records and retain logs in separate per-run subdirectories.

- `RESULT.md`: actual host/OS, retained/installed/changed/deferred items, exact versions and environment paths, statuses below and evidence logs.
- `CLIENT-CONNECTION.md`: WS user, address, port, public host-key SHA256 fingerprint, absolute project/Python paths, Tailscale identity, both RDP ports/authentication methods and each public TLS fingerprint. Use the [templates](records.md); keep actual connection details local and never store passwords/private keys/tokens.
- `RESUME.md`: pending reasons, next commands, user actions, backup/recovery paths and the actual guide path to reopen.
- `gpu-smoke-result.json` and logs: chosen environment/GPU, FP32/BF16, optimizer changes and checkpoint continuation. On MacBook, record only observed remote evidence.

| Item | Evidence required for PASS |
|---|---|
| SSH_READY | Active server plus actual key-authenticated connection from the recorded client |
| REMOTE_DEV_READY | Remote folder, WS Python and WS Codex CLI verified |
| GPU_READY | Finite loss/gradients and optimizer update on the actual GPU |
| CHECKPOINT_READY | A new process loads a checkpoint and advances training steps |
| EXTERNAL_NETWORK_READY | Off-site SSH/RDP and direct/relay path, allowed/denied access checks |
| RDP_REMOTE_LOGIN_READY | Actual client login, correct mode authentication and TLS verification |
| RDP_DESKTOP_SHARING_READY | Existing local app, display/input, Korean, clipboard and resolution |
| GUI_READY | Both RDP modes PASS for the same client/WS; lock/disconnect/monitor behavior recorded |
| TMUX_DISCONNECT_READY | Logging continues after SSH and RDP disconnect |
| GUI_RENDERING_READY | Installed application's actual scene/renderer/GPU and measured performance |
| REBOOT_READY | Changed boot ID, SSH and Remote Login without local login, GPU/checkpoint retest; record local unlock limitations |

Use `PASS / FAIL / PENDING / NOT_APPLICABLE`. Server-only checks are `PENDING: CLIENT_TEST_PENDING`; an untested reboot is `PENDING: REBOOT_UNTESTED`. An absent GPU is `NOT_APPLICABLE` with its reason. Missing GNOME or a required RDP feature leaves GUI pending/failed with the cause; missing authentication or address is `PENDING: NEEDS_INPUT`. One WS or client OS cannot supply evidence for another. Record all session-edge tests and performance using the [common scenarios](network-rdp.md).

These results establish environment readiness only. They do not complete lessons, verify Isaac execution/policy performance or authorize hardware. Do not overwrite historical installation/host ledgers with unmeasured success or change learner progress.

## Source integration

The supplied 2026-10-01 `00-START-HERE.md` maps to this index; `01-MACBOOK-SETUP.md` maps to the MacBook guide; `02-WS1-UBUNTU-SETUP.md` and `03-WS2-UBUNTU-SETUP.md` map to the common Ubuntu procedure with separate roles. OCR competition paths, data and dedicated packages are excluded. The originals remain unchanged.

This repository owns generic setup. Robot-specific private overlays link here from their own documentation; private implementation and machine details never enter the public guide.

If a private overlay pins an earlier public commit exactly, separate current documentation from the runtime checkout. Read this guide in a browser or a separate documentation checkout; run private code against its pinned checkout. Receiving newer main does not justify bypassing pin checks or changing locks. Adopting a new runtime base requires separate compatibility validation.
