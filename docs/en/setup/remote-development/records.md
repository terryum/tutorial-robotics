[한국어](../../../ko/setup/remote-development/records.md) | [ENGLISH](../../../en/setup/remote-development/records.md)

# Local setup and connection records

Copy these templates only into ignored `.local/remote-development/<host>/` during authorized setup. Use `macbook`, `ws1`, `ws2`, `windows-laptop` or `ubuntu-laptop`; retain prior runs. On macOS/Linux, create with `umask 077` and `mkdir -p .local/remote-development/ACTUAL_HOST`, then restrict the directory to 700; on Windows restrict its ACL to the user. Never commit filled records. Store no passwords, private keys, authentication URLs or tokens here. Actual addresses, usernames, certificate fingerprints and environment paths stay local.

Use `PASS / FAIL / PENDING / NOT_APPLICABLE` with evidence and a reason. Missing required GUI functionality is pending/failure, not an optional omission. `GUI_READY=PASS` requires **both** RDP modes to pass for that client/WS pair. Unmeasured reboot or rendering stays pending. Read [test scenarios](network-rdp.md) and [GPU/recovery checks](ubuntu.md).

## CLIENT-CONNECTION.md

```text
Host role / actual host / OS / client OS / date: UNVERIFIED
Tailnet device name / address / key expiry / recovery contact: UNVERIFIED
Company network permission / Personal eligibility: UNVERIFIED
SSH alias / user / port / public host-key SHA256: UNVERIFIED
Project absolute path / task Python path / environment manager: UNVERIFIED
RDP Remote Login: address / port / auth method / public TLS SHA256: UNVERIFIED
RDP Desktop Sharing: address / port / auth method / public TLS SHA256: UNVERIFIED
Certificate comparison algorithm / trusted verification route / date: UNVERIFIED
Client profile names (WS1/WS2, Login/Sharing): UNVERIFIED
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
  Network context / direct, peer relay or DERP / latency / policy tests: UNVERIFIED
RDP_REMOTE_LOGIN_READY: PENDING: CLIENT_TEST_PENDING
RDP_DESKTOP_SHARING_READY: PENDING: CLIENT_TEST_PENDING
GUI_READY: PENDING: BOTH_MODES_REQUIRED
  Existing local app / input / Korean / clipboard / resolution: UNVERIFIED
  Per-mode lock / disconnect / session transition / monitor absent: UNVERIFIED
TMUX_DISCONNECT_READY: PENDING: UNTESTED
REBOOT_READY: PENDING: REBOOT_UNTESTED
  Old/new boot ID / SSH / Remote Login without local login: UNVERIFIED
  Disk unlock or other local intervention / Sharing availability: UNVERIFIED
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
