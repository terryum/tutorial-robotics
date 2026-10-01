[한국어](../../../ko/setup/remote-development/macbook.md) | [ENGLISH](../../../en/setup/remote-development/macbook.md)

# MacBook 원격 개발 클라이언트 설정

[전체 순서·실행 요청문·완료 기준](index.md)을 먼저 읽습니다. 이 문서는 MacBook만 변경합니다. WS의 설치는 [Ubuntu 가이드](ubuntu.md)에서 수행합니다. 기존 MacBook Core 개발 환경을 보존하고 서버용 CUDA·학습 데이터를 추가하지 않습니다.

## 1. 기존 상태와 변경 계획

`sw_vers`, `uname -m`, `command -v code codex brew ssh git`로 현재 도구를 확인합니다. VS Code 확장 목록과 Tailscale/NoMachine 설치 여부, SSH config의 WS 관련 블록·Include·Host *만 조사합니다. 전체 인증 파일이나 환경변수는 출력하지 않습니다.

기존 앱·키·VPN·설정을 재사용하고 누락된 항목, 설치 위치, 명령을 먼저 보여줍니다. 이 가이드의 실행 요청은 해당 사용자 설정과 도구의 추가 설치를 포함합니다. OS 권한은 정상 승인 절차를 따릅니다. 앱 업데이트·전체 패키지 업그레이드는 일괄 수행하지 않습니다.

승인된 설치 기록은 `.local/remote-development/macbook/`에 둡니다. 설정 변경 전 백업을 만들고 owner-only 권한을 유지합니다. 서버 주소·사용자·포트·프로젝트 경로는 기존 설정이나 해당 WS의 `CLIENT-CONNECTION.md`를 우선합니다. 없으면 독립 작업을 끝낸 뒤 필요한 값만 한 번에 요청합니다.

## 2. 앱과 확장

