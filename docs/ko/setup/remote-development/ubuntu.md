[한국어](../../../ko/setup/remote-development/ubuntu.md) | [ENGLISH](../../../en/setup/remote-development/ubuntu.md)

# WS1 · WS2 Ubuntu 추가 설치와 검증

[전체 안내](index.md)의 해당 WS 요청문으로 시작합니다. 공통 절차를 각 장비에서 독립 실행하며 다른 장비의 주소·키·GPU index·가상환경을 복사하지 않습니다. 이 안내를 읽는 것만으로 설치가 승인되지는 않습니다. 실행 요청을 받으면 필요한 변경 계획을 보여주고 실제 추가 설치·검증까지 진행합니다.

## 1. 대상과 기존 환경 조사

| 논리 역할 | SSH 별칭 예시 | 기록 폴더 | tmux 세션 예시 |
|---|---|---|---|
| WS1 | `ws1` | `.local/remote-development/ws1/` | `robotics-ws1` |
| WS2 | `ws2` | `.local/remote-development/ws2/` | `robotics-ws2` |

사용자가 지정한 논리 역할을 실제 hostname·OS·사용자와 대조합니다. hostname은 바꾸지 않습니다. 반대 WS 역할의 기록이 있으면 중복 대상인지 확인합니다. 두 WS 모두 **DEVELOPMENT에서는 학습 가능**, ROBOT_RUNTIME에서는 학습을 병행하지 않습니다. 실행 중인 로봇 서비스·다른 사용자의 학습은 종료하지 말고 충돌하는 변경을 보류합니다.

