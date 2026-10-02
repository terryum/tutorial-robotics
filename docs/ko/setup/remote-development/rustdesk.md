[한국어](../../../ko/setup/remote-development/rustdesk.md) | [ENGLISH](../../../en/setup/remote-development/rustdesk.md)

# RustDesk 우선 화면 제어

확인: 2026-10-02. 사용자 확인에 따르면 동료가 WS1·WS2에서 RustDesk를 사용 중입니다. 버전·서버 구성·무인접속은 **UNVERIFIED**입니다. 이번 작업은 준비 문서 게시이며 각 클라이언트·WS 조합은 **reader_test_required**입니다. [실행 순서와 요청문](index.md)에서 시작합니다.

화면·입력은 기존 RustDesk, 개발은 Tailscale + OpenSSH/VS Code, 작업 유지는 WS의 tmux + checkpoint를 사용합니다. 처음에는 동료가 사용 중인 RustDesk 연결 경로를 재사용합니다. RustDesk를 Tailscale 직접 IP로 자동 전환하거나 새 ID/relay 서버를 구축하지 않습니다. Tailscale 성공은 RustDesk 경로 검증이 아닙니다.

## 변경 전에 WS마다 조사

대상 사용자와 앱 버전/build channel·장치 ID·공용/자체 ID 및 relay 서버·인증 방식·활성 세션을 확인합니다. 로컬 [CLIENT-CONNECTION.md](records.md)에 필요한 항목만 기록하고 설정 파일 전체나 암호를 출력·촬영하지 않습니다. 서비스와 부팅 상태는 읽기 전용으로 확인합니다.

```bash
command -v rustdesk
rustdesk --version
dpkg-query -W rustdesk
systemctl is-active rustdesk.service
systemctl is-enabled rustdesk.service
loginctl list-sessions
loginctl show-session ACTUAL_SESSION_ID -p Type -p State -p Remote
```

세션 자리표시자를 바꿉니다. 실행 파일·패키지·unit이 없으면 다른 설치 방식일 수 있으므로 앱과 실제 launcher를 확인한 뒤 미설치 여부를 판단합니다. 대상 데스크톱과 로그인 화면의 Wayland/Xorg를 각각 확인합니다. 동료의 접속 설정·암호·서버 키·활성 서비스를 보존합니다. 이번 준비를 위해 정상 서비스를 재설치·재시작·업데이트하지 않습니다.

자체 서버라면 기존 ID/relay 주소를 받고 관리자 또는 인증된 기존 설정을 통해 **공개** 서버 키를 확인한 경로를 로컬에 남깁니다. 서버 개인키를 요청하거나 복사하지 않습니다. 설치 버전에 맞는 [공식 클라이언트 설정](https://rustdesk.com/docs/en/self-host/client-configuration/)을 따릅니다. 기존 인증을 보존하고 비밀값은 대화형 입력 또는 사용자 자격 증명 관리자를 사용합니다. 정보·권한이 없으면 `PENDING: NEEDS_INPUT`으로 남기고 독립적인 SSH 준비를 계속합니다.

## 노트북의 발신 클라이언트 준비

기존 앱·인증부터 재사용합니다. 없으면 [공식 클라이언트 다운로드](https://rustdesk.com/docs/en/client/)에서 실제 OS/아키텍처에 맞는 build를 선택하고 버전을 기록합니다. 설치는 이후 실행 단계이며 이번 문서 갱신의 결과가 아닙니다.

| 클라이언트 | 없을 때 설치 경로 | 범위 |
|---|---|---|
| MacBook | [macOS 안내](https://rustdesk.com/docs/en/client/mac/): 맞는 `.dmg`를 열어 Applications로 이동 | 발신 입력에 필요한 권한만 허용하며 Input Monitoring이 필요할 수 있습니다. 로컬 화면 캡처 권한을 이유로 수신 제어를 켜지 않습니다. |
| Windows 노트북 | [Windows 안내](https://rustdesk.com/docs/en/client/windows/): 맞는 공식 클라이언트 build | 발신 클라이언트로 사용하며 노트북 무인 수신 서비스·암호를 설정하지 않습니다. |
| Ubuntu 노트북 | [Linux 안내](https://rustdesk.com/docs/en/client/linux/): 맞는 `.deb`, `sudo apt install ./ACTUAL_RUSTDESK_PACKAGE.deb` 검토 | 패키지·서비스 영향을 확인하고 수신을 비활성으로 유지합니다. 접속만을 위해 부팅 수신 서비스를 켜지 않습니다. |

설치 버전의 수신 제어 설정을 확인하고 노트북 수신을 비활성으로 둡니다. 원격 제어 앱 설치가 노트북 서버 구성 허가는 아닙니다. 무인 배포 옵션·권한 일괄 초기화는 피합니다. 관련 없는 기존 설정은 보존하며 발신 전용 사용과 충돌하면 변경 전에 기록하고 해결합니다.

확인한 장치 ID와 기존 서버 경로로 WS1·WS2 로컬 접속 항목을 만듭니다. 두 WS의 서버 구성이 다르면 접속마다 맞는 구성을 확인하고 공유 프로필을 몰래 덮어쓰지 않습니다. 정보가 있으면 WS SSH 준비 전에도 MacBook 단계에서 기존 RustDesk를 시험합니다. 동료의 전체 설정·인증 캐시는 복사하지 않습니다.

## Wayland: 일반 릴리스와 preview 구분

[일반 Linux 문서](https://rustdesk.com/docs/en/client/linux/)는 1.2.0부터 Wayland 실험 지원과 로그인 화면 접근의 X11 요구를 설명합니다. 별도 [2026-08-14 발표](https://www.rustdesk.com/blog/unattended-remote-access-wayland/)는 x86_64 Debian/Ubuntu preview에서 재부팅 후 로그인 화면 무인접속·다중 모니터를 설명하며 일반 릴리스 통합은 향후 작업이라고 명시합니다. 실행 당일 설치 릴리스의 지원을 다시 확인합니다. 동료가 preview를 사용한다고 추정하거나 일반 Wayland 접속을 무인접속 증거로 쓰지 않습니다.

Preview 설치·Xorg 전환·자동 로그인·세션 강제 종료는 기본 해결책이 아닙니다. 현재 세션을 유지하고 현지 승인·로그인 필요 조건을 기록하며 SSH 작업을 계속합니다. 필요한 기능이 부족하면 그 기능에 대해 [선택적 GNOME RDP](network-rdp.md)를 별도 증거와 함께 검토합니다.

## 완료 기준과 복구

[외부망·잠금·모니터·tmux·재부팅·동일 장면 성능 시험](network-rdp.md)을 WS/클라이언트마다 수행합니다. `RUSTDESK_READY=PASS`는 실제 화면·입력·한글·클립보드·해상도 성공이 필요하며 기본 `GUI_READY`도 이를 따릅니다. `UNATTENDED_GUI_READY=PASS`에는 잠금 후 재접속과 승인된 재부팅 후 현지 로그인·개입 없는 접속이 모두 추가로 필요합니다. 일반 화면·서비스 활성·동료의 성공만으로 입증하지 않습니다.

실제 ID·주소·공개키 확인 경로·인증 방식은 Git 제외 `.local/`에만 두고 암호·개인키·토큰은 기록하지 않습니다. 이전 실행은 보존합니다. 기존 SSH·현지 지원으로 복구하며 이번 클라이언트 항목·설정만 되돌립니다. 동료 서비스를 방해하거나 인증을 약화하지 않습니다. [기록 양식](records.md)에 대기 원인·증거·정확한 다음 작업을 남깁니다.
