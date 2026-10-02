[한국어](../../../ko/setup/remote-development/rustdesk.md) | [ENGLISH](../../../en/setup/remote-development/rustdesk.md)

# RustDesk first: screen control

Checked 2026-10-02. The user confirms colleagues use RustDesk on WS1 and WS2; versions, server configuration and unattended access are **UNVERIFIED**. This publishes preparation instructions only. Each client/WS pair remains **reader_test_required**. Start with the [sequence and execution prompts](index.md).

Use existing RustDesk for screen/input, Tailscale + OpenSSH/VS Code for development, and WS tmux + checkpoints for persistence. Initially reuse colleagues’ working RustDesk connection route. Do not automatically switch RustDesk to direct IP over Tailscale or build a new ID/relay server. Tailscale success does not verify RustDesk routing.

## Audit each WS before changing anything

With the intended user, inspect the app's version/build channel, device ID, public versus self-hosted ID/relay server, authentication method, and current sessions. Record only the required fields in local [CLIENT-CONNECTION.md](records.md); do not dump config files or capture passwords. Check service and boot state read-only:

```bash
command -v rustdesk
rustdesk --version
dpkg-query -W rustdesk
systemctl is-active rustdesk.service
systemctl is-enabled rustdesk.service
loginctl list-sessions
loginctl show-session ACTUAL_SESSION_ID -p Type -p State -p Remote
```

Replace the session placeholder. A missing binary/package/unit may indicate another installation method; inspect the app and actual launcher before concluding RustDesk is absent. Determine Wayland/Xorg for the intended desktop and login screen separately. Preserve colleagues’ connection settings, passwords, server keys and active services. Do not reinstall, restart or upgrade a working service for this setup.

For self-hosted access, obtain the existing ID/relay addresses and verify the **public** server key through the administrator or an authenticated existing configuration; record that verification route locally. Never request/copy the private server key. Follow [official client configuration](https://rustdesk.com/docs/en/self-host/client-configuration/) for the installed version. Preserve existing authentication; enter secrets interactively or through the user's credential manager. If details or permission are missing, use `PENDING: NEEDS_INPUT` while continuing independent SSH preparation.

## Prepare outgoing laptop clients

Reuse existing apps and authentication first. If absent, use the [official client downloads](https://rustdesk.com/docs/en/client/) and the build for the actual OS/architecture; record the installed version. Installation is a later execution step, not a result of this document update.

| Client | Installation route when missing | Scope |
|---|---|---|
| MacBook | [macOS guide](https://rustdesk.com/docs/en/client/mac/): matching `.dmg`, move app into Applications | Grant only permissions needed for outgoing input; Input Monitoring may be needed. Local screen capture permissions are not a reason to enable incoming control. |
| Windows laptop | [Windows guide](https://rustdesk.com/docs/en/client/windows/): matching official client build | Use as an outgoing client; no unattended receiving service or password setup on the laptop. |
| Ubuntu laptop | [Linux guide](https://rustdesk.com/docs/en/client/linux/): matching `.deb`, review `sudo apt install ./ACTUAL_RUSTDESK_PACKAGE.deb` | Inspect package/service effects; keep incoming access disabled. Do not enable a boot receiving service just to connect. |

Check the installed version's incoming-access controls and leave laptop receiving access disabled; installing a remote-control app is not permission to configure a laptop server. Avoid silent deployment options or broad permission resets. Preserve unrelated existing configuration; if client-only operation conflicts with it, record and resolve the conflict before changes.

Create local WS1 and WS2 connection entries using each verified device ID and the existing server route. If the two WS use different server configurations, identify the correct configuration before each connection; do not overwrite a shared profile silently. Test existing RustDesk access during the MacBook step when details are available, even before WS SSH setup. Do not copy a colleague's full configuration/authentication cache.

## Wayland: regular releases versus preview

The [regular Linux documentation](https://rustdesk.com/docs/en/client/linux/) describes experimental Wayland support since 1.2.0 and an X11 requirement for login-screen access. The [2026-08-14 announcement](https://www.rustdesk.com/blog/unattended-remote-access-wayland/) separately describes a preview for x86_64 Debian/Ubuntu, including unattended login-screen access after reboot and multiple monitors. It says standard-release integration is future work. Recheck the installed release's support at execution time; do not infer that colleagues use this preview or that regular Wayland access proves unattended access.

Preview installation, switching to Xorg, automatic login and forced session termination are not default remedies. Preserve the current session; record local consent/login requirements and continue SSH work. If a required feature is missing, consider [optional GNOME RDP](network-rdp.md) for that feature, with its own evidence.

## Acceptance and recovery

Run the [external-network, lock, monitor, tmux, reboot and same-scene performance tests](network-rdp.md) separately per WS/client. `RUSTDESK_READY=PASS` requires actual screen/input/Korean/clipboard/resolution success; default `GUI_READY` follows it. `UNATTENDED_GUI_READY=PASS` additionally requires both lock reconnect and access after an authorized reboot without local login or intervention. A normal desktop session, an active service or a colleague's success is insufficient evidence.

Keep actual IDs, addresses, public-key verification routes and authentication methods only in ignored `.local/`; never record passwords, private keys or tokens. Keep prior runs unchanged. Use retained SSH/local assistance for recovery; undo only this run's new client entries/settings. Do not disrupt colleagues’ service or weaken authentication. Use [records](records.md) for pending causes, evidence and the exact next action.
