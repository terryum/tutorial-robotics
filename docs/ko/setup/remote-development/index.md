[한국어](../../../ko/setup/remote-development/index.md) | [ENGLISH](../../../en/setup/remote-development/index.md)

# MacBook · WS1 · WS2 원격 로봇 개발

작성·공식 자료 확인: 2026-10-01. **추가 설치 실행 안내이며 설치 완료 보고서가 아닙니다.** 각 장비에서 이 저장소의 문서를 읽고 실제 상태를 조사한 뒤 필요한 항목만 설치합니다.

## 역할과 실행 순서

| 대상 | 읽을 문서 | 역할과 범위 |
|---|---|---|
| MacBook | [MacBook 설정](macbook.md) | SSH·VS Code 클라이언트, 코드·결과 확인. 기존 로컬 Core 개발도 유지 |
| WS1 Ubuntu | [Ubuntu 설정](ubuntu.md), 역할 `ws1` | DEVELOPMENT에서 독립 GPU 개발·학습; ROBOT_RUNTIME에서는 학습 중지 |
| WS2 Ubuntu | [Ubuntu 설정](ubuntu.md), 역할 `ws2` | DEVELOPMENT에서 독립 GPU 개발·학습; ROBOT_RUNTIME에서는 학습 중지 |

장비 이름은 실행 권한이나 설치 상태를 뜻하지 않습니다. 두 WS는 독립적으로 준비할 수 있으며 MacBook 설치나 다른 WS의 완료를 기다릴 필요가 없습니다. 분산 학습·공유 스토리지·실물 로봇 연결은 이 안내에 포함하지 않습니다.

1. 각 장비의 기존 설정과 설치 이력을 확인합니다. MacBook은 서버 정보가 없어도 앱·공개키 준비까지 진행합니다.
2. 각 WS에서 공통 Ubuntu 절차를 수행하고 로컬 `CLIENT-CONNECTION.md`를 만듭니다. SSH가 없는 서버는 현지 터미널 또는 이미 작동하는 원격 화면으로 시작합니다.
3. MacBook에서 각 WS의 접속 정보를 받아 SSH → VS Code → 원격 Python/Codex → GPU 시험을 확인합니다.
4. GUI와 재부팅 후 접속은 각각 별도로 검증합니다. 재부팅이 필요하면 먼저 복구 경로와 재개 기록을 준비합니다.

WS의 원격 터미널에서 실행한 코드가 WS GPU를 사용합니다. Codex 자체의 추론을 RTX GPU에서 실행한다는 뜻은 아닙니다. MacBook의 파일이 원격 Codex에 자동 전달되지는 않습니다.

## 각 컴퓨터에서 복사할 요청문

해당 장비의 `tutorial-robotics` checkout에서 Codex를 시작합니다. 먼저 이 문서 변경이 그 checkout에도 있는지 확인하세요. 아직 GitHub에 게시하지 않은 변경은 `git pull`로 받을 수 없습니다. 그 경우 문서 묶음만 안전하게 전달하거나 별도로 게시한 뒤 동기화합니다. `.local/`, 인증 파일, 가상환경을 함께 복사하지 않습니다.

### MacBook

```text
docs/ko/setup/remote-development/index.md와 macbook.md를 읽고 이 MacBook의 원격 로봇 개발 환경을 실제로 추가 설치·설정·검증해줘. AGENTS.md와 기존 설정을 보존하고 필요한 변경을 먼저 보여줘. WS 정보가 없으면 앱과 SSH 공개키 준비부터 끝내줘. 기록은 .local/remote-development/macbook/에 남기고 WS1·WS2별 미검증 항목을 구분해줘. 튜토리얼 완료나 원격 장비 설치를 대신 주장하지 마.
```

### WS1 Ubuntu

```text
docs/ko/setup/remote-development/index.md와 ubuntu.md를 읽고 현재 장비를 논리 역할 ws1, DEVELOPMENT 대상으로 조사한 뒤 필요한 원격 로봇 개발 환경을 추가 설치·검증해줘. 실제 ROBOT_RUNTIME 작업이 있으면 자동으로 종료하거나 모드를 바꾸지 말고 해당 변경을 보류해줘. 기존 ROS·GPU·Isaac 환경과 lock을 재사용하고 누락된 항목만 준비해줘. 기록은 .local/remote-development/ws1/에 남겨줘. 재부팅은 영향·복구 경로·재개 기록을 준비한 뒤 승인 범위 안에서 진행해줘. 실물 로봇 연결과 제어는 하지 마.
```

### WS2 Ubuntu

