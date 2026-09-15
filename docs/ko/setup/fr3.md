<p align="right"><a href="../../ko/setup/fr3.md">한국어</a> | <a href="../../en/setup/fr3.md">ENGLISH</a></p>

# Franka Research 3 — Setup 검토

**검증 상태: 모든 실물 단계는 `reader_test_required`.** 이 안내는 모델별 설치 검토를 준비하기 위한 문서입니다. 시뮬레이션 모델로 보유 장비를 식별하지 마세요. 실물 모델·좌우·리비전·펌웨어·컨트롤러·SDK는 로컬에 기록하고 일련번호·주소·보정값은 Git에서 제외합니다.

실물 작업 전 [하드웨어 안전](../../07_SAFETY.md)을 읽으세요. 해당 매뉴얼, 제조사 지정 고정구와 전원, 보호 접지, 정지 장치, 격리 네트워크, 작업자를 준비합니다. 설치·보정·제어 활성화·동작은 장비별 절차와 해당 실행 승인이 필요합니다. 아래 명령은 합성 데이터만 검사합니다.

## 준비와 설치 검토

다운로드 URL에는 1.5가 있지만, 파일 내부 리비전은 **R02210, 1.5.1 (2025년 6월), 시스템 5.8.0 적용**입니다. 실제 시스템 버전과 맞는지 먼저 확인합니다.

| 검토 작업 | 필요한 확인 근거 | 제품 매뉴얼 |
|---|---|---|
| 안정된 기초와 작업영역 준비 | 설치면·여유 공간·컨트롤러 환기 조건 충족 | §10.2–10.5 60–68쪽 |
| 팔/컨트롤러 배선·정지 주변장치·접지 검토 | 전원 투입 전 커넥터와 기능 접지 확인 | §10.6 69–77쪽; §4.7 23쪽 |
| 엔드이펙터 식별과 장착 | 질량·무게중심·장착 정보를 로컬 기록 | §10.7 78–79쪽 |
| 기동과 정지 기능 시험 검토 | 자격을 갖춘 작업자가 실제 결과 기록 | §11.1–11.3 93–103쪽 |

## 소프트웨어 조합 선택

1. 컨트롤러 화면에서 실제 시스템/image 버전과 FCI 사용 가능 여부를 확인합니다.
2. 보관한 **Compatibility: libfranka** 표에서 해당 로봇/서버 버전을 찾습니다. 예를 들어 스냅샷은 시스템 ≥5.7.2에 libfranka ≥0.15.0 및 서버 9/3을, 시스템 ≥5.9.0에 libfranka ≥0.18.0 및 서버 10/3을 연결합니다. 최신 라이브러리를 바로 선택하지 말고 해당 행의 버전 범위 전체를 확인합니다.
3. **Compatibility: franka_ros2** 표에서 `franka_description`을 포함해 공통으로 허용되는 조합을 선택합니다. Jazzy 안내는 Ubuntu 24.04를 권장합니다. Humble/Jazzy 작업공간을 구분합니다.
4. FCI 네트워크 설정(§11.4 104–112쪽)과 해당 upstream 설치 절을 검토합니다. 커널 설치·FCI 활성화·제어 시험은 실물 시운전 작업이며 이번 오프라인 예제에 포함되지 않습니다.

## 오프라인 상태 검사와 복구

`q`, `dq`, `tau_J`는 rad·rad/s·N·m 단위의 값 7개입니다. libfranka의 `O_T_EE`는 열 우선 4×4 동차변환입니다. 예제의 pose는 O 좌표계의 m/`wxyz` 표현을 따로 선언한 것이며 원시 배열을 그대로 복사한 값이 아닙니다. 수신 시각은 명시적인 합성 시계로 검사합니다. 로봇 상대 시각을 호스트 UTC와 직접 비교하면 안 됩니다.

ID 순서를 뒤집어도 관절값 7개가 복원되어야 합니다. SDK/모델 버전·좌표계·단위·쿼터니언 크기·오래된 시각·SDK 배열 불일치는 실패해야 합니다. 실물의 라이브러리 호환성 오류는 보고된 서버 버전과 호환성 표를 다시 확인합니다. timeout은 케이블·인터페이스·라우팅·FCI 상태를 점검합니다. 시험을 통과시키려고 fault를 해제하거나 Watchman 규칙을 바꾸지 않습니다.

## 출처

- 로컬 `fr3-product`, R02210 1.5.1: 위 설치 및 FCI 절.
- [libfranka 호환성](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html), [Jazzy 호환성](https://frankarobotics.github.io/docs/doc/franka_ros2_jazzy/franka_ros2/doc/compatibility_matrix.html).
- [FCI 로봇·네트워크 설정](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html).

## 합성 검사 실행

```bash
python -m pai_lab.manual_examples fr3
```

[매뉴얼 자료실과 검증 방법](index.md). 이 검사는 장비 준비 상태나 개인 학습 기록을 갱신하지 않습니다.
