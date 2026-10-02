[한국어](../../../ko/setup/remote-development/laptops.md) | [ENGLISH](../../../en/setup/remote-development/laptops.md)

# Windows and Ubuntu laptop clients

Use the [common network/RDP procedure](network-rdp.md) and [acceptance records](records.md). These clients use the same WS servers; each client/WS pair remains **reader_test_required**. MacBook instructions are [separate](macbook.md). Do not enable an incoming desktop server on a laptop.

## Windows laptop

1. Inspect existing VS Code, Remote-SSH/Python/Jupyter extensions, Git, `ssh -V`, keys and Tailscale first. Preserve authentication and settings. If OpenSSH Client is missing, use Windows Settings → Optional features → OpenSSH Client; do not install OpenSSH Server. Use [VS Code for Windows](https://code.visualstudio.com/docs/setup/windows) and [Tailscale for Windows](https://tailscale.com/docs/install/windows) only when absent and permitted.
2. In PowerShell, `Get-Command ssh, code, tailscale, rustdesk` checks command availability (a missing PATH entry may still mean an app is installed). Reuse `%USERPROFILE%\.ssh\config` and an existing suitable key. If there is no suitable key and the filename is unused, run:

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\id_ed25519_remote_robotics"
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_remote_robotics.pub"
```

The user enters the passphrase interactively. Transfer only the `.pub` contents to each WS and preserve authorized keys. Keep private-key/config access restricted to the user with Windows ACLs; do not copy a MacBook private key. Merge the [SSH alias template](macbook.md) with Windows paths such as `~/.ssh/id_ed25519_remote_robotics`, then verify `ssh -G ws1`, `ssh ws1` and `ws2`, including trusted host-key fingerprints.

3. Prepare [RustDesk](rustdesk.md), reuse installation/authentication and create separate WS1/WS2 entries using the existing ID/relay route. Add no incoming laptop service. Windows App/mstsc/Remmina are only [optional RDP supplements](network-rdp.md).
4. Connect VS Code Remote-SSH to the actual WS project folder; install workspace extensions on the WS and select that task's existing WS Python/kernel. A Windows desktop/WSL interpreter is not the remote GPU environment. Retain existing Codex authentication; verify its remote CLI from the WS terminal using the [MacBook guide's shared development checks](macbook.md). WSL is not required for this client setup.

## Ubuntu laptop

1. Inspect `cat /etc/os-release`, `command -v ssh code rustdesk tailscale`, keys and extensions. Reuse existing apps. If needed, review and install only the missing packages from `openssh-client` with `sudo apt install PACKAGE_NAMES`; replace the placeholder, do not run a bulk upgrade. Use [VS Code's Linux installation](https://code.visualstudio.com/docs/setup/linux) and [Tailscale's Linux installation](https://tailscale.com/docs/install/linux) when absent, then follow the common networking procedure. Do not install `openssh-server`, GNOME Remote Desktop or xrdp on this client just to connect.
2. Reuse `~/.ssh/config` and a suitable local key. Only when the filename is unused and no suitable key exists:

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_remote_robotics
cat ~/.ssh/id_ed25519_remote_robotics.pub
```

Enter the passphrase locally. Keep `.ssh` at 700 and private key/config at 600, transfer only the public key, and follow [alias merging and host-key checks](macbook.md).

3. Prepare [RustDesk](rustdesk.md), reuse installation/authentication and create separate WS1/WS2 entries using the existing ID/relay route. Add no incoming laptop service. Windows App/mstsc/Remmina are only [optional RDP supplements](network-rdp.md).
4. Use the same Remote-SSH folder, remote extensions and WS Python/kernel checks as Windows. Record missing features separately from SSH success.

## Both clients: verify and recover

Use the [loopback tunnel commands](macbook.md) on either OS: local 8888/6006 for WS1 and 8889/6007 for WS2, with actual remote ports. Keep Jupyter authentication. Run tmux **on the WS**, and inspect continued logging after client sleep and SSH/RustDesk disconnection; reboot recovery requires checkpoints.

Expected: off-site SSH, remote development, RustDesk screen and separate unattended tests and the [session/reboot/performance scenarios](network-rdp.md) have separate evidence for each WS. Until tested, write `PENDING: CLIENT_TEST_PENDING` under `.local/remote-development/windows-laptop/` or `ubuntu-laptop/`. If server details are missing, complete apps/key preparation and defer only connection tests. Add a local suffix for multiple laptops to avoid overwriting records.

Recovery: keep the old SSH connection while testing a merged config; restore only this run's backed-up blocks if needed. Correct only this run’s new RustDesk entry after trusted verification; preserve shared server settings. For selected RDP, verify the certificate before correcting a new profile/pin. If remote settings need repair, use [WS recovery](ubuntu.md); do not weaken authentication to make a client connect.

## Copyable execution prompts

### Windows laptop

```text
Read docs/en/setup/remote-development/index.md, laptops.md, rustdesk.md, network-rdp.md and records.md. Prepare this Windows laptop as a Tailscale, OpenSSH/VS Code Remote-SSH and RustDesk client. Preserve existing apps, keys and authentication; generate this device's key only if needed and transfer only its public key. Check company permission and Personal plan eligibility before network setup. Reuse the existing RustDesk route and create an entry per WS without enabling a laptop server. Preserve colleagues’ settings/passwords/server keys; do not switch to Tailscale direct IP or deploy a relay. RDP is optional. Record screen and unattended readiness separately. If WS information is missing, finish independent preparation and leave connections pending. Verify each WS from an external network and record only local results under .local/remote-development/windows-laptop/. Do not install WS software, change lesson progress or claim MacBook evidence as this client's success.
```

### Ubuntu laptop

```text
Read docs/en/setup/remote-development/index.md, laptops.md, rustdesk.md, network-rdp.md and records.md. Prepare this Ubuntu laptop as a Tailscale, OpenSSH/VS Code Remote-SSH and RustDesk client. Preserve existing apps, keys and authentication; generate this device's key only if needed and transfer only its public key. Check company permission and Personal plan eligibility before network setup. Reuse the existing RustDesk route and create an entry per WS without enabling a laptop server. Preserve colleagues’ settings/passwords/server keys; do not switch to Tailscale direct IP or deploy a relay. RDP is optional. Record screen and unattended readiness separately. If WS information is missing, finish independent preparation and leave connections pending. Verify each WS from an external network and record only local results under .local/remote-development/ubuntu-laptop/. Do not install WS software, change lesson progress or claim another client's success.
```
