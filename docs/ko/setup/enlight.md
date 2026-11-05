<p align="right"><a href="../../ko/setup/enlight.md">한국어</a> | <a href="../../en/setup/enlight.md">ENGLISH</a></p>

# Enlight — Setup 검토

**검증 상태: 모든 실물 단계는 `reader_test_required`.** 이 안내는 모델별 설치 검토를 준비하기 위한 문서입니다. 시뮬레이션 모델로 보유 장비를 식별하지 마세요. 실물 모델·좌우·리비전·펌웨어·컨트롤러·SDK는 로컬에 기록하고 일련번호·주소·보정값은 Git에서 제외합니다.

실물 작업 전 [하드웨어 안전](../../07_SAFETY.md)을 읽으세요. 해당 매뉴얼, 제조사 지정 고정구와 전원, 보호 접지, 정지 장치, 격리 네트워크, 작업자를 준비합니다. 설치·보정·제어 활성화·동작은 장비별 절차와 해당 실행 승인이 필요합니다. 아래 명령은 합성 데이터만 검사합니다.

## 준비와 설치 검토

제공된 **Enlight Series User Manual V0.1**을 해당 Orion 컨트롤러 및 Aegis 안전 문서와 함께 사용합니다. 시리즈 매뉴얼이 컨트롤러 문서를 대신하지 않습니다.

| 검토할 작업 | 필요한 확인 근거 | 출처 |
|---|---|---|
| 기초·볼트·인양·베이스 평탄도 확인 | 안정된 지지와 해당 설치 도면 | V0.1 §4.3.2–4.3.3, 인쇄 쪽수 26–29 |
| 컨트롤러를 통한 접지 확인 | 올바른 연결과 보호 접지 방식 | §4.3.3.1.5 29쪽; Orion 필요 |
| 설치 방향과 중력 방향 대조 | Elements Robot Installation이 바닥·역방향·경사 설치와 일치 | §4.3.4 29–30쪽 |
| 툴 질량·무게중심·관성 검토 | 툴 전체와 작업물을 포함한 하중 정의 | §4.3.5 30–32쪽 |
| 전원 연결 전 케이블·커넥터 검토 | 당김·끼임·커넥터 불일치 없음 | §4.4 33–36쪽; Orion 필요 |

**미해결 베이스 체결 토크 불일치:** V0.1 인쇄 27쪽은 36 Nm, 29쪽은 22 Nm, 41쪽은 32 Nm이며 각각 ±10%입니다. Flexiv에 적용 볼트·설치 리비전·정정값을 확인해야 합니다. 이 안내는 실행할 베이스 토크를 지정하지 않습니다. PDF 뷰어의 페이지 번호와 인쇄 쪽수는 다릅니다.

## 소프트웨어와 상태

