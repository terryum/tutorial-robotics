[한국어](../../../ko/setup/remote-development/laptops.md) | [ENGLISH](../../../en/setup/remote-development/laptops.md)

# Windows·Ubuntu 노트북 클라이언트

[공통 네트워크·RDP 절차](network-rdp.md)와 [검증 기록](records.md)을 사용합니다. 같은 WS 서버에 연결하지만 각 클라이언트·WS 조합은 **reader_test_required**입니다. [MacBook 안내](macbook.md)는 별도입니다. 노트북에 화면 접속을 받는 서버를 켜지 않습니다.

## Windows 노트북

1. 기존 VS Code, Remote-SSH/Python/Jupyter 확장, Git, `ssh -V`, 키와 Tailscale부터 조사합니다. 인증·설정을 보존합니다. OpenSSH Client가 없으면 Windows 설정 → 선택적 기능 → OpenSSH Client를 사용하며 OpenSSH Server는 설치하지 않습니다. [VS Code Windows](https://code.visualstudio.com/docs/setup/windows), [Tailscale Windows](https://tailscale.com/docs/install/windows)는 없고 허용된 경우만 설치합니다.
2. PowerShell에서 `Get-Command ssh, code, tailscale, mstsc`로 명령을 확인합니다. PATH에 없어도 앱은 설치돼 있을 수 있습니다. `%USERPROFILE%\.ssh\config`와 적절한 기존 키를 재사용합니다. 적절한 키가 없고 파일명이 비어 있을 때만 실행합니다.

```powershell
ssh-keygen -t ed25519 -f "$env:USERPROFILE\.ssh\id_ed25519_remote_robotics"
Get-Content "$env:USERPROFILE\.ssh\id_ed25519_remote_robotics.pub"
```

Passphrase는 사용자가 직접 입력합니다. 각 WS에 `.pub` 내용만 전달하고 기존 authorized keys를 보존합니다. 개인키·config는 Windows ACL로 사용자 접근만 허용하고 MacBook 개인키를 복사하지 않습니다. [SSH 별칭 템플릿](macbook.md)에 `~/.ssh/id_ed25519_remote_robotics` 같은 Windows 경로를 넣어 병합한 뒤 `ssh -G ws1`, `ssh ws1`, `ws2`와 신뢰할 수 있는 호스트키 지문을 확인합니다.

3. 기본 원격 데스크톱 연결(`mstsc`)의 **옵션 표시**에서 WS1 Login, WS1 Sharing, WS2 Login, WS2 Sharing 네 프로필을 만듭니다. 컴퓨터에는 WS Tailscale 이름·주소와 **실제 포트**를 넣습니다. 예: `ACTUAL_WS_ADDRESS:ACTUAL_LOGIN_PORT`. 별도 `.rdp` 파일을 로컬에 저장하며 평문 인증 정보를 넣지 않습니다. 대화형 실행 예시는 `mstsc /v:ACTUAL_WS_ADDRESS:ACTUAL_LOGIN_PORT`입니다. 공통 가이드대로 각 TLS 인증서와 모드별 인증을 확인합니다.
4. VS Code Remote-SSH로 실제 WS 프로젝트를 열고 WS에 작업공간 확장을 설치해 해당 작업의 기존 WS Python·kernel을 선택합니다. Windows 데스크톱·WSL interpreter는 원격 GPU 환경이 아닙니다. 기존 Codex 인증을 유지하고 [MacBook 가이드의 공통 개발 검증](macbook.md)에 따라 WS 터미널에서 원격 CLI를 확인합니다. 이 클라이언트 구성에 WSL은 필수가 아닙니다.

## Ubuntu 노트북

1. `cat /etc/os-release`, `command -v ssh code remmina tailscale`, 키와 확장을 확인하고 기존 앱을 재사용합니다. 필요하면 `openssh-client remmina remmina-plugin-rdp` 중 빠진 패키지만 검토해 `sudo apt install PACKAGE_NAMES`로 설치합니다. 자리표시자를 바꾸고 일괄 upgrade는 하지 않습니다. [VS Code Linux](https://code.visualstudio.com/docs/setup/linux), [Tailscale Linux](https://tailscale.com/docs/install/linux)는 없을 때만 설치하고 공통 네트워크 절차를 따릅니다. 접속만을 위해 이 클라이언트에 `openssh-server`, GNOME Remote Desktop, xrdp를 설치하지 않습니다.
2. `~/.ssh/config`와 적절한 로컬 키를 재사용합니다. 적절한 키가 없고 파일명이 비어 있을 때만 실행합니다.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_remote_robotics
cat ~/.ssh/id_ed25519_remote_robotics.pub
```

Passphrase는 로컬에서 입력합니다. `.ssh`는 700, 개인키·config는 600으로 보호하고 공개키만 전달합니다. [별칭 병합과 호스트키 확인](macbook.md)을 따릅니다.

3. Remmina에 WS1/WS2와 Login/Sharing을 구분한 RDP 프로필 네 개를 만듭니다. Server는 `ACTUAL_WS_ADDRESS:ACTUAL_MODE_PORT`이며 인증서별로 검증하고 대응하는 인증 정보를 대화형으로 입력합니다. 자격 증명 저장은 사용자의 의도에 따릅니다. [Ubuntu Remmina 안내](https://ubuntu.com/desktop/docs/en/24.04/how-to/access-a-remote-desktop/)를 참고하고 인증서 오류 전체 무시는 설정하지 않습니다.
4. Windows와 같은 Remote-SSH 폴더·원격 확장·WS Python/kernel 검증을 수행합니다. 누락 기능은 SSH 성공과 구분해 기록합니다.

## 공통 검증과 복구

두 OS에서 [loopback 터널 명령](macbook.md)을 사용합니다. WS1 로컬 포트는 8888/6006, WS2는 8889/6007 예시이며 원격 포트는 실제값을 씁니다. Jupyter 인증을 유지합니다. tmux는 **WS에서** 실행하고 클라이언트 절전과 SSH/RDP 종료 뒤 로그가 계속됐는지 확인합니다. 재부팅 복구에는 checkpoint가 필요합니다.

예상 결과: 외부망 SSH·원격 개발·두 RDP 모드·[세션/재부팅/성능 시나리오](network-rdp.md)에 WS별 증거가 있습니다. 시험 전에는 `.local/remote-development/windows-laptop/` 또는 `ubuntu-laptop/`에 `PENDING: CLIENT_TEST_PENDING`으로 씁니다. 서버 정보가 없으면 앱·키 준비를 마치고 접속 시험만 보류합니다. 같은 OS 노트북이 여러 대면 로컬 suffix를 붙여 기록을 덮어쓰지 않습니다.

복구: 병합한 SSH config를 시험하는 동안 이전 연결을 유지하고 문제가 생기면 이번에 백업한 블록만 복원합니다. WS 인증서를 신뢰할 경로로 확인한 뒤 새 RDP 프로필·인증서 pin만 수정·삭제합니다. 원격 설정 복구가 필요하면 [WS 복구 절차](ubuntu.md)를 사용하며 클라이언트 연결을 위해 인증을 약화하지 않습니다.

## 복사할 실행 요청문

### Windows 노트북

```text
docs/ko/setup/remote-development/index.md, laptops.md, network-rdp.md, records.md를 읽고 이 Windows 노트북을 Tailscale·OpenSSH/VS Code Remote-SSH·mstsc 클라이언트로 준비해줘. 기존 앱·키·인증을 보존하고 필요할 때만 이 장치의 키를 생성해 공개키만 전달해줘. 네트워크 설정 전 회사 허용과 Personal 요금제 적용을 확인해줘. WS별 Login/Sharing 프로필을 구분하고 노트북 서버 기능은 켜지 마. WS 정보가 없으면 독립 준비를 끝내고 접속만 대기로 남겨줘. 외부망에서 각 WS를 검증하고 .local/remote-development/windows-laptop/에 로컬 결과만 기록해줘. WS 소프트웨어 설치·수업 진도 변경을 하지 말고 MacBook 증거를 이 클라이언트 성공으로 대신하지 마.
```

### Ubuntu 노트북

```text
docs/ko/setup/remote-development/index.md, laptops.md, network-rdp.md, records.md를 읽고 이 Ubuntu 노트북을 Tailscale·OpenSSH/VS Code Remote-SSH·Remmina 클라이언트로 준비해줘. 기존 앱·키·인증을 보존하고 필요할 때만 이 장치의 키를 생성해 공개키만 전달해줘. 네트워크 설정 전 회사 허용과 Personal 요금제 적용을 확인해줘. WS별 Login/Sharing 프로필을 구분하고 노트북 서버 기능은 켜지 마. WS 정보가 없으면 독립 준비를 끝내고 접속만 대기로 남겨줘. 외부망에서 각 WS를 검증하고 .local/remote-development/ubuntu-laptop/에 로컬 결과만 기록해줘. WS 소프트웨어 설치·수업 진도 변경을 하지 말고 다른 클라이언트 증거를 성공으로 대신하지 마.
```
