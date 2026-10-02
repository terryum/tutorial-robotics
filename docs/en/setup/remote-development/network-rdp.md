[한국어](../../../ko/setup/remote-development/network-rdp.md) | [ENGLISH](../../../en/setup/remote-development/network-rdp.md)

# Network, RDP and software choices

Prepared 2026-10-02; **reader_test_required** on every WS/client pair. Start with the [sequence](index.md), [Ubuntu server](ubuntu.md), and [local record templates](records.md). This is preparation material, not evidence of installed or working services.

## Why this stack

| Purpose | Default | Reason |
|---|---|---|
| Off-site network | Tailscale | Private device connectivity, generally without a fixed public IP or router port forwarding |
| Editing and commands | OpenSSH + VS Code Remote-SSH | Reuses keys, shells and project environments |
| Disconnected training | tmux + task checkpoints | Terminal reconnection plus separate recovery after process/reboot failure |
| Full Ubuntu desktop | Existing GNOME Remote Desktop, RDP | No RDP server subscription; prepare both login and sharing |
| Laptop client | Windows App on Mac; mstsc on Windows; Remmina on Ubuntu | RDP clients for the same WS setup |
| Isaac viewport | Version-matched NVIDIA WebRTC, when needed | Application-specific streaming, tested separately |

Personal, non-commercial research is the intended use. Before installation verify actual eligibility under the [Tailscale Personal terms](https://tailscale.com/pricing) and company network permission; a company location does not establish either. If unresolved, finish offline client/key preparation and record networking as pending. Do not enroll in a paid plan automatically.

```text
MacBook / Windows / Ubuntu laptop (clients)
  Tailscale encrypted device connection (direct or relay)
    +-- OpenSSH --> WS terminal / VS Code --> Python / GPU / tmux
    |                +-- loopback tunnels --> Jupyter / TensorBoard
    +-- RDP ------> GNOME Remote Desktop on WS1 or WS2 (server)
                       +-- Remote Login     (example TCP 3389)
                       +-- Desktop Sharing  (example TCP 3390)
                       +-- GNOME compositor / Wayland / GPU renderer
```

SSH and desktop connections are independent. Wayland is the WS display/session system, not a client app or VPN. Keep the existing session type and test it; do not switch to Xorg, install xrdp, reinstall GNOME, enable automatic login, or terminate someone else's session as a default fix. SSH success does not prove display/GPU rendering. An RDP disconnect is not necessarily a logout; test actual session behavior. tmux is not a checkpoint and does not survive reboot.

## Private network and recovery

Use the [official Tailscale installer for the actual OS](https://tailscale.com/download) and reuse an existing installation/tailnet. For a WS, the [Linux instructions](https://tailscale.com/docs/install/linux) provide a distribution-specific package route. Install only after the audit and permissions; do not add an unattended bulk installer here. On a new Linux installation, the following are individual, reviewed steps:

```bash
sudo systemctl enable --now tailscaled
sudo tailscale up
# User completes authentication personally; do not log authentication URLs/tokens.
tailscale status
tailscale ping ACTUAL_WS_TAILSCALE_NAME
tailscale netcheck
```

Do not add `--ssh`: existing OpenSSH performs key authentication. On an existing tailnet, inspect settings before changing them; do not reset existing flags. Do not configure an exit node, advertise/accept subnet routes, or bridge the company/robot network. If such routes already exist, record the conflict and resolve its scope before using this guide; do not silently reconfigure unrelated VPN use. Record boot service, key expiry and reauthentication/recovery requirements locally.

Review tailnet grants/ACLs for allowed users/devices and only the actual WS SSH/RDP ports. Do not assume membership alone means least privilege. Review host firewall rules too: [Tailscale's netfilter handling](https://tailscale.com/docs/reference/netfilter-modes) can interact with UFW, so UFW alone is not proof of restriction. Retain the existing SSH/local recovery route; never reset UFW, flush rules or open router/public RDP ports.

If UFW is already used, first inspect `sudo ufw status numbered` and the actual listeners with `sudo ss -ltnp`. The following is a **template**, not a complete policy or instruction to enable UFW. Replace every placeholder, review existing broad allows and address families, and add only necessary rules after confirming recovery:

```bash
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SSH_PORT proto tcp
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_LOGIN_PORT proto tcp
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SHARING_PORT proto tcp
```

Expected: an allowed laptop can open the intended services, an unauthorized test device cannot, and RDP is inaccessible through non-approved LAN/public paths. Test all applicable IPv4/IPv6 paths. If the policy fails, leave network acceptance pending and correct the specific grant/firewall rule from the retained session. Record exact added rule numbers/specifications and backups before edits; rollback removes only this run's rules (`sudo ufw delete RULE_NUMBER`, recheck numbering each time) and restores only this run's policy changes. Do not disable Tailscale through your sole recovery connection.

## Prepare both RDP modes on each WS

Audit locally, preserving active sessions:

```bash
cat /etc/os-release
gnome-shell --version
loginctl list-sessions
# Replace with the intended user's actual session ID:
loginctl show-session ACTUAL_SESSION_ID -p Type -p State -p Remote
dpkg-query -W gnome-remote-desktop
systemctl status gnome-remote-desktop.service --no-pager
systemctl --user status gnome-remote-desktop.service --no-pager
sudo ss -ltnp
```

Run user-service checks from the intended user's desktop/session; a missing SSH user bus is not proof of a broken desktop service. An inactive/missing service before configuration is audit evidence, not permission to install a replacement server. Prior Ubuntu 24.04 records are historical; confirm this WS's current OS/GNOME features.

In **Settings → System → Remote Desktop**, enable Desktop Sharing and Remote Control in the intended user session. Open Remote Login, unlock the panel with administrator authorization, enable it and configure its credentials separately. See [GNOME configuration](https://github.com/GNOME/gnome-remote-desktop/blob/main/docs/configuration.md), selecting the installed version when using CLI help. The [Ubuntu guide](https://ubuntu.com/desktop/docs/en/24.04/how-to/share-your-desktop-remotely/) distinguishes logged-in Desktop Sharing from Remote Login. With both enabled, its default ports are 3390 for sharing and 3389 for login. Inspect actual settings/listeners for collisions. Sharing needs Remote Control enabled for input. Save local work before a login/session-transition test; never accept a prompt to terminate an active session automatically.

| Connection | Authentication to verify | TLS trust to verify |
|---|---|---|
| Desktop Sharing | Credentials shown/configured in that mode, not assumed to be SSH credentials | That mode's configured certificate/fingerprint |
| Remote Login | RDP gateway credentials in Remote Login, then the intended Ubuntu account at the login screen | Remote Login's own certificate/fingerprint |

Keep passwords in the user's credential manager or enter interactively. Do not put them in shell arguments, screenshots, logs or Git. Record authentication *method* only. On each mode, inspect **Verify Encryption** if offered; otherwise locate the configured **public certificate** using the installed version's settings/help. Compute a SHA256 fingerprint from that public file only:

```bash
openssl x509 -in ACTUAL_PUBLIC_CERTIFICATE_PATH -noout -fingerprint -sha256
```

Compare the client certificate with the trusted WS console/authenticated report before accepting it. Match the algorithm; if the UI exposes another digest, compare like-for-like and retain SHA256 locally. Do not read/copy the TLS private key or blindly ignore a changed certificate. Separate profiles must not assume the two certificates or credentials are identical.

Expected: both listeners correspond to GNOME Remote Desktop and the intended ports, then each mode succeeds from the laptop. If GNOME, a required feature, credentials, or compatible session behavior is missing, mark that mode `PENDING`/`FAIL` with reason and continue SSH work. Do not mark GUI ready or automatically install another desktop/server. Recovery: use the retained SSH/local console, restore the prior mode settings and only this run's firewall changes; do not restart the display manager or log out active users merely to troubleshoot.

## Test from outside the company network

For **each WS and each client OS**, record date, versions and evidence using [records.md](records.md). A successful MacBook test does not verify future Windows/Ubuntu laptops.

1. Use home Wi-Fi or phone tethering. Record network context, run `tailscale ping ACTUAL_WS_TAILSCALE_NAME` and `tailscale status` after traffic; distinguish [direct, peer relay and DERP](https://tailscale.com/docs/reference/connection-types). First-packet relay alone is not the steady-state result. Confirm a fresh key-authenticated SSH connection and both RDP profiles.
2. In Desktop Sharing, find an app opened locally beforehand. Test input, Korean text, clipboard with harmless text, and resolution/scaling. Do not use private content as evidence.
3. Save work, then test Remote Login and intentional session transition with the user; record lock/reconnect and monitor-disconnected behavior for **each mode**. GNOME documents that sharing an active session can disconnect when that session locks; measure this version's behavior and record the Remote Login recovery route. A failed edge case stays a limitation, not an assumed success.
4. Run a short logging job in tmux, disconnect SSH and RDP, then reconnect and inspect new timestamps. If logout policy kills work, record it; do not relax global policy automatically.
5. Only after [reboot recovery](ubuntu.md) is prepared and reboot authorized, verify changed boot ID, SSH and Remote Login without local login, and GPU/checkpoint continuation. Desktop Sharing can require a user session; record when it becomes available. Disk unlock/local intervention prevents an unattended-reboot PASS.
6. In an installed RViz/Isaac application, use the same scene for comparisons. Record WS/client versions, display size, network path/latency, renderer/GPU, scene, input response and available frame/encode/decode metrics. Use “not measured” when a metric is unavailable. Compare GUI rendering independently of CUDA computation.

Diagnose relay path, resolution and renderer before switching products. For Isaac-only use, consult [NVIDIA WebRTC documentation matching the installed version](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html); do not copy ports or launch commands across versions. For full 3D desktops, [Sunshine/Moonlight](https://github.com/LizardByte/Sunshine) is a free comparison candidate. [RustDesk's Wayland work](https://www.rustdesk.com/blog/unattended-remote-access-wayland/) needs stable-release support verification before unattended use. Reconsider NoMachine only if measured problems remain, with current licensing checked then. No candidate is assumed faster on these machines; installing any alternative is a separate decision.
