<p align="right"><a href="../../ko/setup/aloha.md">한국어</a> | <a href="../../en/setup/aloha.md">ENGLISH</a></p>

# ALOHA — Setup 검토

**검증 상태: 모든 실물 단계는 `reader_test_required`.** 이 안내는 모델별 설치 검토를 준비하기 위한 문서입니다. 시뮬레이션 모델로 보유 장비를 식별하지 마세요. 실물 모델·좌우·리비전·펌웨어·컨트롤러·SDK는 로컬에 기록하고 일련번호·주소·보정값은 Git에서 제외합니다.

실물 작업 전 [하드웨어 안전](../../07_SAFETY.md)을 읽으세요. 해당 매뉴얼, 제조사 지정 고정구와 전원, 보호 접지, 정지 장치, 격리 네트워크, 작업자를 준비합니다. 설치·보정·제어 활성화·동작은 장비별 절차와 해당 실행 승인이 필요합니다. 아래 명령은 합성 데이터만 검사합니다.

## 조립 전에 키트 선택

Trossen **2.0 문서**는 Interbotix Stationary·Mobile·Solo 키트용입니다. Trossen AI Arms는 별도 문서를 사용하라고 명시합니다. 과정의 Menagerie **ALOHA 2 시뮬레이션**과도 구분해야 합니다. ALOHA라는 이름이 같아도 팔·카메라·배선·소프트웨어가 같지는 않습니다.

구성에 맞는 **Getting Started → Hardware Setup**을 먼저 검토합니다. Stationary는 테이블/프레임 고정, leader WidowX와 follower ViperX 배치, 풀리·중력 보상 장치, 카메라 장착과 배선이 필요합니다. Mobile은 자체 베이스·컨트롤러 설정이 있으며 Solo는 leader/follower 팔 한 쌍입니다. 해당 키트 전원과 허브를 준비하고 배선·전원 투입 전에 팔과 카메라를 로컬에서 개별 식별합니다. 다른 현장의 일련번호 기반 udev 규칙을 복사하지 않습니다.

## 소프트웨어와 상태 확인

수집한 Stationary 2.0 설치 안내는 native Ubuntu 22.04 / ROS 2 Humble을 지정합니다. Interbotix 2.0의 수집·텔레오퍼레이션 지원과 ACT/ACT++ 학습 호환성은 별개이며, 문서는 해당 학습 흐름에 1.0을 안내합니다. 선택한 branch/commit·ROS 배포판·학습/데이터 어댑터 명세를 명시합니다. 코드 참조 목록의 커밋은 소스 검토 기준이며 모든 branch가 설치 안내와 일치한다는 의미가 아닙니다.

**Post-Install Hardware Setup**에서 leader/follower별 장치명·카메라 식별을 확인하고 **Bringup & Shutdown**에서 실물 절차를 검토합니다. bringup·텔레오퍼레이션·녹화·재생은 토크를 켜거나 팔을 움직일 수 있습니다. 오프라인 명령은 이 작업들을 실행하지 않습니다.

## 에피소드와 카메라 시각 정렬

공식 **Data Collection → Dataset Format**은 HDF5 에피소드를 설명합니다.

| 구성 | qpos / qvel / action | 카메라 | 추가 action |
|---|---|---|---|
| Stationary | 각각 14 | high, low, 좌우 wrist | 없음 |
| Mobile | 각각 14 | high, 좌우 wrist | base_action: 2 |
| Solo | 각각 7 | high와 해당 wrist | 없음 |

합성 예제는 Stationary를 명시적으로 선택합니다. 팔 2개 × (관절 6개 + 정규화 gripper 1개) = 14입니다. 현재 시뮬레이션은 각 gripper의 두 finger 좌표 때문에 `nq=16`, `nu=14`입니다. 모델 qpos 길이와 데이터셋 action 길이를 같다고 보면 안 됩니다. 합성 데이터의 rad/정규화 단위와 카메라별 시각은 교육용 메타데이터이며 모든 HDF5 파일에 존재한다는 뜻은 아닙니다. HDF5·LeRobot 변환 전 실제 gripper 정규화·프레임률·카메라명·시각 출처를 확인합니다. 행 번호가 같다고 동기화가 입증되지는 않습니다.

## 오프라인 실행과 복구

합성 행 2개, qpos/action 각 14개, 카메라 4개의 정렬을 확인합니다. 예제의 10 ms 허용치는 설명용입니다. 차원 오류·카메라 누락·역전되거나 어긋난 시각·format 변경은 실패해야 합니다. 데이터 명세나 수집 시각을 점검하고, 데이터 형태를 진단하려고 실물 로봇에서 재생하지 않습니다.

## 출처

- [Interbotix ALOHA 2.0](https://docs.trossenrobotics.com/aloha_docs/2.0/index.html): 구성별 하드웨어·소프트웨어 설치.
- [데이터 수집·에피소드 형식](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/data_collection.html).
- [Interbotix ALOHA](https://github.com/Interbotix/aloha): 고정 `scripts/record_episodes.py`, `aloha/real_env.py`, `aloha/constants.py`; 기존 LeRobot·Menagerie pin 유지.

## 합성 검사 실행

```bash
python -m pai_lab.manual_examples aloha
```

[매뉴얼 자료실과 검증 방법](index.md). 이 검사는 장비 준비 상태나 개인 학습 기록을 갱신하지 않습니다.
