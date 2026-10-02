[한국어](../../../ko/setup/remote-development/network-rdp.md) | [ENGLISH](../../../en/setup/remote-development/network-rdp.md)

# 네트워크·RDP·소프트웨어 선택

작성 2026-10-02. 모든 WS·클라이언트 조합은 **reader_test_required**입니다. [실행 순서](index.md), [Ubuntu 서버](ubuntu.md), [로컬 기록 양식](records.md)을 함께 읽습니다. 이 문서는 설치 준비 자료이며 실제 서비스 설치·접속 성공의 증거가 아닙니다.

## 이 구성을 선택한 이유

| 용도 | 기본 선택 | 이유 |
|---|---|---|
| 외부망 연결 | Tailscale | 일반적으로 공인 고정 IP·공유기 포트포워딩 없이 장치 간 비공개 연결 |
| 편집·명령 실행 | OpenSSH + VS Code Remote-SSH | 기존 키·셸·프로젝트 환경 재사용 |
| 연결 종료 후 학습 | tmux + 작업별 checkpoint | 터미널 재접속과 프로세스·재부팅 이후 복구를 각각 지원 |
| Ubuntu 전체 화면 | 기존 GNOME Remote Desktop의 RDP | RDP 서버 구독료 없음; 로그인과 공유 모두 준비 |
| 노트북 클라이언트 | Mac의 Windows App, Windows의 mstsc, Ubuntu의 Remmina | 같은 WS 구성에 연결하는 OS별 RDP 앱 |
| Isaac 화면 | 필요 시 버전에 맞는 NVIDIA WebRTC | 앱 전용 스트리밍을 별도 검증 |

