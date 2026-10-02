[한국어](../../../ko/setup/remote-development/index.md) | [ENGLISH](../../../en/setup/remote-development/index.md)

# MacBook · WS1 · WS2 원격 로봇 개발

갱신: 2026-10-02. RustDesk 근거는 이날 확인했습니다. **추가 설치 실행 안내이며 설치 완료 보고서가 아닙니다.** 각 장비에서 이 저장소의 문서를 읽고 실제 상태를 조사한 뒤 필요한 항목만 설치합니다.

기본 구성은 **RustDesk + Tailscale + OpenSSH/VS Code**, 작업 유지는 tmux와 작업별 checkpoint입니다. 이번 산출물은 게시된 설치 준비 문서이며 앱 설치·WS 설정·실제 접속은 미검증입니다. 다음 실행 순서는 **MacBook → WS1 → WS2**이고 각 WS 설치 후 MacBook으로 돌아와 해당 WS를 검증합니다. 설치된 NoMachine 클라이언트는 제거하지 않고 사용을 보류합니다.

사용자 확인에 따르면 동료가 WS1·WS2에서 이미 RustDesk를 사용 중입니다. 버전·서버 구성·무인접속은 아직 미확인입니다. 그 연결 경로를 재사용하고 Tailscale은 SSH·개발 서비스용으로 별도 유지합니다. 접속 정보가 있으면 MacBook 단계에서 기존 RustDesk 연결부터 시험할 수 있습니다. 이전 RDP 준비·NoMachine 설치 기록은 변환하지 않고 당시 사실로 보존합니다.

- [RustDesk 화면 제어·무인접속](rustdesk.md)
- [공통 네트워크·RDP·선택 근거·성능 시험](network-rdp.md)
- [Windows·Ubuntu 노트북과 별도 실행 요청문](laptops.md)
- [로컬 접속·결과·복구 기록 양식](records.md)

## 역할과 실행 순서

| 대상 | 읽을 문서 | 역할과 범위 |
|---|---|---|
| MacBook | [MacBook 설정](macbook.md) | SSH·VS Code 클라이언트, 코드·결과 확인. 기존 로컬 Core 개발도 유지 |
| Windows·Ubuntu 노트북 | [클라이언트 설정](laptops.md) | 미래 클라이언트; 각각 별도 검증 |
| WS1 Ubuntu | [Ubuntu 설정](ubuntu.md), 역할 `ws1` | DEVELOPMENT에서 독립 GPU 개발·학습; ROBOT_RUNTIME에서는 학습 중지 |
| WS2 Ubuntu | [Ubuntu 설정](ubuntu.md), 역할 `ws2` | DEVELOPMENT에서 독립 GPU 개발·학습; ROBOT_RUNTIME에서는 학습 중지 |

장비 이름은 실행 권한이나 설치 상태를 뜻하지 않습니다. 두 WS는 독립적으로 준비할 수 있으며 MacBook 설치나 다른 WS의 완료를 기다릴 필요가 없습니다. 분산 학습·공유 스토리지·실물 로봇 연결은 이 안내에 포함하지 않습니다.

1. 각 장비의 기존 설정과 설치 이력을 확인합니다. MacBook은 서버 정보가 없어도 앱·공개키 준비까지 진행합니다.
2. 각 WS에서 공통 Ubuntu 절차를 수행하고 로컬 `CLIENT-CONNECTION.md`를 만듭니다. SSH가 없는 서버는 현지 터미널 또는 이미 작동하는 원격 화면으로 시작합니다.
3. MacBook에서 각 WS의 접속 정보를 받아 SSH → VS Code → 원격 Python/Codex → GPU 시험을 확인합니다.
4. GUI와 재부팅 후 접속은 각각 별도로 검증합니다. 재부팅이 필요하면 먼저 복구 경로와 재개 기록을 준비합니다.

WS의 원격 터미널에서 실행한 코드가 WS GPU를 사용합니다. Codex 자체의 추론을 RTX GPU에서 실행한다는 뜻은 아닙니다. MacBook의 파일이 원격 Codex에 자동 전달되지는 않습니다.

