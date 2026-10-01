# MacBook remote development preparation

Verified on 2026-10-01 (Asia/Seoul), from public work base `cb6c472`.
This is a sanitized installation report. Local preparation is complete;
WS1/WS2 connection acceptance remains pending server setup. It does not
complete a lesson or authorize hardware.

## Installed and retained tools

| Component | Version / result | Action |
|---|---|---|
| macOS / architecture | 26.6.2, build 25G83 / arm64 | Inspected |
| VS Code | 1.140.0 | Retained |
| Remote-SSH | 0.128.0 | Retained |
| Python / Pylance / debugpy extensions | 2026.4.0 / 2026.4.1 / 2026.6.0 | Retained |
| Jupyter extension | 2025.9.1 | Retained |
| Codex CLI | 0.159.3; authenticated status confirmed | Retained |
| Codex IDE extension | `openai.chatgpt` 26.928.31416 | Installed |
| Codex audio dependency | `openai.codex-audio` 26.928.31416 | Installed by the IDE extension |
| OpenSSH / Git | 10.3p1 / 2.54.0 | Retained |
| Dedicated Ed25519 key | Created; private-file permissions and agent identity verified | Added through interactive Terminal; Keychain registration succeeded |
| NoMachine Enterprise Client | Package 10.1.7_1; application 10.1.7 | Installed; local GUI launch verified |

Extension registration was checked using the VS Code CLI. Remote extension,
Python interpreter/kernel and Codex operation await an actual WS connection.
Existing SSH configuration, Python environments and global Codex settings were
preserved. No placeholder host aliases were activated.

## NoMachine evidence and remaining finding

The installer came from the [official Enterprise Client download page](https://download.nomachine.com/download/?id=7&platform=mac).
Its published MD5 matched; the downloaded DMG SHA256 was
`31f6bd4924bfe77f272952c0a6fddeb4bc19dde4b0d69a60feba15e3066df358`.
Apple package signature and notarization checks passed for NoMachine S.a.r.l.

Package receipts and the installation log confirmed completion. The `nxplayer`
and `nxdock` processes were observed; both executables matched the signed
package byte for byte, and the standalone `nxplayer` signature passed.
No `nxserver` executable was found in the installed client bundle.

**The strict application-bundle resource-seal check failed**, reporting added
and missing resources after installation. Its cause was not conclusively
resolved. No re-signing or security bypass was performed. This finding remains
separate from successful installation and launch.

Automated GUI inspection timed out. The user's screenshot confirmed the
Machines screen with Add/Settings controls and no discovered computers.
That verifies local window rendering only, not remote display/input or the
bundle's resource seal. The screenshot and raw logs remain outside Git.

## Pending server-dependent acceptance

| Check | WS1 | WS2 |
|---|---|---|
| SSH_READY | PENDING: server setup and key registration | PENDING: server setup and key registration |
| REMOTE_DEV_READY | PENDING: CLIENT_TEST_PENDING | PENDING: CLIENT_TEST_PENDING |
| GPU_READY / CHECKPOINT_READY | PENDING: actual remote tests | PENDING: actual remote tests |
| GUI_READY | PENDING: remote display/input | PENDING: remote display/input |
| REBOOT_READY | PENDING: REBOOT_UNTESTED | PENDING: REBOOT_UNTESTED |

Tailscale was not installed: its need depends on the eventual LAN/VPN route.
No workstation installation, GPU operation, reboot or robot action occurred.

Next, follow the [Ubuntu guide](en/setup/remote-development/ubuntu.md)
([한국어](ko/setup/remote-development/ubuntu.md)) independently on each WS,
register only the MacBook public key, and return connection details and trusted
server host-key fingerprints. Then complete the
[MacBook connection checks](en/setup/remote-development/macbook.md)
([한국어](ko/setup/remote-development/macbook.md)).

Keys, fingerprints, actual host/user/network details, local paths and raw
receipts remain in ignored machine-local storage. Other hosts' history,
learner progress and runtime pins are unchanged.