```text
docs/ko/setup/remote-development/index.md와 ubuntu.md를 읽고 현재 장비를 논리 역할 ws2, DEVELOPMENT 대상으로 조사한 뒤 필요한 원격 로봇 개발 환경을 추가 설치·검증해줘. 실제 ROBOT_RUNTIME 작업이 있으면 자동으로 종료하거나 모드를 바꾸지 말고 해당 변경을 보류해줘. WS1 설정을 복제하지 말고 이 장비의 GPU·드라이버·디스크·기존 환경을 확인해줘. 기록은 .local/remote-development/ws2/에 남겨줘. 재부팅은 영향·복구 경로·재개 기록을 준비한 뒤 승인 범위 안에서 진행해줘. 실물 로봇 연결과 제어는 하지 마.
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

모든 경로는 해당 장비의 checkout 기준입니다. 설치가 승인된 시점에 `.local/remote-development/<host>/`를 만들고 사용자만 접근하도록 보호합니다. `<host>`는 `macbook`, `ws1`, `ws2`입니다. 읽기 전용 점검만 요청받았다면 파일을 만들지 않습니다. 재실행 시 기존 기록을 읽고 실행별 로그는 별도 하위 폴더에 보존합니다.

- `RESULT.md`: 실제 host/OS, 유지·설치·변경·보류 내역, 정확한 버전·환경 경로, 아래 상태와 근거 로그.
- `CLIENT-CONNECTION.md`: WS의 사용자·주소·포트·공개 호스트키 SHA256 지문·프로젝트/Python 절대경로. 실제 접속 정보는 Git에 넣지 않습니다.
- `RESUME.md`: 미완료 이유, 다음 명령, 필요한 사용자 조작, 백업·복구 경로, 다시 읽을 가이드의 실제 경로.
- `gpu-smoke-result.json`과 실행 로그: 선택 환경·GPU, FP32/BF16, optimizer 변경, checkpoint 재개 결과. MacBook에는 원격 시험을 관찰한 근거만 남깁니다.

| 항목 | PASS의 근거 |
|---|---|
| SSH_READY | 서버 활성 + MacBook의 실제 키 인증 접속 |
| REMOTE_DEV_READY | 원격 폴더·WS Python·WS Codex CLI 동작 확인 |
| GPU_READY | 실제 GPU에서 finite loss/gradient와 optimizer 갱신 |
| CHECKPOINT_READY | 새 프로세스가 checkpoint를 읽고 학습 step을 추가 진행 |
| GUI_READY | 실제 클라이언트의 화면·입력 확인, 라이선스·로그인 조건 기록 |
| REBOOT_READY | boot ID 변경 + 현지 로그인 없이 재접속 + GPU 재검증 |

상태는 `PASS / FAIL / PENDING / NOT_APPLICABLE`입니다. 서버 측만 확인한 접속은 `PENDING: CLIENT_TEST_PENDING`, 재부팅을 시험하지 않았으면 `PENDING: REBOOT_UNTESTED`로 씁니다. GPU 미탑재/선택 GUI 미구성은 이유와 함께 `NOT_APPLICABLE`; 필요한 인증·라이선스·주소가 없으면 `PENDING: NEEDS_INPUT`입니다. 다른 WS의 성공으로 대체하지 않습니다.

이 결과는 환경 준비 증거입니다. 수업 완료·Isaac 실행·정책 성능·하드웨어 권한을 자동 부여하지 않습니다. 기존 설치 이력과 host ledger를 새 성공으로 덮어쓰지 않으며 learner progress도 변경하지 않습니다.

## 원본과 통합 관계

2026-10-01 제공된 `00-START-HERE.md`는 이 색인으로, `01-MACBOOK-SETUP.md`는 MacBook 가이드로, `02-WS1-UBUNTU-SETUP.md`와 `03-WS2-UBUNTU-SETUP.md`는 역할을 구분한 공통 Ubuntu 가이드로 통합했습니다. OCR 대회 경로·데이터·전용 패키지는 제외했습니다. 원본 파일은 수정하지 않습니다.

공용 설치 기준은 이 저장소입니다. 로봇별 private overlay는 자기 문서에서 이 가이드를 참조하고 private 구현·장비 정보는 공용 문서로 옮기지 않습니다.

private overlay가 과거 public commit을 정확히 고정했다면 최신 가이드 열람과 runtime checkout을 구분합니다. 가이드는 브라우저나 별도 문서 checkout에서 읽고, private 실행은 기존 pin에 맞는 checkout에서 합니다. 최신 main을 받았다는 이유로 pin 검사를 무시하거나 lock을 바꾸지 않습니다. 새 runtime 기준 채택은 별도 호환성 검증이 필요합니다.