## 각 컴퓨터에서 복사할 요청문

해당 장비의 `tutorial-robotics` checkout에서 다음 세션을 시작하고 이 개정이 있는지 확인합니다. 동기화 전에 로컬 변경을 살펴보고 깨끗한 대응 branch에서만 `git pull --ff-only`를 사용합니다. 분기된 변경은 보존해 별도로 통합합니다. `.local/`, 인증 파일, 가상환경은 복사하지 않습니다. Private overlay가 runtime 기준을 고정했다면 공개 가이드나 별도 문서 checkout을 읽고 runtime pin은 바꾸지 않습니다.

### MacBook

```text
docs/ko/setup/remote-development/index.md, macbook.md, rustdesk.md, network-rdp.md, records.md를 읽고 이 MacBook의 원격 로봇 개발 환경을 실제로 추가 설치·설정·검증해줘. AGENTS.md와 기존 설정을 보존하고 필요한 변경을 먼저 보여줘. Personal 요금제 적용과 회사 허용을 확인한 뒤 Tailscale·RustDesk 클라이언트를 준비하고 NoMachine은 제거하지 말고 보류해줘. 노트북 서버 기능은 추가하지 말고 기존 RustDesk 설치·인증을 재사용하고 WS별 접속 항목을 만들어줘. 동료 설정·암호·서버 키를 보존하고 Tailscale 직접 IP 전환·새 중계 서버 구축은 하지 마. RDP는 RustDesk에서 필요한 기능이 부족할 때만 선택해줘. 접속 정보가 있으면 기존 연결부터 시험하고 GUI와 무인접속을 따로 기록해줘. WS 정보가 없으면 앱과 SSH 공개키 준비부터 끝내줘. 기록은 .local/remote-development/macbook/에 남기고 WS1·WS2별 미검증 항목을 구분해줘. 튜토리얼 완료나 원격 장비 설치를 대신 주장하지 마.
```

### WS1 Ubuntu

```text
docs/ko/setup/remote-development/index.md, ubuntu.md, rustdesk.md, network-rdp.md, records.md를 읽고 현재 장비를 논리 역할 ws1, DEVELOPMENT 대상으로 조사한 뒤 필요한 원격 로봇 개발 환경을 추가 설치·검증해줘. 실제 ROBOT_RUNTIME 작업이 있으면 자동으로 종료하거나 모드를 바꾸지 말고 해당 변경을 보류해줘. 기존 ROS·GPU·Isaac 환경과 lock을 재사용하고 누락된 항목만 준비해줘. 회사 허용과 Personal 적용을 확인하고 OpenSSH over Tailscale을 구성하고 기존 RustDesk를 조사·재사용하되 기존 SSH 복구 경로를 유지해줘. Exit node·subnet route·세션 강제 종료·자동 로그인·대체 데스크톱/서버 설치는 하지 마. RustDesk 버전·서비스/부팅·Wayland/Xorg·ID/relay 서버·인증 방식·활성 세션부터 확인해줘. 동료 설정·암호·서버 키 변경, RustDesk 재설치, Tailscale 직접 IP 전환, 새 중계 서버 구축, preview 설치는 하지 마. RDP는 선택 사항으로 두고 외부망 MacBook에서 RustDesk를 검증해줘. 잠금·재부팅 후 무인접속은 별도로 시험하고 증거가 없으면 대기로 남겨줘. 기록은 .local/remote-development/ws1/에 남겨줘. 재부팅은 영향·복구 경로·재개 기록을 준비한 뒤 승인 범위 안에서 진행해줘. 실물 로봇 연결과 제어는 하지 마.
```

### WS2 Ubuntu

