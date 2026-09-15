<p align="right"><a href="../../ko/setup/wuji.md">한국어</a> | <a href="../../en/setup/wuji.md">ENGLISH</a></p>

# Wuji Hand 2 Beta 2 — Setup 검토

**검증 상태: 모든 실물 단계는 `reader_test_required`.** 이 안내는 모델별 설치 검토를 준비하기 위한 문서입니다. 시뮬레이션 모델로 보유 장비를 식별하지 마세요. 실물 모델·좌우·리비전·펌웨어·컨트롤러·SDK는 로컬에 기록하고 일련번호·주소·보정값은 Git에서 제외합니다.

실물 작업 전 [하드웨어 안전](../../07_SAFETY.md)을 읽으세요. 해당 매뉴얼, 제조사 지정 고정구와 전원, 보호 접지, 정지 장치, 격리 네트워크, 작업자를 준비합니다. 설치·보정·제어 활성화·동작은 장비별 절차와 해당 실행 승인이 필요합니다. 아래 명령은 합성 데이터만 검사합니다.

## Beta 2 식별과 설치 준비

**Version Identification and Compatibility**로 Beta 2를 로컬에서 식별합니다. 제조사가 안내하는 하드웨어 리비전 표식을 확인하되 일련번호를 공개하지 않습니다. 좌우에 맞는 장착면, 케이블 고정, **11–13 V DC** 전원과 XT30 전원/RJ45 통신 케이블을 준비합니다. **Hardware Integration → Power Supply**는 200 W 이상, 제공 어댑터는 12 V 20 A로 설명합니다. 전원 차단 상태에서 극성과 배선을 확인하고 작동 중 연결·분리하지 않습니다. **Palm Mounting Interface**, **Coordinate Frames and Models** 절로 기계 설치를 검토합니다.

저장소 프로필은 펌웨어 v2.6.0·SDK v2026.8.31을 기록합니다. 수집한 호환성 페이지는 여전히 v2.5.1을 현재 버전으로 표기하며 펌웨어/SDK 릴리스 노트 대조를 요구합니다. 이 차이는 실물 호환성 미확정 사항이며 업그레이드 승인으로 해석하지 않습니다. 연결 전 실제 버전과 해당 릴리스 노트를 확인합니다. description은 기존 두 lock과 같은 `c003186833616b23c06784ebefe442474cc5f4b5`(v2026.8.19)이며 펌웨어 식별과는 별개입니다.

## 상태·단위·촉각 메타데이터

관절 각도는 `joint_states`에서 읽습니다. diagnostics에는 관절 각도가 없습니다. 수신 프레임은 온라인 관절만 임의 순서로 포함할 수 있으므로 **`nid`**로 처리합니다. 엄지 0–3, 검지 4–7, 중지 8–11, 약지 12–15, 소지 16–19입니다. 없는 관절은 누락 상태로 남깁니다. 위치는 rad, 속도는 rad/s이며 **`effort`는 토크 N·m가 아닌 전류 A**입니다.

공식 control guide는 SDK `S1..S4`와 모델 액추에이터 `J0..J3`의 축 순서를 아직 제공하지 않는다고 명시합니다. 관절 개수와 이름이 맞는 것만으로 축 대응이 검증되지는 않습니다. 제조사 근거와 별도 승인된 실물 확인 전에는 미확정으로 유지합니다.

검토한 fingertip 예제는 센서별 format/digest를 받은 뒤 디코딩합니다. 점 개수·필드 단위·위치·센서 좌표계를 보존합니다. 해당 소스는 최근 펌웨어의 정규화된 점별 힘과 이전 펌웨어의 N을 구분하며 합력은 N, 온도는 C로 유지합니다. 정규화 값을 N으로 취급하거나 센서 차원을 고정하지 않습니다. 교육 예제는 합성 점 하나를 사용하며 실제 센서 배치를 뜻하지 않습니다. `timestamp_us`는 SDK의 시계·동기화 의미를 확인해야 합니다. 예제는 실제 UTC 대신 명시적인 합성 시계를 사용합니다.

## 오프라인 실행·예상 결과·복구

순서가 복원된 관절값 20개를 확인합니다. ID 0을 지우고 `allow_partial=True`로 검사하면 `complete=false`, `missing_ids=[0]`, 0번 위치의 `None`이 나옵니다. 다른 손가락을 당겨 채우거나 0을 만들어 넣지 않습니다. 알 수 없는 ID·중복·오래된 상태·펌웨어/SDK 불일치·촉각 메타데이터 변경은 실패합니다. 일관된 합성 데이터를 복원하거나 정확한 센서 format을 다시 확보합니다. fault 해제·원점 설정·토크 활성화·펌웨어 갱신을 자동 복구로 사용하지 않습니다.

## 출처

- [Beta 2 호환성](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility/), [하드웨어 통합](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration/).
- [제어 가이드](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide/), [SDK 참조](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/): 단위·관절 번호·가변 길이 프레임·시각.
- 코드 참조 목록의 고정 `wuji-sdk/examples/python/wuji_hand_2/3.fingertip_typed.py`, `0.subscribe_callback.py`.

## 합성 검사 실행

```bash
python -m pai_lab.manual_examples wuji
python -m pai_lab.manual_examples hands
```

[매뉴얼 자료실과 검증 방법](index.md). 이 검사는 장비 준비 상태나 개인 학습 기록을 갱신하지 않습니다.
