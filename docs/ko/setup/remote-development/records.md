[한국어](../../../ko/setup/remote-development/records.md) | [ENGLISH](../../../en/setup/remote-development/records.md)

# 로컬 설치·접속 기록 양식

설치가 승인된 실행에서만 아래 양식을 Git 제외 경로 `.local/remote-development/<host>/`에 복사합니다. `macbook`, `ws1`, `ws2`, `windows-laptop`, `ubuntu-laptop`을 사용하고 이전 실행 기록을 보존합니다. macOS/Linux는 `umask 077`, `mkdir -p .local/remote-development/ACTUAL_HOST` 후 디렉터리를 700으로 제한하고 Windows는 사용자 전용 ACL로 보호합니다. 채운 기록은 커밋하지 않습니다. 암호·개인키·인증 URL·토큰은 이곳에도 저장하지 않습니다. 실제 주소·사용자명·인증서 지문·환경 경로는 로컬에만 둡니다.

`PASS / FAIL / PENDING / NOT_APPLICABLE`에 증거와 이유를 붙입니다. 필수 GUI 기능 누락은 대기·실패이며 선택적 생략이 아닙니다. `GUI_READY`는 해당 클라이언트·WS의 화면·입력·한글·클립보드·해상도를 검증한 `RUSTDESK_READY`를 따릅니다. `UNATTENDED_GUI_READY`는 잠금 후 재접속과 재부팅 후 현지 로그인·개입 없는 접속이 모두 필요합니다. 미선택 RDP는 `NOT_APPLICABLE: NOT_SELECTED`, 선택한 모드는 클라이언트 증거가 필요합니다. 과거 기록은 변경하지 않습니다. 측정하지 않은 재부팅·렌더링은 대기로 둡니다. [시험 시나리오](network-rdp.md)와 [GPU·복구 검사](ubuntu.md)를 따릅니다.

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
