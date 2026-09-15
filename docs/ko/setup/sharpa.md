<p align="right"><a href="../../ko/setup/sharpa.md">한국어</a> | <a href="../../en/setup/sharpa.md">ENGLISH</a></p>

# Sharpa Wave — Setup 검토

**검증 상태: 모든 실물 단계는 `reader_test_required`.** 이 안내는 모델별 설치 검토를 준비하기 위한 문서입니다. 시뮬레이션 모델로 보유 장비를 식별하지 마세요. 실물 모델·좌우·리비전·펌웨어·컨트롤러·SDK는 로컬에 기록하고 일련번호·주소·보정값은 Git에서 제외합니다.

실물 작업 전 [하드웨어 안전](../../07_SAFETY.md)을 읽으세요. 해당 매뉴얼, 제조사 지정 고정구와 전원, 보호 접지, 정지 장치, 격리 네트워크, 작업자를 준비합니다. 설치·보정·제어 활성화·동작은 장비별 절차와 해당 실행 승인이 필요합니다. 아래 명령은 합성 데이터만 검사합니다.

## 맞는 손과 소프트웨어 패키지 준비

장착 도면·전원·케이블을 선택하기 전에 Wave의 좌우와 하드웨어 리비전을 식별합니다. 보관한 **Overview**, **Get Started**, **User Guide → Hardware Installation** 및 안전 절로 고정 강성·케이블 여유·제공 전기 인터페이스·냉각 공간을 전원 차단 상태에서 검토합니다. 매뉴얼은 능동 자유도 22개를 설명합니다. 이름만 바꿔 왼손 모델을 오른손으로 사용할 수는 없습니다.

현재 공개 SDK 저장소에는 설치 안내가 있고 바이너리·예제는 릴리스 패키지로 제공합니다. 검토한 README는 amd64 `.deb`와 aarch64 `.zip`을 구분하며 설치 구조는 `/opt/sharpa-wave-sdk/`입니다. Python은 패키지의 3.10/3.11/3.12 확장 모듈과 CPU 아키텍처가 맞아야 합니다. 수집한 웹 매뉴얼에는 Python 3.13 파일명 예시가 있지만 SDK README는 3.13 미지원이라고 명시합니다. 실제 릴리스 내용과 해당 README로 호환성을 확인하며 여기서 패키지를 설치하지 않습니다.

## 좌표계·촉각과 Wuji 비교

| 항목 | Sharpa Wave 모델 | Wuji Hand 2 Beta 2 모델 |
|---|---|---|
| 손 하나의 구동 관절 | 22 | 20 |
| 루트 body | `left_hand_C_MC` / `right_hand_C_MC` | `l_wrist` / `r_wrist` |
| 이름 규칙 | 관절의 `left_` / `right_` 접두사 | 관절의 `l_` / `r_` 접두사 |
| SDK 관계 | 해당 릴리스의 관절 표와 확인 | S1–S4/J0–J3 축 대응 미확정 |

비교 명령은 양쪽 모델을 불러와 관절 수·좌우 접두사·루트 프레임을 검사합니다. 관절 부호를 반전하거나 실물 축을 확인하지는 않습니다. Sharpa **Development** 절의 joint mapping·control·tactile API를 기준으로 실제 센서·좌표계·단위·format 메타데이터를 보존합니다. Wuji 전류나 촉각 규칙을 그대로 가져오지 않습니다. Sharpa 합성 데이터의 단위는 교육용으로 따로 선언한 것이며 SDK 원시 ABI가 아닙니다.

## 오프라인 실행과 복구

`python -m pai_lab.manual_examples sharpa`와 아래 손 비교 명령을 실행합니다. Sharpa 좌우 각각 22개, Wuji 각각 20개를 기대합니다. 모델이 없으면 unavailable이며 고정 파일이 변조되면 체크섬 검사가 실패해야 합니다. 자산 관리 절차로 정확한 vendor 캐시를 복원하고 시험을 맞추려고 캐시를 수정하지 않습니다. 향후 실물 호스트의 Python import/loader 오류는 CPU·Python minor 버전·공유 라이브러리 조합을 확인합니다. 제어 소스 변경이나 gesture 실행은 읽기 전용 복구가 아닙니다.

## 출처

- [Sharpa Wave 매뉴얼](https://sharpa-robotics.github.io/sharpa-docs/): Development/SDK·Support를 포함한 모든 절 본문과 그림 보관.
- [Wave SDK](https://github.com/sharpa-robotics/sharpa-wave-sdk): 코드 참조 목록에 README의 정확한 커밋·해시 기록; 바이너리 패키지 재배포 권한은 미확인.
- 기존 Menagerie·Wuji model lock과 Wuji MJLab 참조를 유지하며 Sharpa RL 패키지는 새로 설치하지 않았습니다.

## 합성 검사 실행

```bash
python -m pai_lab.manual_examples sharpa
python -m pai_lab.manual_examples hands
```

[매뉴얼 자료실과 검증 방법](index.md). 이 검사는 장비 준비 상태나 개인 학습 기록을 갱신하지 않습니다.