```text
docs/ko/setup/remote-development/index.md, ubuntu.md, rustdesk.md, network-rdp.md, records.md를 읽고 현재 장비를 논리 역할 ws2, DEVELOPMENT 대상으로 조사한 뒤 필요한 원격 로봇 개발 환경을 추가 설치·검증해줘. 실제 ROBOT_RUNTIME 작업이 있으면 자동으로 종료하거나 모드를 바꾸지 말고 해당 변경을 보류해줘. WS1 설정을 복제하지 말고 이 장비의 GPU·드라이버·디스크·기존 환경을 확인해줘. 회사 허용과 Personal 적용을 확인하고 OpenSSH over Tailscale을 구성하고 기존 RustDesk를 조사·재사용하되 기존 SSH 복구 경로를 유지해줘. Exit node·subnet route·세션 강제 종료·자동 로그인·대체 데스크톱/서버 설치는 하지 마. RustDesk 버전·서비스/부팅·Wayland/Xorg·ID/relay 서버·인증 방식·활성 세션부터 확인해줘. 동료 설정·암호·서버 키 변경, RustDesk 재설치, Tailscale 직접 IP 전환, 새 중계 서버 구축, preview 설치는 하지 마. RDP는 선택 사항으로 두고 외부망 MacBook에서 RustDesk를 검증해줘. 잠금·재부팅 후 무인접속은 별도로 시험하고 증거가 없으면 대기로 남겨줘. 기록은 .local/remote-development/ws2/에 남겨줘. 재부팅은 영향·복구 경로·재개 기록을 준비한 뒤 승인 범위 안에서 진행해줘. 실물 로봇 연결과 제어는 하지 마.
```

<a id="codex-bootstrap"></a>

## 아직 Codex가 없는 장비

