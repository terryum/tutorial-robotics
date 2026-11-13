<!-- pal:language:start -->
<p align="right">
  <a href="vr-teleop.md" lang="ko">한국어</a> | <a href="../../en/setup/vr-teleop.md" lang="en">ENGLISH</a>
</p>
<!-- pal:language:end -->

# Ubuntu VR 텔레오퍼레이션 설치·검증

WS2 Ubuntu는 Quest 3 시점·표시·컨트롤러, MANUS 손가락, VIVE 손목 입력과
시뮬레이션·수집·학습의 기본 환경입니다. Mac은 입력 계약·좌표 변환·재생·품질 검사·
소형 MuJoCo 예제를 지원합니다. Windows는 제조사 설정·복구용 선택 경로이며 상시
입력 서버가 아닙니다. 기존 VR 없는 기초 수업과 Isaac·CloudXR·MANUS 환경을 보존합니다.

## VIVE Linux 베타 설치

[공식 Hub v1.0.3 beta](https://github.com/ViveRoboticsSoftware/vivehub-linux/releases/tag/v1.0.3)의
x86_64 archive SHA256은 `4bd87a7d7cb7d580a8dce0a5b2b5d4c32c1bd44822fec4a7bbf5971da277bc07`입니다.
배포 checksum을 검증한 뒤 ignored `.local/vendor/vivehub-1.0.3/`에 격리 압축 해제합니다.
`LICENSE.txt`·`ThirdPartyLicenses.txt`와 HTC EULA를 먼저 검토합니다. 기존 NVIDIA
동의는 HTC 동의가 아닙니다. 동의 전 Hub·SDK 실행이나 udev·장치 설정을 하지 않습니다.
현재 개발 상태는 checksum 검증·격리 압축 해제뿐이며 약관 동의·실제 입력은 대기입니다.
고정 URL·hash·프로토콜 판정은 `setup/vr-input-lock.json`에 있습니다.

[공식 Hub 구조](https://github.com/ViveRoboticsSoftware/vivehub-linux)에 따라
`run-vivehub.sh`로 실행하고 Hub가 tracker_server를 관리하게 합니다. 수집기가 두 번째
server를 띄우면 안 됩니다. Hub는 Linux 페어링·맵 생성·tracker IPC를 제공하지만 Quest
HMD를 지원하는 프로그램은 아닙니다. 포함 SDK는 `/tmp/vut.sock`, protocol 1,
12-byte `<BBHII` header, HELLO/ACK, READY=2를 사용합니다. 좌표는 HTC/OpenVR 오른손
좌표계의 m, quaternion xyzw입니다. 수집기는 pose/status HELLO 구독만 전송하며
페어링·전원·reset·setup 명령을 제공하지 않습니다. serial은 로컬 원시 증거에만 둡니다.

[standalone SDK](https://github.com/ViveRoboticsSoftware/vive-ultimate-tracker-sdk)의
후보 revision `8685112780734c2513c66d53b9eb104db47afcf9`는 `/tmp/vive_tracker.sock`,
16-byte `<IBB10s` header, READY=8을 사용합니다. **Hub v1.0.3 포함 SDK와 wire 호환되지
않습니다.** 해당 Python reference client를 그대로 연결하거나 standalone server를 Hub와
함께 실행하지 않습니다. `pai_lab.vive_ipc`는 Hub 형식을 사용하며 분할 패킷의 나머지를
blocking으로 기다리지 않습니다. 소프트웨어 socketpair 테스트는 실제 daemon 호환성
검증을 대신하지 않습니다.

## 입력과 공간 보정

1. Quest: 기존 CloudXR/Isaac 환경에서 읽기 전용으로 시점·컨트롤러·timestamped
   clutch/deadman 해제를 확인합니다. Quest-only 모드는 명시적으로 선택하며
   integrated 입력 손실 때 자동 fallback하지 않습니다.
2. MANUS: 실제 모델·firmware·Linux SDK와 Integrated 권한부터 확인하고 공식
   printer/plugin stream을 사용합니다. 관절 이름을 명시하고 원시 시각·clock·추적 상태를 보존합니다.
3. VIVE: 별도 HTC 검토 뒤 누락 USB 권한·의존성만 적용합니다. Hub에서 페어링·Linux 맵
   생성을 하고 좌우 tracker를 로컬로 지정합니다. tracker_from_wrist 장착 변환과
   Quest 공간에 대한 world_from_device 정합을 정지·기지 이동으로 검사합니다.
   Windows 보정값을 Ubuntu에서 그대로 사용하지 않습니다.
4. `InputMux`는 읽기 전용 `DeviceSample`을 받습니다. 보정 SE3 행렬·ID를 명시합니다.
   장치 원시 clock은 증거이며 freshness는 해당 호스트 monotonic 수신 시각으로 계산합니다.
   캐시된 입력에 새 수신 시각을 붙이지 않습니다. 재연결은 새 session입니다. 통합 모드에서는
   Quest 스위치, MANUS 양손, VIVE 양손이 모두 fresh해야 합니다.

## 검증 기준

각 장치별·동시 입력을 최소 60초 측정합니다. `pai_lab.teleop_sources.rate_report`로
수신율·최대 간격·tracking 유효율을 기록하고 정지·움직임·가림·해제·재연결을 확인합니다.
수신 callback과 별도로 sink를 poll합니다. 마지막 유효 입력 후 정확히 100 ms에서 hold로
잠기며 두 스위치 해제 → 로컬 재무장 → fresh press 전에는 재개하지 않습니다. 실제
controller는 수집기 process가 멈춘 경우에도 자체 watchdog을 유지해야 합니다.

로봇별 저장 에피소드 3개와 폐기·중단 사례, 원시 입력·적용 목표·실제 상태·카메라의 시각
및 좌표·관절 이름 대응을 검사합니다. 기존 파일을 덮어쓰지 않고 중단 기록은 보존합니다.
재로드·hash 검증 후 전체 에피소드 단위로 분할합니다. 합성 데이터는 사람 시연이 아닙니다.
설치·소프트웨어 검사·실제 입력·시뮬레이션 성능·실물 동작을 별도로 판정합니다.

## 수업 경로

[core-teleop-01](../lessons/core-teleop-01.md) →
[sim-teleop-01](../lessons/sim-teleop-01.md) →
[sim-teleop-02](../lessons/sim-teleop-02.md) →
[sim-enlight-06](../lessons/sim-enlight-06.md).
실기 보정이 대기여도 sim-teleop-02의 오프라인 검사는 독립적으로 실행할 수 있으나
sim-teleop-01 완료로 인정하지 않습니다. Enlight는 자체 모델·6DoF IK·관절 한계를 쓰며
팔 전용 BC 수집을 제공합니다. 그리퍼 집기·이송은 검증 후 엽니다.

## 현재 검증 상태와 실기 명령

native Ubuntu WS2에서 archive 무결성과 SDK 프로토콜 불일치를 확인했습니다.
USB Quest/MANUS/VIVE는 없었습니다. HTC 검토, native SDK 연결, MANUS 권한·firmware,
맵·장착 변환·정합, 동시 60초와 사람 시연은 대기입니다. MuJoCo 후 기존 정상 Isaac
환경에서 확장을 검증하고 Lab 의존 수업만 별도 환경을 구성합니다.
개인 수업 완료나 실물 권한은 생성하지 않았습니다.

HTC 약관을 실제로 검토한 operator만, Hub daemon 실행 후 아래 읽기 전용 수집을 실행합니다.
개발 setup은 동의 flag를 자동 전달하지 않습니다. 출력은 로컬에 보존합니다.

```bash
python -m pai_lab.vive_ipc --htc-eula-reviewed --duration 61 --output-dir .local/vive-input-unique
```
