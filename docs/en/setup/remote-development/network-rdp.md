[한국어](../../../ko/setup/remote-development/network-rdp.md) | [ENGLISH](../../../en/setup/remote-development/network-rdp.md)

# Common network and optional RDP

Prepared 2026-10-02; **reader_test_required** on every WS/client pair. Start with the [sequence](index.md), [Ubuntu server](ubuntu.md), and [local record templates](records.md). This is preparation material, not evidence of installed or working services.

## Why this stack

| Purpose | Default | Reason |
|---|---|---|
| Off-site network | Tailscale | Private device connectivity, generally without a fixed public IP or router port forwarding |
| Editing and commands | OpenSSH + VS Code Remote-SSH | Reuses keys, shells and project environments |
| Disconnected training | tmux + task checkpoints | Terminal reconnection plus separate recovery after process/reboot failure |
| Full Ubuntu desktop | Existing RustDesk | Reuse colleagues’ connection route; [audit first](rustdesk.md) |
| Laptop client | RustDesk on Mac/Windows/Ubuntu | Windows App / mstsc / Remmina only for optional RDP |
| Isaac viewport | Version-matched NVIDIA WebRTC, when needed | Application-specific streaming, tested separately |

Personal, non-commercial research is the intended use. Before installation verify actual eligibility under the [Tailscale Personal terms](https://tailscale.com/pricing) and company network permission; a company location does not establish either. If unresolved, finish offline client/key preparation and record networking as pending. Do not enroll in a paid plan automatically.

```text
MacBook / Windows / Ubuntu laptop
  RustDesk --> existing ID/relay route --> WS1 / WS2 screen + input
  Tailscale --> OpenSSH --> VS Code / Python / GPU / tmux
                         +--> loopback tunnels: Jupyter / TensorBoard
            --> optional GNOME RDP (only selected modes)
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

Review tailnet grants/ACLs for allowed users/devices and only the actual WS SSH ports and only selected RDP ports. Do not assume membership alone means least privilege. Review host firewall rules too: [Tailscale's netfilter handling](https://tailscale.com/docs/reference/netfilter-modes) can interact with UFW, so UFW alone is not proof of restriction. Retain the existing SSH/local recovery route; never reset UFW, flush rules or open router/public RDP ports.

If UFW is already used, first inspect `sudo ufw status numbered` and the actual listeners with `sudo ss -ltnp`. The following is a **template**, not a complete policy or instruction to enable UFW. Replace every placeholder, review existing broad allows and address families, and add only necessary rules after confirming recovery:

```bash
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SSH_PORT proto tcp
# Optional RDP only / 선택한 RDP만:
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_LOGIN_PORT proto tcp
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SHARING_PORT proto tcp
```

Expected: an allowed laptop can open the intended services, an unauthorized test device cannot, and RDP is inaccessible through non-approved LAN/public paths. Test all applicable IPv4/IPv6 paths. If the policy fails, leave network acceptance pending and correct the specific grant/firewall rule from the retained session. Record exact added rule numbers/specifications and backups before edits; rollback removes only this run's rules (`sudo ufw delete RULE_NUMBER`, recheck numbering each time) and restores only this run's policy changes. Do not disable Tailscale through your sole recovery connection.

## Optional GNOME RDP modes

Use RDP only when a required feature is missing in RustDesk. It is excluded from default installation and completion. Select Remote Login (login/session creation) and/or Desktop Sharing (existing logged-in desktop) according to the unmet need. Unselected modes remain `NOT_APPLICABLE: NOT_SELECTED`; do not enable both automatically. The instructions below apply only to selected modes.

Clients: Mac uses [Windows App from Microsoft’s official Mac App Store link](https://learn.microsoft.com/windows-app/get-started-connect-devices-desktops-apps?pivots=remote-pc); Windows uses built-in `mstsc`; Ubuntu uses [Remmina](https://ubuntu.com/desktop/docs/en/24.04/how-to/access-a-remote-desktop/) (`remmina remmina-plugin-rdp` only if missing). Create a local WS/mode profile with `ACTUAL_WS_ADDRESS:ACTUAL_MODE_PORT`, verify its certificate and enter matching credentials interactively. Do not enable laptop receiving services.

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

In **Settings → System → Remote Desktop**, if Desktop Sharing was selected, enable it and Remote Control in the intended user session. If Remote Login was selected, unlock that panel with administrator authorization, enable it and configure its credentials separately. See [GNOME configuration](https://github.com/GNOME/gnome-remote-desktop/blob/main/docs/configuration.md), selecting the installed version when using CLI help. The [Ubuntu guide](https://ubuntu.com/desktop/docs/en/24.04/how-to/share-your-desktop-remotely/) distinguishes logged-in Desktop Sharing from Remote Login. With both enabled, its default ports are 3390 for sharing and 3389 for login. Inspect actual settings/listeners for collisions. Sharing needs Remote Control enabled for input. Save local work before a login/session-transition test; never accept a prompt to terminate an active session automatically.

| Connection | Authentication to verify | TLS trust to verify |
|---|---|---|
| Desktop Sharing | Credentials shown/configured in that mode, not assumed to be SSH credentials | That mode's configured certificate/fingerprint |
| Remote Login | RDP gateway credentials in Remote Login, then the intended Ubuntu account at the login screen | Remote Login's own certificate/fingerprint |

Keep passwords in the user's credential manager or enter interactively. Do not put them in shell arguments, screenshots, logs or Git. Record authentication *method* only. On each mode, inspect **Verify Encryption** if offered; otherwise locate the configured **public certificate** using the installed version's settings/help. Compute a SHA256 fingerprint from that public file only:

```bash
openssl x509 -in ACTUAL_PUBLIC_CERTIFICATE_PATH -noout -fingerprint -sha256
```

Compare the client certificate with the trusted WS console/authenticated report before accepting it. Match the algorithm; if the UI exposes another digest, compare like-for-like and retain SHA256 locally. Do not read/copy the TLS private key or blindly ignore a changed certificate. Separate profiles must not assume the two certificates or credentials are identical.

Expected: selected listeners correspond to GNOME Remote Desktop and the intended ports, then each selected mode succeeds from the laptop. If GNOME, a required feature, credentials, or compatible session behavior is missing, mark that mode `PENDING`/`FAIL` with reason and continue SSH work. An RDP result does not replace RustDesk acceptance; do not automatically install another desktop/server. Recovery: use the retained SSH/local console, restore the prior mode settings and only this run's firewall changes; do not restart the display manager or log out active users merely to troubleshoot.

## Test from outside the company network

For **each WS and each client OS**, record date, versions and evidence using [records.md](records.md). A successful MacBook test does not verify future Windows/Ubuntu laptops.

1. Use home Wi-Fi or tethering. Check fresh SSH over Tailscale and RustDesk over its existing route separately. Record Tailscale [direct/peer relay/DERP](https://tailscale.com/docs/reference/connection-types) after traffic using `tailscale ping ACTUAL_WS_TAILSCALE_NAME` and `tailscale status`. Record RustDesk direct/relay from its own connection information; do not infer it from Tailscale. Test allowed/denied access through approved test devices, not colleagues’ accounts.
2. In RustDesk, identify a harmless app opened on the WS; test screen, input, Korean, harmless clipboard text and resolution/scaling. This client/WS evidence establishes `RUSTDESK_READY` and default `GUI_READY`.
3. Save work and coordinate with active users. Test lock/reconnect, disconnection and monitor-absent behavior independently. Record local consent/session requirements; a working logged-in desktop does not prove unattended access. Do not force logout to test.
4. Run a short logging job in WS tmux, disconnect SSH and RustDesk, then reconnect and inspect new timestamps. Include client sleep. Record logout-policy failures without weakening global policy.
5. Only after [recovery preparation and authorized reboot](ubuntu.md), verify changed boot ID, SSH and RustDesk without local login, GPU and checkpoint continuation. `UNATTENDED_GUI_READY` requires both lock reconnect and reboot access without local intervention; disk unlock or local consent prevents PASS. Untested cases stay pending. Test selected RDP modes separately.
6. In installed RViz/Isaac, compare the same scene on each WS at the same resolution. Record WS/client/app versions, display size, network path/latency, renderer/GPU, input response, FPS and available encode/decode metrics. Mark unavailable metrics “not measured”; GUI rendering is separate from CUDA computation.

Diagnose RustDesk path, resolution and renderer first. Optional RDP can address a specific missing feature; for Isaac-only streaming consult [version-matched NVIDIA WebRTC documentation](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html). Do not assume an alternative is faster without the same-scene measurements. Preserve NoMachine installation history; reconsider it only for measured needs with licensing checked then.