**Enlight-L / Software Package v3E.1 / RDK Professional** 설치 조합은
[RDK v2.1](https://github.com/flexivrobotics/flexiv_rdk/releases/tag/v2.1)
(`bfab04f4e385ca335ee3025bfefe70249b015578`)과 독립 Python 3.12 환경의
`flexivrdk==2.1.0`입니다. 공식 wheel은 macOS arm64·Linux x86_64를 지원합니다.
전체 커밋·패키지 SHA256·라이선스를 잠그고 재현 시 이동 가능한 태그를 다시 따라가지 않습니다.

고정 [ROS 매니페스트](https://github.com/flexivrobotics/flexiv_ros2/blob/a165e88a2b41cb7e09b46aa1bfb842718ee783b1/flexiv.jazzy.repos)는
ROS `jazzy-v2.1` (`a165e88a2b41cb7e09b46aa1bfb842718ee783b1`)과 description
`jazzy-v2.1` (`54593cda75bac0251567a13db3d6862da7fe7cfb`)을 연결합니다.
다만 description README는 소프트웨어 **v4**를 명시하므로 실제 v3E.1 관절·프레임·한계
호환성을 Flexiv에 확인한 뒤 실물에 사용합니다.

공개 교육용 description `77dd8d8ec4c48a06778ac3886569c9d24e7a977a`와
소스 검토용 RDK `ff92fe421e19daee6cdf27794a332c8fef7cf831`는 유지합니다.
교육용 리비전과 v3E.1 운영 조합을 구분합니다. 수업 ID를 유지하고, 대체 모델은 관절 7개의
순서·축·한계·관성·프레임·렌더링과 독립 FK 오차 `1e-9 m` 미만을 검증한 뒤 반영합니다.
회사 설치파일·현장 설정·장비 고유 모델은 비공개로 보관합니다.

### 앱·연결·복구 순서

1. Teach Pendant **Elements**에서 설치 방향·중력·툴 하중·정지 장치·수동 Jog 절차와
   Remote Mode를 먼저 검토합니다. 실물 변경·Jog에는 해당 절차와 새 승인이 필요합니다.
2. v3E.1 호환 Ubuntu **Elements Studio** 패키지는 Flexiv에 요청하고 버전·해시를 로컬에 기록합니다.
   [공식 설치 안내](https://github.com/flexivrobotics/flexiv_sim_plugin/blob/v2.x/docs/elements_studio_setup.md)를 따릅니다.
3. Mac은 독립 SDK import·오프라인 모델·원격 개발, Ubuntu 24.04/Jazzy는 첫 유선 실물 연결·C++·ROS에 사용합니다.
   로봇 LAN과 원격 접속망을 구분하고 초기 명령 송신자는 하나로 제한합니다.
4. import → 오프라인 replay → 명령 없는 상태 조회 → 별도 승인된 비실시간 단일 동작
   → 필요한 경우 실시간 제어 순서로 진행합니다. Professional만으로 실시간 커널이 필요하지 않습니다.
5. 공식 ROS 드라이버는 먼저 `use_fake_hardware:=true`로 검사합니다.
   `sim-enlight-01` 교육용 DDS/MuJoCo 어댑터와 별도 검사이며 어느 쪽도 실물 준비 완료를 입증하지 않습니다.
   호스트 접속·패키지가 없으면 대기로 남깁니다.

읽기 전용 조회는 `ARM_1`·관절 7개 순서·rad/rad/s/N·m와 장비·수신 시각을 보존합니다.
빈 값·NaN·범위 초과·단절과 오래된·미래·정지한 장비 시각을 거부합니다.
오래된 장비 시각을 수신 시각으로 갱신하지 않습니다. `operational=False`만으로 서보 꺼짐을
입증할 수 없으므로 명시적 disabled 근거가 필요합니다. 조회 전후 Elements의 서보·fault 상태를 대조합니다.
실패하면 중단 후 제조사 복구 절차를 따르며, 상태 조회에서 ClearFault·ServoOn·모드 변경·동작을 호출하지 않습니다.

snapshot은 ignored `.local/`에 저장하고 조회 직후
`pal hardware preflight enlight --snapshot <local-snapshot.json> --read-only --json`으로 검사합니다.
오래된 snapshot은 freshness 검사에서 실패해야 합니다. 매 동작 전 정확한 로봇·동작·한계·명령 확인·timeout·
stale-state watchdog·독립 정지 경로를 새 실행 카드에 명시한 뒤 별도 승인을 받습니다.

외장 SSD는 **x86_64 PC용 Ubuntu 24.04 amd64**·SSD 자체 EFI/Ubuntu 파티션·동일 의존성 잠금을 사용합니다.
파티션 작업 전 대상 디스크와 백업을 확인합니다. PC마다 유선 NIC·드라이버·격리 경로·지연을 재검사합니다.
Apple Silicon 부팅용이 아니며 이번 설치에는 펌웨어·커널·GPU 변경을 포함하지 않습니다.

V0.1 §4.5.1 37쪽의 표시등은 노랑=전원 켜짐/서보 꺼짐, 흰색=서보 켜짐/정지, 초록=프로젝트 실행, 파랑=Freedrive, 빨강 점등/점멸=일반/치명적 fault, 주황=복구 상태입니다. 컨트롤러 상태도 함께 읽어야 하며 표시등만으로 준비 완료를 판단하지 않습니다.

보정 검토: §6.2 51쪽은 관절 토크 센서, §6.3 52–53쪽은 바닥 설치 및 TCP 고정을 전제로 한 기구학 모델 검증, §6.4 54–55쪽은 동역학 보정입니다. 팔을 움직이거나 컨트롤러 값을 바꿀 수 있는 절차입니다. 해당 Orion/Aegis 문서와 실행 승인을 갖춘 뒤 수행해야 합니다. 메뉴를 열었다는 사실은 보정 완료 근거가 아닙니다.

## 오프라인 실행과 복구

아래 명령은 관절값 7개, rad·rad/s·N·m 단위, base/TCP 좌표계, 최신 합성 수신 시각을 검사합니다. 교육용 데이터는 위치를 m, 쿼터니언을 `wxyz`로 정규화하며 RDK 원시 패킷과는 다릅니다.

고정한 `example_py/basics1_display_robot_states.py`는 상태 출력 전에 **`ClearFault()`와 `ServoOn()`**을 호출합니다. 파일명만 보고 읽기 전용으로 판단하지 마세요. 이 예제는 해당 파일을 import하지 않습니다. 단위·좌표계·시각 오류가 나면 합성 데이터의 명세부터 바로잡습니다. 실물 fault는 자동 해제하지 말고 제조사 복구 절차를 따릅니다.

## 출처

- 로컬 `enlight-v01`; 위 인쇄 쪽수는 제공 원본과 대조했습니다.
- [Flexiv RDK 매뉴얼](https://www.flexiv.com/software/rdk/manual/v2.x/index.html): 소프트웨어 호환성, 상태 필드, 오류 처리.
- [Flexiv 자료실](https://www.flexiv.com/download?type=User+Manuals), [Flexiv Hub](https://hub.flexiv.com/login): 미확보 Elements·Orion·Aegis·Enlight Quick Start의 해당 리비전 요청 경로.

## 합성 검사 실행

```bash
python -m pai_lab.manual_examples enlight
```

[매뉴얼 자료실과 검증 방법](index.md). 이 검사는 장비 준비 상태나 개인 학습 기록을 갱신하지 않습니다.