1. VS Code stable이 없으면 기존 Homebrew의 `brew install --cask visual-studio-code` 또는 [공식 macOS 설치](https://code.visualstudio.com/docs/setup/mac)를 사용합니다. `code`의 PATH를 확인합니다. Homebrew가 없다는 이유만으로 새 개발 도구 묶음을 설치하지 않습니다.
2. Git/OpenSSH가 동작하면 유지합니다. Apple Command Line Tools UI·관리자 인증은 필요한 순간에 사용자가 완료합니다.
3. Codex CLI는 기존 설치·로그인을 유지합니다. 없으면 [공식 설치·원격 인증 안내](index.md#codex-bootstrap)를 따릅니다.
4. `code --list-extensions`와 비교하여 없는 확장만 설치합니다.

```bash
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.debugpy
code --install-extension ms-toolsai.jupyter
```

Python/Jupyter 작업공간 확장은 접속 후 **SSH 대상 WS에도** 설치합니다. Codex IDE 확장은 선택 사항이며 [공식 안내](https://developers.openai.com/codex/ide/)에서 연결되는 배포본을 사용합니다. 실제 원격 실행 위치를 검증하지 않고 `remote.extensionKind`를 강제하지 않습니다. 기본 경로는 원격 터미널의 Codex CLI입니다.

기존 LAN/VPN으로 접속 가능하면 Tailscale은 필요 없습니다. 필요하고 조직에서 허용한 경우 [공식 macOS 앱](https://tailscale.com/docs/install/mac)을 하나만 설치하고 사용자가 로그인합니다. 기존 tailnet·exit node·subnet route를 바꾸지 않습니다.

GUI가 필요하면 [NoMachine 클라이언트](https://www.nomachine.com/download)를 선택합니다. MacBook에 서버 수신 기능을 추가하지 않습니다. 클라이언트는 무료지만 현재 v10 서버에는 평가 또는 구독 라이선스가 필요합니다. 자동 구매하지 않습니다. [라이선스 근거, 확인 2026-10-01](https://kb.nomachine.com/AR03P00972).

## 3. SSH 키와 별칭

재사용 가능한 키가 없으면 충돌하지 않는 전용 Ed25519 키를 생성합니다. 예시 이름은 `~/.ssh/id_ed25519_remote_robotics`입니다. passphrase는 사용자가 로컬 터미널에서 입력하며 ssh-agent/Keychain을 사용합니다. 개인키는 WS에 복사하지 않습니다. `.ssh`는 700, 개인키·config는 600 권한을 유지합니다.

공개키만 WS에 전달합니다. WS에서 기존 `authorized_keys`를 보존하며 등록한 뒤, 별도 세션에서 접속을 시험합니다. 첫 접속의 SHA256 호스트키 지문을 현지 콘솔이나 인증된 경로로 받은 WS 보고서와 대조합니다. `ssh-keyscan` 출력만으로 신뢰를 확정하거나 `StrictHostKeyChecking=no`를 쓰지 않습니다.

아래는 **활성화 전에 모든 값을 채워야 하는 템플릿**입니다. 기존 같은 별칭이 다른 장비를 가리키면 새 별칭을 정하고 이후 모든 명령에도 적용합니다. Include와 Host *의 첫 적용값을 고려해 병합합니다.

```sshconfig
Host ws1
  HostName ACTUAL_WS1_ADDRESS
  User ACTUAL_WS1_USER
  Port ACTUAL_WS1_SSH_PORT
  IdentityFile ACTUAL_PRIVATE_KEY_PATH
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
  ForwardAgent no

Host ws2
  HostName ACTUAL_WS2_ADDRESS
  User ACTUAL_WS2_USER
  Port ACTUAL_WS2_SSH_PORT
  IdentityFile ACTUAL_PRIVATE_KEY_PATH
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
  ForwardAgent no
```

`ssh -G ws1`과 `ssh -G ws2`의 유효 설정을 로컬에서 확인합니다. placeholder가 남아 있으면 접속 설정으로 사용하지 않습니다. 실제 접속 후 `hostname`, `id -un`, `pwd`, `nvidia-smi`로 목적지를 확인합니다. GPU 미탑재와 SSH 실패는 별도 결과입니다.

## 4. VS Code · Python · Codex

VS Code의 `Remote-SSH: Connect to Host...`에서 대상 별칭을 선택하고 **WS 보고서의 프로젝트 경로**를 엽니다. VS Code Server는 원격 사용자 계정에 설치되며 별도 WS 데스크톱 앱을 요구하지 않습니다. [Remote-SSH 근거, 확인 2026-10-01](https://code.visualstudio.com/docs/remote/ssh).

원격 표시와 터미널의 `hostname`을 확인하고 `codex --version`, `codex login status`를 실행합니다. Codex가 원격 경로에서 읽기와 임시 파일 작업을 수행하는지 확인합니다. 시험 파일은 WS의 기록 폴더 아래에만 둡니다. 클라우드 작업 제출을 WS GPU 실행 검증으로 대신하지 않습니다.

Python interpreter와 Notebook kernel은 **그 작업에 맞는 WS 환경**으로 선택합니다. Core는 기존 Python 3.12 `.venv`, GPU 작업은 WS 보고서에 등록한 별도 GPU 환경입니다. 모든 작업에 Core `.venv`나 MacBook Python을 선택하지 않습니다. 필요 시 해당 환경에만 `ipykernel`을 설치하며 기존 lock 관리 방식을 따릅니다.

## 5. 로그 · 포트 전달 · 지속 실행

WS에서 Jupyter는 token 인증을 유지한 채 `127.0.0.1`과 `--no-browser`, TensorBoard도 `127.0.0.1`에 바인딩합니다. 설치된 프로젝트 환경에서 실행하고 토큰은 보고서에 쓰지 않습니다. VS Code Ports 또는 다음 SSH 터널을 사용합니다.

```bash
# MacBook: WS1 서비스가 실제로 8888/6006에 떠 있을 때의 예
ssh -N -L 127.0.0.1:8888:127.0.0.1:8888 -L 127.0.0.1:6006:127.0.0.1:6006 ws1
# 두 WS를 동시에 볼 때 WS2의 로컬 포트는 다르게 선택
ssh -N -L 127.0.0.1:8889:127.0.0.1:8888 -L 127.0.0.1:6007:127.0.0.1:6006 ws2
```

포트 충돌 시 다른 빈 로컬 포트를 기록합니다. 서비스나 포트를 인터넷에 공개하지 않습니다. 원격 결과 파일의 존재와 해시를 확인한 뒤 필요한 작은 파일만 가져옵니다. 대용량 데이터·checkpoint 전체 복제나 `rsync --delete`는 기본 작업이 아닙니다.

각 WS에서 `tmux new -As robotics-ws1` 또는 `robotics-ws2`로 작업합니다. `Ctrl-b` 다음 `d`로 분리하고 같은 명령으로 복귀합니다. 짧은 합성 로그 작업을 시작해 SSH 종료 및 MacBook 절전 후에도 이어지는지 실제 확인합니다. MacBook 전체 절전을 끌 필요는 없습니다. **WS 재부팅은 tmux와 학습을 종료**하므로 checkpoint 재개가 별도로 필요합니다.

## 6. GUI · 재접속 · 마무리

NoMachine은 WS의 실제 VPN/LAN 주소와 설정 포트로 연결합니다. 화면·키보드 입력을 시험하고 로컬 로그인 전, 잠금 상태, 모니터 없는 상태는 별도 결과로 기록합니다. GUI가 없거나 라이선스가 대기 중이어도 SSH 개발의 성공은 별도로 남깁니다. 화면이 보인다는 사실만으로 Isaac GPU 렌더링 성공을 주장하지 않습니다.

WS 재부팅 시험은 [Ubuntu 복구 절차](ubuntu.md)를 먼저 수행하고 승인된 경우에만 진행합니다. MacBook에서 현지 로그인 없이 새 SSH·VS Code 연결, GPU 시험, 선택 GUI 접속을 확인합니다. 재부팅하지 않았으면 `REBOOT_UNTESTED`입니다.

`RESULT.md`에 WS별 [완료 기준](index.md#records-and-acceptance), 유지/설치한 앱과 버전, 변경·백업 위치를 남깁니다. `RESUME.md`에는 아직 필요한 주소·인증·라이선스·현지 작업과 정확한 다음 명령을 씁니다. 미검증 연결을 완료로 바꾸지 않습니다.