개인·비상업 연구 목적입니다. 실제 설치 전에 [Tailscale Personal 요금 조건](https://tailscale.com/pricing) 적용 여부와 회사 네트워크 사용 허용을 확인합니다. 회사에 있는 장비라는 사실만으로 어느 쪽도 확정하지 않습니다. 미확정이면 오프라인 앱·키 준비를 끝내고 네트워크만 대기로 기록합니다. 유료 요금제에 자동 가입하지 않습니다.

```text
MacBook / Windows / Ubuntu 노트북 (클라이언트)
  Tailscale 암호화 장치 연결 (직접 또는 중계)
    +-- OpenSSH --> WS 터미널 / VS Code --> Python / GPU / tmux
    |                +-- loopback 터널 --> Jupyter / TensorBoard
    +-- RDP ------> WS1 또는 WS2의 GNOME Remote Desktop (서버)
                       +-- Remote Login     (예: TCP 3389)
                       +-- Desktop Sharing  (예: TCP 3390)
                       +-- GNOME compositor / Wayland / GPU 렌더러
```

SSH와 화면 접속은 독립적입니다. Wayland는 WS의 화면·세션 시스템이지 클라이언트 앱이나 VPN이 아닙니다. 기존 세션 종류를 유지하며 시험합니다. Xorg 전환, xrdp 설치, GNOME 재설치, 자동 로그인, 다른 사람의 세션 종료를 기본 해결책으로 쓰지 않습니다. SSH 성공은 화면·GPU 렌더링 성공이 아닙니다. RDP 연결 종료가 로그아웃과 같은지도 실제 시험합니다. tmux는 checkpoint가 아니며 재부팅을 견디지 못합니다.

## 비공개 네트워크와 복구

[해당 OS의 공식 Tailscale 설치 경로](https://tailscale.com/download)를 사용하고 기존 설치·tailnet을 재사용합니다. WS는 [Linux 안내](https://tailscale.com/docs/install/linux)의 배포판별 패키지 절차를 따릅니다. 조사와 권한 확인 후 필요한 것만 설치하며 무인 일괄 설치기는 추가하지 않습니다. 새 Linux 설치에서 다음은 각각 검토해 수행할 단계입니다.

```bash
sudo systemctl enable --now tailscaled
sudo tailscale up
# 사용자가 직접 인증합니다. 인증 URL·토큰은 로그에 남기지 않습니다.
tailscale status
tailscale ping ACTUAL_WS_TAILSCALE_NAME
tailscale netcheck
```

`--ssh`는 넣지 않습니다. 기존 OpenSSH가 키 인증을 담당합니다. 기존 tailnet에서는 설정을 조사하고 필요한 변경만 하며 flag를 초기화하지 않습니다. Exit node, subnet route 광고·수락, 회사·로봇 네트워크 브리지를 구성하지 않습니다. 이미 해당 경로가 있으면 충돌과 범위를 기록해 해결한 뒤 이 가이드를 사용하며 관련 없는 VPN을 몰래 바꾸지 않습니다. 부팅 서비스·키 만료·재인증·복구 조건은 로컬에 남깁니다.

Tailnet grants/ACL에서 허용 사용자·장치와 실제 WS SSH/RDP 포트만 접근 가능한지 확인합니다. Tailnet 가입만으로 최소 권한이라고 판단하지 않습니다. 호스트 방화벽도 함께 조사합니다. [Tailscale 자체 netfilter 처리](https://tailscale.com/docs/reference/netfilter-modes)와 UFW가 상호작용할 수 있어 UFW만으로 제한을 입증할 수 없습니다. 기존 SSH·현지 복구 경로를 유지하고 UFW 초기화·규칙 일괄 삭제·공유기 또는 인터넷 RDP 개방은 하지 않습니다.

UFW를 이미 사용한다면 `sudo ufw status numbered`, 실제 listener는 `sudo ss -ltnp`로 확인합니다. 아래는 **템플릿**이며 완성된 정책이나 UFW 활성화 지시가 아닙니다. 모든 자리표시자를 바꾸고 기존 광범위 허용·주소 계열을 검토한 뒤 복구 경로가 있을 때 필요한 규칙만 추가합니다.

```bash
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SSH_PORT proto tcp
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_LOGIN_PORT proto tcp
sudo ufw allow in on tailscale0 from ACTUAL_CLIENT_TAILSCALE_IP to any port ACTUAL_SHARING_PORT proto tcp
```

예상 결과: 허용한 노트북은 필요한 서비스에 연결되고, 비허용 시험 장치는 차단되며, 허용하지 않은 LAN·공인 경로에서는 RDP가 열리지 않습니다. 해당 IPv4/IPv6 경로를 모두 확인합니다. 실패하면 네트워크 완료를 보류하고 유지한 세션에서 해당 grant·방화벽 규칙만 수정합니다. 변경 전에 추가할 규칙 번호·내용과 백업을 기록합니다. 복구는 이번 규칙만 삭제하고(`sudo ufw delete RULE_NUMBER`, 매번 번호 재확인) 이번 정책 변경만 되돌립니다. 유일한 복구 접속에서 Tailscale을 끄지 않습니다.

## WS마다 두 RDP 모드 준비

기존 세션을 보존하며 현지에서 조사합니다.

```bash
cat /etc/os-release
gnome-shell --version
loginctl list-sessions
# 대상 사용자의 실제 세션 ID로 바꿉니다.
loginctl show-session ACTUAL_SESSION_ID -p Type -p State -p Remote
dpkg-query -W gnome-remote-desktop
systemctl status gnome-remote-desktop.service --no-pager
systemctl --user status gnome-remote-desktop.service --no-pager
sudo ss -ltnp
```

사용자 서비스는 대상 사용자의 데스크톱·세션에서 확인합니다. SSH에 user bus가 없다는 사실은 데스크톱 서비스 장애의 증거가 아닙니다. 설정 전 비활성·누락 서비스는 조사 결과이며 다른 서버 설치 허가가 아닙니다. 과거 Ubuntu 24.04 기록과 별개로 현재 OS·GNOME 기능을 확인합니다.

**설정 → 시스템 → 원격 데스크톱**에서 대상 사용자 세션의 Desktop Sharing·Remote Control을 켭니다. Remote Login 패널을 관리자 권한으로 잠금 해제해 활성화하고 별도 자격 증명을 설정합니다. [GNOME 설정 안내](https://github.com/GNOME/gnome-remote-desktop/blob/main/docs/configuration.md)를 참고하고 CLI 도움말은 설치 버전에 맞춥니다. [Ubuntu 안내](https://ubuntu.com/desktop/docs/en/24.04/how-to/share-your-desktop-remotely/)의 Desktop Sharing은 로그인된 화면 공유, Remote Login은 원격 로그인입니다. 둘을 켰을 때 기본 포트는 공유 3390, 로그인 3389입니다. 실제 설정과 listener의 충돌을 확인합니다. 공유의 입력은 Remote Control도 켜야 합니다. 로그인·세션 전환 시험 전에 작업을 저장하고 활성 세션 종료 질문에 자동 동의하지 않습니다.

| 접속 | 확인할 인증 | 확인할 TLS 신뢰 |
|---|---|---|
| Desktop Sharing | 해당 모드에서 설정·표시한 자격 증명; SSH 인증과 같다고 가정하지 않음 | 해당 모드에 설정된 인증서·지문 |
| Remote Login | Remote Login의 RDP 입구 자격 증명, 이후 로그인 화면의 대상 Ubuntu 계정 | Remote Login 자체 인증서·지문 |

암호는 사용자의 자격 증명 관리자에 보관하거나 대화형으로 입력합니다. 명령 인수·스크린샷·로그·Git에는 넣지 않습니다. 기록에는 인증 *방식*만 씁니다. 각 모드의 **Verify Encryption**이 있으면 확인하고, 없으면 설치 버전의 설정·도움말에서 실제 **공개 인증서** 경로를 찾습니다. 공개 파일에서만 SHA256 지문을 계산합니다.

```bash
openssl x509 -in ACTUAL_PUBLIC_CERTIFICATE_PATH -noout -fingerprint -sha256
```

클라이언트가 제시한 인증서를 신뢰할 수 있는 WS 콘솔·인증된 보고서와 대조한 뒤 수락합니다. 알고리즘도 맞춰 비교합니다. UI가 다른 digest만 제공하면 동일 알고리즘끼리 비교하고 SHA256도 로컬에 보관합니다. TLS 개인키는 읽거나 복사하지 않고 변경된 인증서를 무조건 무시하지 않습니다. 두 프로필의 인증서·자격 증명이 같다고 가정하지 않습니다.

예상 결과: 두 listener가 GNOME Remote Desktop의 의도한 포트와 일치하고 노트북에서 각각 접속에 성공합니다. GNOME·필수 기능·인증·세션 호환성이 없으면 해당 모드를 사유와 함께 `PENDING`/`FAIL`로 남기고 SSH 작업을 계속합니다. GUI 완료로 처리하거나 다른 데스크톱·서버를 자동 설치하지 않습니다. 복구는 기존 SSH·현지 콘솔에서 이전 모드 설정과 이번 방화벽 변경만 되돌립니다. 문제 해결만을 위해 display manager를 재시작하거나 활성 사용자를 로그아웃시키지 않습니다.

## 회사 밖 네트워크에서 검증

**WS별·클라이언트 OS별** 날짜·버전·증거를 [records.md](records.md)에 기록합니다. MacBook 성공은 미래 Windows·Ubuntu 노트북의 검증이 아닙니다.

1. 집 Wi-Fi 또는 휴대전화 테더링을 사용합니다. 네트워크 상황을 기록하고 트래픽 발생 후 `tailscale ping ACTUAL_WS_TAILSCALE_NAME`, `tailscale status`로 [direct·peer relay·DERP](https://tailscale.com/docs/reference/connection-types)를 구분합니다. 첫 패킷의 중계만으로 지속 경로를 판단하지 않습니다. 새 키 인증 SSH와 두 RDP 프로필을 확인합니다.
2. Desktop Sharing에서 현지에 미리 열어 둔 앱을 확인합니다. 입력·한글·무해한 텍스트 클립보드·해상도·배율을 시험합니다. 비공개 내용은 증거로 사용하지 않습니다.
3. 작업을 저장한 후 사용자와 Remote Login·의도한 세션 전환을 시험합니다. **각 모드별** 잠금·재접속·모니터 미연결 동작을 기록합니다. GNOME 안내에서는 활성 세션 공유가 잠금 시 끊길 수 있으므로 이 버전의 동작과 Remote Login 복구 경로를 기록합니다. 실패한 조건은 제한으로 남깁니다.
4. tmux에서 짧은 로그 작업을 돌리고 SSH와 RDP를 끊은 뒤 다시 연결해 새 timestamp를 확인합니다. 로그아웃 정책이 작업을 종료하면 원인을 기록하며 전역 정책을 자동 완화하지 않습니다.
5. [재부팅 복구](ubuntu.md)를 준비하고 재부팅이 승인된 뒤에만 boot ID 변경, 현지 로그인 없는 SSH·Remote Login, GPU·checkpoint 재개를 확인합니다. Desktop Sharing은 사용자 세션이 필요할 수 있어 언제 사용 가능한지 기록합니다. 디스크 암호 해제 등 현지 개입이 필요하면 무인 재부팅 PASS가 아닙니다.
6. 설치된 RViz·Isaac의 동일 장면에서 비교합니다. WS·클라이언트 버전, 화면 크기, 네트워크 경로·지연, 렌더러·GPU, 장면, 입력 반응, 가능한 frame·encode·decode 지표를 기록합니다. 얻지 못한 수치는 “미측정”으로 씁니다. GUI 렌더링과 CUDA 연산은 따로 확인합니다.

제품을 바꾸기 전에 중계 경로·해상도·렌더러를 진단합니다. Isaac 전용은 [설치 버전에 맞는 NVIDIA WebRTC 문서](https://docs.isaacsim.omniverse.nvidia.com/latest/installation/manual_livestream_clients.html)를 보고 버전 간 포트·실행 명령을 그대로 복사하지 않습니다. 전체 3D 화면은 [Sunshine/Moonlight](https://github.com/LizardByte/Sunshine)를 무료 비교 후보로 둡니다. [RustDesk의 Wayland 지원](https://www.rustdesk.com/blog/unattended-remote-access-wayland/)은 무인접속 전에 안정 릴리스 지원을 확인해야 합니다. NoMachine은 측정된 문제가 남을 때만 당시 라이선스를 확인해 재검토합니다. 어느 후보도 이 장비에서 더 빠르다고 미리 단정하지 않으며 대안 설치는 별도 결정입니다.
