# 한국어 오프라인 교재 첫 검증

2026년 11월 24일 Apple Silicon Mac에서 공개 Core 캐시를 사용해 개발 검증을 실행했습니다. 운영체제와 Python·MuJoCo 버전, 기존 수업의 구현과 대표 산출물 SHA-256은 [Mac 수치 요약](robotics-ko/mac-results.json)에 있습니다. 대표 수업은 씨드 7, 표본 수 64, 변형 계수 1.0으로 실행했습니다. 개발 러너는 학습 완료 요건만 분리하고 플랫폼, 의존성, 모델 지문, 수치와 렌더링 검사를 적용했습니다. BC의 입력은 같은 배치에서 생성하고 검사한 시연 기록을 사용했습니다.

| 검증 | 근거 | 결과 |
| --- | --- | --- |
| 진자와 2링크 팔 | `core-01`, `arm.json` | 에너지 최대 편차 6.51×10⁻¹³ J, 자코비안 중앙차분 최대 차이 8.23×10⁻¹¹ m/rad. 보간 직선은 충돌했고 우회 경로의 여유 하한은 10.64 mm였습니다. |
| Enlight 추종과 학습 | `core-enlight-03/04/05` | 후반 TCP RMSE 5.19 mm. BC·PPO 모두 16회 갱신하고 저장 후 예측을 재현했습니다. 독립 도달 기준은 16/20이고, BC는 20/20, PPO는 0/20이었습니다. |
| 알려진 위치와 RGB-D 집기 | `pick.json`, `pick-trace.csv`, `pick-camera.npz` | 두 시험 모두 82.26 mm 상승과 양쪽 손가락 접촉 1,007 스텝을 기록했습니다. RGB-D의 물체 중심 오차 0.606 mm, 재투영 오차 0 px, 목표 영역의 최종 XY 오차 0.677 mm를 확인했습니다. |
| 이동 로봇 | `slam.json`, `slam-trace.npz` | 위치 RMSE는 오도메트리 2.177 m, SLAM 2.67 mm였습니다. SLAM 점유 격자의 벽 셀 IoU는 0.968이었습니다. |
| Enlight 카메라 | `rgbd.json`, `rgb.png`, `depth.npy` | MuJoCo의 기본 팔 초기 자세에서 TCP 오차 0 m, 320×240 배열에서 유한한 양의 픽셀 76,800개, 장면 깊이 중앙값 0.900 m를 기록했습니다. |
| XR 명령 차단 | `xr.json` | 합성 입력에서 정상 8 mm, 추적 유실·오래된 수신·신규 프레임 부재·클러치 해제 0 mm, 조기 재시도 0 mm, 재무장 후 48 mm를 기록했습니다. |
| HTML | Chrome 158, 네트워크 비활성화, 1440×950과 390×844 | 목차의 다섯 앵커, 목차 복귀, 키보드로 펼치기, 내장 그림, 외부 리소스 요청 0건을 확인했습니다. |

Mac 검증에는 ROS 2 Jazzy와 Isaac Sim·CUDA에 필요한 조건이 없었습니다. 해당 카탈로그 실행은 차단 결과를 남겼습니다. WS2에서는 [워크스테이션 런북](../setup/WS2_ROBOTICS_KO_VERIFY.md)에 따라 PhysX 추종·접촉, 초기 자세 RGB-D, 짧은 정책 학습과 독립 평가, NVIDIA 모델 추론을 검증합니다. 장비 입력과 실제 로봇은 별도의 현장 실습에 해당합니다.

교재를 재생성하려면 저장소 루트에서 Docs 환경으로 빌더를 실행합니다.

```bash
uv sync --locked --extra docs
uv run --no-sync python scripts/build_robotics_ko.py
```

생성 파일은 `outputs/robotics-ko/index.html`입니다. [교재 원고](robotics-ko/index.md)에서 각 실습의 명령과 비교 조건을 확인할 수 있습니다.