기존 설치는 `command -v codex`, `codex --version`으로 확인하고 유지합니다. 없을 때만 사람이 현지 터미널 또는 인증된 SSH에서 [공식 설치 절차](https://developers.openai.com/codex/cli/)를 수행합니다. macOS/Linux 독립 설치 예시는 다음과 같습니다. 기존 npm/Homebrew 설치와 중복하지 않고 `sudo codex`를 쓰지 않습니다.

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
# 설치기가 안내한 PATH를 적용하거나 새 터미널을 연 뒤:
codex --version
codex login status
```

원격 로그인에는 계정/조직에서 허용하는 경우 `codex login --device-auth`를 사용하고 본인이 MacBook 브라우저에서 인증합니다. 사용할 수 없으면 [공식 SSH callback 전달](https://developers.openai.com/codex/auth/)을 사용합니다. 예: MacBook에서 `ssh -L 127.0.0.1:1455:localhost:1455 ws1`로 접속한 세션에서 `codex login`. 포트 충돌을 먼저 확인합니다. 토큰·인증 캐시를 출력하거나 장비 간 복사하지 않습니다.

모델·MCP·skills·계정·권한 정책과 기존 사용자/관리자 설정을 유지합니다. 이 설치를 위해 sandbox를 끄거나 전역 모델·effort 설정을 바꾸지 않습니다.

<a id="records-and-acceptance"></a>

## 기록과 완료 기준

모든 경로는 해당 장비의 checkout 기준입니다. 설치가 승인된 시점에 `.local/remote-development/<host>/`를 만들고 사용자만 접근하도록 보호합니다. `<host>`는 `macbook`, `ws1`, `ws2`, `windows-laptop`, `ubuntu-laptop`입니다. 읽기 전용 점검만 요청받았다면 파일을 만들지 않습니다. 재실행 시 기존 기록을 읽고 실행별 로그는 별도 하위 폴더에 보존합니다.

- `RESULT.md`: 실제 host/OS, 유지·설치·변경·보류 내역, 정확한 버전·환경 경로, 아래 상태와 근거 로그.
- `CLIENT-CONNECTION.md`: WS의 사용자·주소·포트·공개 호스트키 SHA256 지문·프로젝트/Python 절대경로, Tailscale 장치, RustDesk 버전·장치 ID·서버 유형/주소·공개키 확인 경로·인증 방식·서비스 상태와 선택한 RDP 정보. [양식](records.md)을 사용하고 실제 정보는 로컬에만 둡니다. 암호·개인키·토큰은 저장하지 않습니다.
- `RESUME.md`: 미완료 이유, 다음 명령, 필요한 사용자 조작, 백업·복구 경로, 다시 읽을 가이드의 실제 경로.
- `gpu-smoke-result.json`과 실행 로그: 선택 환경·GPU, FP32/BF16, optimizer 변경, checkpoint 재개 결과. MacBook에는 원격 시험을 관찰한 근거만 남깁니다.

| 항목 | PASS의 근거 |
|---|---|
| SSH_READY | 서버 활성 + 해당 클라이언트의 실제 키 인증 접속 |
| REMOTE_DEV_READY | 원격 폴더·WS Python·WS Codex CLI 동작 확인 |
| GPU_READY | 실제 GPU에서 finite loss/gradient와 optimizer 갱신 |
| CHECKPOINT_READY | 새 프로세스가 checkpoint를 읽고 학습 step을 추가 진행 |
| EXTERNAL_NETWORK_READY | 외부망 SSH/RustDesk·직접/중계 경로·허용/비허용 접근 확인 |
| RDP_REMOTE_LOGIN_READY (선택) | 실제 클라이언트 로그인·모드별 인증·TLS 검증 |
| RDP_DESKTOP_SHARING_READY (선택) | 현지 앱·화면·입력·한글·클립보드·해상도 확인 |
| RUSTDESK_READY | 해당 클라이언트·WS의 실제 화면·입력·한글·클립보드·해상도 시험 |
| UNATTENDED_GUI_READY | RustDesk 잠금 후 재접속과 재부팅 후 현지 로그인·개입 없는 접속 모두 확인 |
| GUI_READY | 같은 클라이언트·WS의 RUSTDESK_READY 결과를 따름 |
| TMUX_DISCONNECT_READY | SSH·RustDesk 종료 뒤 로그 계속 기록 |
| GUI_RENDERING_READY | 설치된 앱의 실제 장면·렌더러·GPU와 성능 측정 |
| REBOOT_READY | boot ID 변경·현지 로그인 없는 SSH/RustDesk·GPU/checkpoint 재검증; 현지 암호 해제 제한 기록 |

상태는 `PASS / FAIL / PENDING / NOT_APPLICABLE`입니다. 서버 측만 확인한 접속은 `PENDING: CLIENT_TEST_PENDING`, 재부팅을 시험하지 않았으면 `PENDING: REBOOT_UNTESTED`로 씁니다. GPU 미탑재는 이유와 함께 `NOT_APPLICABLE`입니다. 필수 RustDesk 기능이 없으면 GUI를 원인과 함께 대기·실패로 남기며, 선택하지 않은 RDP는 `NOT_APPLICABLE: NOT_SELECTED`로 기록합니다. 또한, 필요한 인증·주소가 없으면 `PENDING: NEEDS_INPUT`입니다. 다른 WS·클라이언트 OS의 성공으로 대체하지 않습니다. [공통 시나리오](network-rdp.md)의 세션 조건과 성능도 기록합니다.

이 결과는 환경 준비 증거입니다. 수업 완료·Isaac 실행·정책 성능·하드웨어 권한을 자동 부여하지 않습니다. 기존 설치 이력과 host ledger를 새 성공으로 덮어쓰지 않으며 learner progress도 변경하지 않습니다.

## 원본과 통합 관계

2026-10-01 제공된 `00-START-HERE.md`는 이 색인으로, `01-MACBOOK-SETUP.md`는 MacBook 가이드로, `02-WS1-UBUNTU-SETUP.md`와 `03-WS2-UBUNTU-SETUP.md`는 역할을 구분한 공통 Ubuntu 가이드로 통합했습니다. OCR 대회 경로·데이터·전용 패키지는 제외했습니다. 원본 파일은 수정하지 않습니다.

공용 설치 기준은 이 저장소입니다. 로봇별 private overlay는 자기 문서에서 이 가이드를 참조하고 private 구현·장비 정보는 공용 문서로 옮기지 않습니다.

private overlay가 과거 public commit을 정확히 고정했다면 최신 가이드 열람과 runtime checkout을 구분합니다. 가이드는 브라우저나 별도 문서 checkout에서 읽고, private 실행은 기존 pin에 맞는 checkout에서 합니다. 최신 main을 받았다는 이유로 pin 검사를 무시하거나 lock을 바꾸지 않습니다. 새 runtime 기준 채택은 별도 호환성 검증이 필요합니다.
