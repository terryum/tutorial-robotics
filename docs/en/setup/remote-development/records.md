[한국어](../../../ko/setup/remote-development/records.md) | [ENGLISH](../../../en/setup/remote-development/records.md)

# Local setup and connection records

Copy these templates only into ignored `.local/remote-development/<host>/` during authorized setup. Use `macbook`, `ws1`, `ws2`, `windows-laptop` or `ubuntu-laptop`; retain prior runs. On macOS/Linux, create with `umask 077` and `mkdir -p .local/remote-development/ACTUAL_HOST`, then restrict the directory to 700; on Windows restrict its ACL to the user. Never commit filled records. Store no passwords, private keys, authentication URLs or tokens here. Actual addresses, usernames, certificate fingerprints and environment paths stay local.

Use `PASS / FAIL / PENDING / NOT_APPLICABLE` with evidence and a reason. Missing required GUI functionality is pending/failure, not an optional omission. `GUI_READY` follows `RUSTDESK_READY`: screen, input, Korean, clipboard and resolution must pass for that client/WS. `UNATTENDED_GUI_READY` separately requires lock reconnect and post-reboot access without local login/intervention. Unselected RDP modes are `NOT_APPLICABLE: NOT_SELECTED`; selected modes need client evidence. Preserve historical records unchanged. Unmeasured reboot or rendering stays pending. Read [test scenarios](network-rdp.md) and [GPU/recovery checks](ubuntu.md).

## CLIENT-CONNECTION.md

```text
Host role / actual host / OS / client OS / date: UNVERIFIED
Tailnet device name / address / key expiry / recovery contact: UNVERIFIED
Company network permission / Personal eligibility: UNVERIFIED
SSH alias / user / port / public host-key SHA256: UNVERIFIED
Project absolute path / task Python path / environment manager: UNVERIFIED
RustDesk client/WS version / build channel / device ID: UNVERIFIED
RustDesk server type (public/self-hosted) / ID server / relay address: UNVERIFIED
RustDesk public server-key verification route / trusted contact / date: UNVERIFIED
RustDesk authentication method (no password) / service / boot state: UNVERIFIED
RustDesk Wayland/Xorg / active session / connection entries WS1/WS2: UNVERIFIED
Optional RDP Remote Login: address / port / auth method / public TLS SHA256: UNVERIFIED
Optional RDP Desktop Sharing: address / port / auth method / public TLS SHA256: UNVERIFIED
Certificate comparison algorithm / trusted verification route / date: UNVERIFIED
Optional RDP profile names (WS1/WS2, selected modes): UNVERIFIED
Local tunnel ports / actual remote service ports: UNVERIFIED
Approved device/user policy / host firewall scope: UNVERIFIED
```

## RESULT.md

```text
Run date / host / client / WS / guide revision: UNVERIFIED
Retained / installed / changed / deferred (versions and reasons): UNVERIFIED
Backup paths / evidence log paths: UNVERIFIED
SSH_READY: PENDING: CLIENT_TEST_PENDING
REMOTE_DEV_READY: PENDING: CLIENT_TEST_PENDING
GPU_READY: PENDING: UNTESTED
CHECKPOINT_READY: PENDING: UNTESTED
EXTERNAL_NETWORK_READY: PENDING: UNTESTED
  Tailscale context / direct, peer relay or DERP / latency / policy tests: UNVERIFIED
RDP_REMOTE_LOGIN_READY: NOT_APPLICABLE: NOT_SELECTED
RDP_DESKTOP_SHARING_READY: NOT_APPLICABLE: NOT_SELECTED
RUSTDESK_READY: PENDING: CLIENT_TEST_PENDING
GUI_READY: PENDING: CLIENT_TEST_PENDING
UNATTENDED_GUI_READY: PENDING: LOCK_AND_REBOOT_UNTESTED
  Existing local app / input / Korean / clipboard / resolution: UNVERIFIED
  RustDesk direct/relay path / lock / disconnect / session transition / monitor absent: UNVERIFIED
TMUX_DISCONNECT_READY: PENDING: UNTESTED
REBOOT_READY: PENDING: REBOOT_UNTESTED
  Old/new boot ID / SSH / RustDesk without local login: UNVERIFIED
  Disk unlock or other local intervention / optional RDP availability: UNVERIFIED
GUI_RENDERING_READY: PENDING: UNTESTED
  App/version / same scene / renderer and GPU / resolution: UNVERIFIED
  Network path / response / FPS / encode-decode metrics: NOT_MEASURED
Per-item expected / observed / evidence / limitation / next action: UNVERIFIED
```

## RESUME.md

```text
Current state / completed steps: UNVERIFIED
Pending item / cause / required user input: UNVERIFIED
Exact next command or UI action / host / guide path: UNVERIFIED
Recovery route tested / local assistance / backups: UNVERIFIED
Exact rollback for this run's config, firewall rules and profiles: UNVERIFIED
Reboot impact / approval scope / checkpoints / next GPU command: UNVERIFIED
Next laptop-to-WS verification after each server setup: UNVERIFIED
```
