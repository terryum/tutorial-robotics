[한국어](../../../ko/setup/remote-development/macbook.md) | [ENGLISH](../../../en/setup/remote-development/macbook.md)

# MacBook remote development client

Read the [sequence, prompts and acceptance criteria](index.md) first. This guide changes only the MacBook; use the [Ubuntu guide](ubuntu.md) on each WS. Preserve existing MacBook Core development and do not add server CUDA or training datasets.

## 1. Inspect and plan the changes

Inspect `sw_vers`, `uname -m` and `command -v code codex brew ssh git`. Check VS Code extensions, Tailscale/Windows App/NoMachine installations, and only the relevant SSH blocks, Include directives and Host * settings. Do not dump authentication files or the full environment.

Reuse apps, keys, VPN and settings. Show missing tools, installation locations and commands first. An execution request for this guide includes these user settings and incremental tools; obtain OS permissions through normal approval mechanisms. Do not bulk-upgrade apps or packages.

Keep authorized setup records under `.local/remote-development/macbook/`. Back up settings before merging changes and restrict records/backups to the owner. Reuse server address/user/port/project paths from existing configuration or that WS's `CLIENT-CONNECTION.md`. If absent, finish independent work, then request only the missing values together.

## 2. Apps and extensions

1. If VS Code stable is absent, use the existing Homebrew's `brew install --cask visual-studio-code` or the [official macOS installation](https://code.visualstudio.com/docs/setup/mac). Check the `code` PATH. Do not install a broad toolchain just because Homebrew is absent.
2. Retain working Git/OpenSSH. Ask the user to complete Apple Command Line Tools UI or administrator authentication only when needed.
3. Preserve existing Codex installation/login; if absent, follow the [official installation and remote authentication instructions](index.md#when-codex-is-not-installed-yet).
4. Compare with `code --list-extensions` and install only missing extensions.

```bash
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-toolsai.jupyter
```

Install Python/Jupyter workspace extensions **on the SSH target WS** after connecting. The Codex IDE extension is optional; use the distribution linked by the [official guide](https://developers.openai.com/codex/ide/). Do not force `remote.extensionKind` without testing execution location. The default route is Codex CLI in the remote terminal.

Use Tailscale as the default off-site route after checking Personal plan eligibility and company permission in the [network guide](network-rdp.md). Reuse existing installations; if missing, install one [official macOS app](https://tailscale.com/docs/install/mac) and let the user sign in. Preserve the existing recovery route and add no exit node or subnet routing.

For RDP, install Microsoft's **Windows App** from its official Mac App Store link in the [Microsoft instructions](https://learn.microsoft.com/windows-app/get-started-connect-devices-desktops-apps?pivots=remote-pc). Reuse an existing installation and verify its supported macOS version. Add no receiving server to the MacBook. Keep the previously installed NoMachine client, but leave it unused in the default setup; the [historical report](../../../MACBOOK_REMOTE_DEVELOPMENT_STATUS_2026-10-01.md) remains valid for its date.

## 3. SSH keys and aliases

If no reusable key exists, generate a dedicated Ed25519 key without overwriting an existing file; an example name is `~/.ssh/id_ed25519_remote_robotics`. The user enters the passphrase locally and uses ssh-agent/Keychain. Never copy the private key to a WS. Keep `.ssh` at 700 and private keys/config at 600.

Send only the public key to the WS. Preserve existing `authorized_keys` entries and test with a separate connection. Compare the first connection's SHA256 host-key fingerprint with a WS report obtained from the local console or another authenticated route. `ssh-keyscan` alone does not establish trust; do not use `StrictHostKeyChecking=no`.

This is a **template requiring all values before activation**. If an existing alias points to a different machine, choose a new alias and use it throughout subsequent commands. Merge with awareness of Include and Host * first-value semantics.

```sshconfig
Host ws1
  HostName ACTUAL_WS1_ADDRESS
  User ACTUAL_WS1_USER
  Port ACTUAL_WS1_SSH_PORT
  IdentityFile ACTUAL_PRIVATE_KEY_PATH
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
  ForwardAgent no

Host ws2
  HostName ACTUAL_WS2_ADDRESS
  User ACTUAL_WS2_USER
  Port ACTUAL_WS2_SSH_PORT
  IdentityFile ACTUAL_PRIVATE_KEY_PATH
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
  ForwardAgent no
```

Inspect effective settings locally with `ssh -G ws1` and `ssh -G ws2`. Never activate remaining placeholders. After connecting, verify `hostname`, `id -un`, `pwd` and `nvidia-smi`. An absent GPU and a failed SSH connection are different results.

## 4. VS Code, Python and Codex

Choose the alias in `Remote-SSH: Connect to Host...` and open **the WS report's project path**. VS Code Server installs in the remote user's account; a separate WS desktop app is unnecessary. [Remote-SSH source, checked 2026-10-01](https://code.visualstudio.com/docs/remote/ssh).

Check the remote indicator, terminal `hostname`, `codex --version` and `codex login status`. Verify Codex can read the remote project and work on a temporary file under the WS record directory. Submitting a cloud task is not a WS GPU execution test.

Choose **the WS environment for the particular task** as the Python interpreter and Notebook kernel: the existing Python 3.12 `.venv` for Core, or the separate registered GPU environment for GPU work. Do not select Core `.venv` or MacBook Python for every task. If needed, add `ipykernel` only to the chosen environment using its existing lock workflow.

## 5. Logs, tunnels and persistent work

On the WS, run Jupyter with token authentication, `127.0.0.1` and `--no-browser`; bind TensorBoard to `127.0.0.1` too. Use the installed project environment and keep tokens out of reports. Use VS Code Ports or these SSH tunnels.

```bash
# MacBook example: WS1 services actually listening on 8888/6006
ssh -N -L 127.0.0.1:8888:127.0.0.1:8888 -L 127.0.0.1:6006:127.0.0.1:6006 ws1
# Use different local ports to view both workstations concurrently
ssh -N -L 127.0.0.1:8889:127.0.0.1:8888 -L 127.0.0.1:6007:127.0.0.1:6006 ws2
```

If ports conflict, choose and record other available local ports. Do not expose services publicly. Verify remote result existence and hashes before transferring selected small files. Full dataset/checkpoint replication and `rsync --delete` are not defaults.

On the WS use `tmux new -As robotics-ws1` or `robotics-ws2`. Detach with `Ctrl-b`, then `d`; reattach with the same command. Test a short synthetic logging job across SSH disconnection and MacBook sleep. There is no need to disable MacBook sleep globally. **A WS reboot ends tmux and training**, requiring separate checkpoint continuation.

## 6. GUI, reconnection and closeout

In Windows App, use **Add PC** to create `WS1 Login`, `WS1 Sharing`, `WS2 Login` and `WS2 Sharing`. Set PC name to `ACTUAL_WS_TAILSCALE_ADDRESS:ACTUAL_MODE_PORT`; defaults with both modes enabled are Login 3389 and Sharing 3390, but copy actual values from the WS report. Use the two modes' credentials separately and verify their certificates through the [common RDP procedure](network-rdp.md). Store no passwords in the connection report. Keep profiles local.

Run all [off-site, lock/disconnect, monitor and performance tests](network-rdp.md), recording each WS independently. Both RDP modes must pass for GUI readiness; a desktop alone does not prove Isaac GPU rendering. If WS details are absent, finish apps/public-key preparation and leave only connection-dependent checks pending. After each WS setup, return here to complete its MacBook tests.

Before a WS reboot test, follow the [Ubuntu recovery procedure](ubuntu.md) and stay within explicit reboot approval. From MacBook verify a new SSH/VS Code connection without local login, GPU tests and Remote Login; record Desktop Sharing session availability separately. If no reboot occurred, record `REBOOT_UNTESTED`.

Write per-WS [acceptance results](index.md#records-and-acceptance), retained/installed app versions and change/backup locations in `RESULT.md`. Record missing addresses, authentication, local actions and exact next commands in `RESUME.md`. Do not promote untested connections to complete.