현재 checkout과 상위 `AGENTS.md`, [기존 host 이력](https://github.com/terryum/tutorial-robotics/blob/main/state/HOST_STATUS.md), 해당 Ubuntu 설치 보고서를 읽습니다. [WS1 이력](https://github.com/terryum/tutorial-robotics/blob/main/setup/WS1_UBUNTU_VERIFICATION_2026-09-11.md)과 [WS2 이력](../../../WS2_UBUNTU_INSTALLATION_STATUS.md)은 조사 출발점이며 현재 성공의 증거가 아닙니다. Windows/WSL 기록을 native Ubuntu 설치로 대체하지 않습니다. private overlay가 있으면 그 저장소의 Ubuntu handoff와 pin 검사를 별도로 따릅니다.

확인 항목: Ubuntu/kernel/아키텍처, sudo 가능 여부, CPU/RAM, GPU/VRAM/드라이버·활성 프로세스, 디스크 공간/inode, SSH·VPN·desktop/display manager, 기존 Python/uv/Conda·ROS·Isaac·Docker 환경과 lock. 필요한 항목만 읽고 인증 파일·전체 환경변수는 출력하지 않습니다.

기존 정상 환경은 보존합니다. OS 재설치·배포판 업그레이드·전체 apt upgrade·드라이버 purge·디스크 포맷·새 마운트는 하지 않습니다. 누락된 도구와 변경 명령을 먼저 제시하고 권한은 정상 절차로 요청합니다. 승인된 설치부터 기록 폴더를 만들며 백업과 실제 접속 정보는 사용자만 읽게 합니다.

## 2. 기본 도구와 Codex

현재 설치와 비교해 필요한 패키지만 대상 Ubuntu에서 확인·설치합니다. 기본 후보는 `openssh-server tmux git rsync curl ca-certificates unzip jq ripgrep python3-venv`입니다. `git-lfs`, `build-essential`, `pkg-config`, `pciutils`, `ubuntu-drivers-common`은 선택한 프로젝트나 진단에 필요할 때 추가합니다. 시스템 Python을 교체하거나 `sudo pip`를 쓰지 않습니다.

uv가 없으면 [공식 사용자 범위 설치](https://docs.astral.sh/uv/getting-started/installation/)를 사용합니다. 기존 Conda 프로젝트를 uv로 변환하지 않습니다. 로그인 셸과 비대화형 SSH에서 PATH가 동작하는지 확인합니다. 전역 Git 계정·remote를 변경하지 않습니다.

Codex는 [공식 설치와 원격 인증](index.md#codex-bootstrap)을 따르고 버전·로그인 상태를 확인합니다. 모델·MCP·skills·관리자 정책을 복제하거나 덮어쓰지 않습니다. WS에 VS Code 데스크톱이나 code-server를 일괄 설치하지 않습니다.

## 3. OpenSSH와 네트워크

1. 기존 SSH 포트와 설정을 보존하고 누락된 OpenSSH만 설치합니다. 대상 Ubuntu의 service/socket 구성을 확인해 부팅 시 활성화합니다. `sudo sshd -t`로 문법을 확인한 뒤 필요한 reload만 수행합니다. 기존 연결은 새 연결 검증까지 유지합니다.
2. MacBook 공개키를 받으면 대상 계정의 `authorized_keys`에 중복 없이 추가합니다. 기존 키는 지우지 않습니다. 키가 없으면 등록만 `NEEDS_INPUT`으로 남기고 독립된 설치를 계속합니다.
3. root 로그인·암호 인증을 새로 완화하지 않습니다. 키 접속 검증 전에 기존 암호 인증을 끄지 않습니다. 방화벽은 실제 신뢰 LAN/VPN 또는 `tailscale0`의 필요한 포트만 허용합니다. UFW reset/disable, 접근 경로 확인 없는 신규 활성화, 공유기 포트 포워딩은 하지 않습니다.
4. 기존 LAN/VPN이 충분하면 유지합니다. 필요하고 허용될 때만 [Tailscale Linux](https://tailscale.com/docs/install/linux)를 설치하고 부팅 서비스를 확인합니다. 사용자가 인증하며 tailnet/ACL/exit node/subnet 설정은 보존합니다. 기본은 **OpenSSH over Tailscale**이며 `tailscale up --ssh`를 자동 적용하지 않습니다. 두 WS의 장치 이름·주소를 구분하고 재인증·키 만료 조건을 기록합니다.
5. 사용 중인 SSH 공개 호스트키 파일의 SHA256 지문을 `ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub -E sha256` 등으로 확인합니다. 해당 키가 실제 활성인지 확인하고, 다르면 실제 공개키 파일로 바꿉니다. 개인 호스트키 파일은 읽지 않습니다.

로컬 `CLIENT-CONNECTION.md`에 접속 정보·공개 지문·프로젝트/Python 경로를 남깁니다. MacBook의 실제 연결 전에는 `SSH_READY=PENDING: CLIENT_TEST_PENDING`입니다. 팀원은 본인 계정과 키를 사용합니다. 관리 네트워크 접속이 로봇 NIC·ROS DDS discovery를 외부에 여는 이유가 되지 않습니다.

## 4. GPU 드라이버와 환경 선택

RTX 5090을 기대하더라도 실제 `nvidia-smi` 결과부터 확인합니다. 다른 GPU면 모델과 차이를 기록하고 5090 통과라고 쓰지 않습니다. 정상 드라이버를 최신이라는 이유로 교체하지 않습니다. 드라이버 변경이 필요한 경우에만 [Ubuntu 절차](https://ubuntu.com/server/docs/nvidia-drivers-installation/)와 [NVIDIA kernel module 지원](https://docs.nvidia.com/datacenter/tesla/driver-installation-guide/kernel-modules.html)을 확인해 해당 GPU에 맞는 패키지와 rollback을 제시합니다. Blackwell은 open kernel module 계열을 사용합니다. `.run`과 APT를 혼용하지 않고 Secure Boot/MOK가 필요한지 먼저 확인합니다. 근거 확인: 2026-10-01, 실행 당일 재확인.

`nvidia-smi`의 CUDA 표시는 드라이버 지원 수준입니다. PyTorch wheel의 CUDA runtime, 컴파일용 CUDA Toolkit과 구분합니다. 커스텀 CUDA extension 빌드가 필요하지 않으면 전체 Toolkit은 기본 설치하지 않습니다.

환경은 다음 순서로 선택합니다.

1. 기존 프로젝트의 README·환경 기록·lock을 조사하고 해당 관리 방식으로 재사용합니다. 튜토리얼 Core의 Python 3.12 `.venv`에 GPU 패키지를 덧붙이지 않습니다.
2. `gpu-mjlab`, `gpu-lerobot`, vendor/modern Isaac은 별도 환경으로 유지합니다. Isaac·ROS·Docker가 이미 있으면 보존하며 이번 SSH 설치 때문에 다시 설치하지 않습니다.
3. GPU 검증용 환경도 없으면 기록 폴더 아래 `gpu-smoke/`에 독립 uv 프로젝트를 만듭니다. Python 후보는 3.12이며 선택한 PyTorch가 지원하는 버전을 확인합니다. 기존 저장소의 lock은 바꾸지 않습니다. 최소 패키지는 CUDA `torch`; 프로젝트가 필요로 할 때만 호환 `torchvision`, Jupyter/TensorBoard 등을 추가합니다.
4. [PyTorch 공식 설치](https://pytorch.org/get-started/locally/)에서 GPU 아키텍처·드라이버·Python·프로젝트 요구를 함께 대조합니다. [2.7의 Blackwell/CUDA 12.8 도입](https://pytorch.org/blog/pytorch-2-7/)은 역사적 기준이며 고정 설치 버전이 아닙니다. 오래된 wheel이나 nightly 안내를 그대로 복사하지 않습니다.
5. 새 uv 환경은 [공식 PyTorch index 구성](https://docs.astral.sh/uv/guides/integration/pytorch/)에 따라 이름 있는 CUDA index와 `explicit = true`, `tool.uv.sources`를 사용합니다. 선택한 실제 URL·정확한 버전을 기록하고 그 독립 프로젝트에서 `uv lock`, `uv sync --locked`, `uv pip check`를 실행합니다. 호환되지 않는 기존 환경은 보존하고 별도 환경에서 원인을 분리합니다.

큰 모델·데이터·Isaac/ROS 배포판·컨테이너는 해당 작업이 필요하고 설치 요청에 포함될 때만 준비합니다. 문서만 읽고 자동 설치하지 않습니다. 프레임워크 환경 사이에 `.venv`를 복사하지 않습니다.

## 5. 실제 GPU와 checkpoint 시험

선택한 환경의 Python으로 기록 폴더 아래 시험 스크립트를 작성·실행합니다. 다른 GPU 작업의 메모리·부하를 확인하고 작고 짧은 합성 입력만 사용합니다. GPU가 없으면 `NOT_APPLICABLE`; 사용 중이라 안전하게 실행할 수 없으면 `PENDING`입니다.

1. Python 경로, torch/CUDA runtime 버전, 실제 장치 이름·capability·index/UUID를 로컬 결과에 기록합니다. `torch.cuda.is_available()`를 확인하고 model/tensor의 CUDA 장치도 확인합니다.
2. 작은 CUDA 행렬곱과 Conv2d → loss → backward → optimizer.step을 FP32로 실행합니다. `torch.cuda.synchronize()`로 비동기 오류를 확인하고 loss/gradient가 finite이며 파라미터가 바뀌었는지 검사합니다. CPU fallback과 `no kernel image`를 성공 처리하지 않습니다.
3. 지원되면 BF16 autocast에서도 검사합니다. 미지원이면 이유를 남기고 FP32와 구분합니다. 작은 합성 DataLoader 및 설치된 경우 torchvision의 실제 필요한 연산도 확인합니다. 아키텍처 문자열 하나의 존재만으로 호환성을 판정하지 않습니다.
4. 첫 프로세스에서 model·optimizer·step·사용한 RNG 상태를 저장하고 종료합니다. 두 번째 프로세스에서 직접 만든 checkpoint를 로드하여 step 증가와 파라미터 갱신을 확인합니다. 파일 로드만 성공한 것을 학습 재개로 보고하지 않습니다.
5. 결과를 `gpu-smoke-result.json`과 로그에 저장합니다. 이후 의존성이 바뀌면 영향받은 환경을 재검증합니다. 컨테이너 작업이라면 컨테이너 내부에서도 시험해야 합니다.

이 시험은 GPU 기반 연산·재개만 검증합니다. ROS는 해당 lesson의 DDS/record-replay, Isaac은 설치 버전에 맞는 공식 smoke와 예제, mjlab/LeRobot은 해당 작업 검증이 따로 필요합니다. 라이선스/EULA를 사용자가 검토하기 전에 수락하지 않습니다.

## 6. 지속 실행과 결과 확인

위 표의 tmux 세션을 사용합니다. 합성 로그 작업으로 detach, SSH 단절, 재접속을 실제 시험합니다. logind 정책 때문에 작업이 종료되면 원인을 기록하고 무조건 정책을 완화하지 않습니다. WS 재부팅 시 tmux는 종료됩니다.

launcher는 실제 working directory·Python·GPU 선택·고유 run 폴더·unbuffered 로그·실패 exit code를 보존해야 합니다. 존재하지 않는 `train.py`를 실행 명령으로 적지 않습니다. 학습의 checkpoint에는 사용하는 optimizer/scheduler/scaler/RNG 상태를 보관하고 가능하면 임시 파일 후 atomic rename으로 저장합니다. 부팅 후 학습·로봇 제어 자동 재시작은 기본으로 켜지 않습니다.

Jupyter/TensorBoard가 필요하면 선택 환경에만 준비하고 [MacBook 포트 전달](macbook.md)을 따릅니다. loopback 바인딩과 Jupyter 인증을 유지합니다. 데이터·checkpoint·GPU UUID·실제 주소는 Git에서 제외하며 전체 데이터 복제는 별도 요청 사항입니다.

## 7. 선택 GUI

기존 Ubuntu Desktop과 원격 GUI가 있으면 먼저 시험하고 유지합니다. desktop이 없으면 이 작업만을 위해 GNOME을 설치하지 않으며 `GUI_READY=NOT_APPLICABLE: desktop absent`로 기록합니다.

NoMachine이 필요하면 공식 아키텍처별 패키지와 라이선스를 확인합니다. 현재 v10 서버는 평가/구독 라이선스가 필요하고 클라이언트는 무료입니다. 구매·구독·라이선스 동의를 대행하지 않습니다. [공식 조건, 확인 2026-10-01](https://kb.nomachine.com/AR03P00972). 라이선스 대기 중에도 SSH 준비는 계속합니다.

실제 서비스·포트(기본 NX 4000)를 확인하고 신뢰 네트워크 범위만 허용합니다. UPnP를 켜지 않습니다. X11/Wayland를 먼저 시험하며 display manager 전환·재시작이나 자동 로그인을 기본 해결책으로 쓰지 않습니다. MacBook에서 화면·입력을 확인하고 로그인 전·잠금·모니터 제거는 각각 시험합니다. GPU 렌더링은 별도 검증합니다. 무료 GUI가 명시적으로 필요하면 [Ubuntu Remote Login과 Desktop Sharing](https://documentation.ubuntu.com/desktop/en/24.04/how-to/share-your-desktop-remotely/)의 차이를 확인해 선택하며 여러 RDP 서버를 같은 포트에 설치하지 않습니다.

## 8. 재부팅과 복구

재부팅 전 현재 작업과 세션, 변경 이유·영향, `cat /proc/sys/kernel/random/boot_id` 결과, SSH/VPN 부팅 설정, 로그인 전 네트워크·절전 정책을 확인합니다. 장시간 무인접속을 위해 필요하면 AC 자동 suspend만 조정하고 화면 잠금은 유지합니다. 모든 전원 target을 mask하지 않습니다.

디스크 암호 해제·Secure Boot MOK 입력·부팅 장애에 현장/BMC/PiKVM 경로가 필요한지 확인합니다. 필요한데 접근 수단이 없다면 재부팅을 보류합니다. BIOS·암호화·Secure Boot를 임의 변경하지 않습니다. SSH 변경 후에는 별도 새 연결이 성공해야 합니다.

`RESUME.md`에 완료 단계, 백업·복구 명령, 재접속 주소, 다음 GPU 시험 명령과 가이드 경로를 남깁니다. 영향과 복구 경로를 제시한 뒤 아직 승인되지 않은 재부팅만 승인받습니다. 이미 승인된 같은 재부팅을 다시 묻지 않습니다. 현재 Codex 세션이 종료될 수 있으며 자동 재접속을 약속하지 않습니다.

재부팅 후 같은 가이드를 다시 읽고 boot ID 변경, 현지 로그인 없는 MacBook SSH·VS Code 접속, `nvidia-smi`, 같은 환경의 GPU/checkpoint 시험을 확인합니다. GUI는 별도로 확인합니다. 실제 학습은 checkpoint를 확인한 후 수동 재개합니다. 미시험이면 `REBOOT_UNTESTED`, 서버 측만 확인했으면 `CLIENT_TEST_PENDING`을 유지합니다.

## 9. 결과와 다음 작업

[공통 결과 형식](index.md#records-and-acceptance)으로 기록하고 MacBook에 `CLIENT-CONNECTION.md`만 안전하게 전달합니다. 입력 부족·다른 GPU·선택 GUI·재부팅 미시험을 각각 구분합니다. 새 기록은 과거 성공이나 다른 호스트의 상태를 덮어쓰지 않습니다. 설치가 끝나도 lesson finish나 하드웨어 명령을 자동 실행하지 않습니다.

원격 개발을 넘어 로봇 실행으로 전환할 때는 학습 작업을 정리하고 별도 runtime 환경·격리 네트워크·검증된 bundle·read-only 검사·현재 실행 승인을 확인합니다. SSH 권한은 모션 권한이 아닙니다.
