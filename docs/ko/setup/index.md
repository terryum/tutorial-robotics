<p align="right"><a href="../../ko/setup/index.md">한국어</a> | <a href="../../en/setup/index.md">ENGLISH</a></p>

# 하드웨어 매뉴얼 자료실과 setup

로컬 자료실은 저장소의 `.local/manuals/<장비>/`입니다. 원본·그림·열람용 PDF는 Git에서 제외합니다. 공개 파일에는 출처·리비전·수집 시각·SHA-256·이용 조건을 담은 `assets/manuals.json`, 코드 참조를 담은 `assets/manual-code-refs.json`과 직접 작성한 설명만 둡니다.

| 장비 | Setup | 확보 문서 수 | 미확보 |
|---|---|---:|---|
| enlight | [enlight setup](enlight.md) | 28 | elements, orion, aegis, enlight-quick-start |
| fr3 | [fr3 setup](fr3.md) | 6 | — |
| g1 | [g1 setup](g1.md) | 4 | — |
| wuji | [wuji setup](wuji.md) | 9 | — |
| sharpa | [sharpa setup](sharpa.md) | 1 | — |
| aloha | [aloha setup](aloha.md) | 10 | — |

## 목록·가져오기·다운로드·검사

```bash
uv sync --locked --extra docs --extra manuals
python scripts/manuals.py list
python scripts/manuals.py import enlight-v01 --file "/path/to/Enlight Series User Manual_V0.1_en.pdf"
python scripts/manuals.py download fr3-product
python scripts/manuals.py verify
```

동일 바이트는 기존 버전을 검증하고 재사용합니다. 변경본은 SHA-256별 디렉터리에 보관하여 이전 파일을 덮어쓰지 않습니다. 가져오기 대상 ID는 매니페스트에 있어야 합니다. HTML을 PDF로 잘못 저장하면 파일 헤더와 PDF 파서가 거부합니다. 누락 자료는 `UNAVAILABLE`로 별도 표시하고, 확보된 파일의 해시/형식 오류는 0이 아닌 종료값을 반환합니다.

웹 자료는 `original.html`, `reading.html`, `reading.pdf`, `images/`로 보관합니다. 열람용 HTML에는 본문과 로컬 그림을 넣고 스크립트를 제거했습니다. 링크는 출처 이동용이며 다른 웹사이트 전체를 미러링한 것은 아닙니다. 동영상은 수집 범위에 포함되지 않습니다. PDF에는 웹 변환본임을 표시하고, 표·본문을 재배치하므로 제조사 PDF의 인쇄 쪽수와 다릅니다. G1은 공식 페이지 이미지를 전부 보관하며 Sharpa는 동적 앱의 실제 9개 절 본문·원래 배포 JS·추출 JSON도 보관합니다.

## 오프라인 예제와 검증 경계

```bash
python -m pai_lab.manual_examples all
python -m pai_lab.manual_examples hands
pytest tests/test_manual_examples.py tests/test_manual_library.py
```

`all`은 SDK 형태를 참고한 교육용 합성 데이터만 검사합니다. 접속·SDK import·서보 활성화·모드 변경을 실행하지 않으며 `pal`의 준비/학습 기록을 쓰지 않습니다. `hands`는 기존 vendor 모델이 필요하고 체크섬·좌우 관절·루트 프레임을 확인합니다. 캐시가 없으면 자산 관리 절차를 사용하세요. 전체 하드웨어 lesson의 `reader_test_required`는 유지합니다.

정상 입력과 순서 변경·누락·중복·잘못된 단위·오래된/미래 시각·버전 불일치·카메라 정렬 오류를 검사합니다. Wuji 부분 프레임은 `None`과 누락 ID를 반환하며 완전한 상태로 승격하지 않습니다. 합성 시각·허용치는 교육용이고 실제 장비 통신이나 안전 검증이 아닙니다.

## 고정 코드 참조

| Repository | Commit | License finding |
|---|---|---|
| [flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk/tree/ff92fe421e19daee6cdf27794a332c8fef7cf831) | `ff92fe421e19` | Apache-2.0 |
| [libfranka](https://github.com/frankarobotics/libfranka/tree/e88d08f64cbf842b8f53c0b551963684064038d6) | `e88d08f64cbf` | Apache-2.0 |
| [franka_ros2](https://github.com/frankarobotics/franka_ros2/tree/6cedf7f1a2ca280c433f643eae697be23eb2a15e) | `6cedf7f1a2ca` | Apache-2.0 |
| [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python/tree/65691c8a8bc53b98d3976dba4dbf9d5d20b2e7f5) | `65691c8a8bc5` | BSD-3-Clause |
| [wuji-sdk](https://github.com/wuji-technology/wuji-sdk/tree/b0e48652dd94f4bc33df61cdc23a6d5dc598f93d) | `b0e48652dd94` | MIT |
| [sharpa-wave-sdk](https://github.com/sharpa-robotics/sharpa-wave-sdk/tree/1c48c44ab7aa08e495bf603e8b68dc5290d01328) | `1c48c44ab7aa` | NOASSERTION - consult vendor; license not established |
| [aloha](https://github.com/Interbotix/aloha/tree/4fa6b2c4428f5334441a7bee5ab2b2e8071cff93) | `4fa6b2c4428f` | MIT |

기존 source/model pin은 변경하지 않았습니다. Sharpa SDK의 공개 저장소는 설치 README를 제공하며 실제 패키지 예제·라이선스는 별도 확인이 필요합니다.

## 자료 목록

- `enlight-v01` — 확보
- [elements](https://flexiv.com/uploaded/en/resource/file/2024/09/20/kppxbf5nmd.pdf) — 미확보
- [orion](https://hub.flexiv.com/login) — 미확보
- [aegis](https://hub.flexiv.com/login) — 미확보
- [enlight-quick-start](https://hub.flexiv.com/login) — 미확보
- [flexiv-rdk-manual](https://www.flexiv.com/software/rdk/manual/v2.x/index.html) — 확보
- [fr3-product](https://www.franka.de/hubfs/Product%20Manual%20Franka%20Research%203_R02210_1.5_EN-1.pdf) — 확보
- [fci-compatibility](https://frankarobotics.github.io/docs/compatibility.html) — 확보
- [fci-install](https://frankarobotics.github.io/docs/doc/libfranka/docs/installation.html) — 확보
- [fci-robot-network](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html) — 확보
- [g1-user](https://marketing.unitree.com/article/en/G1/User_Manual.html) — 확보
- [g1-remote](https://marketing.unitree.com/article/en/G1/Remote_Control.html) — 확보
- [g1-battery-charger](https://marketing.unitree.com/article/en/G1/Battery_Charger.html) — 확보
- [g1-waist-fastener](https://marketing.unitree.com/article/en/G1/Lumbar_fasteners.html) — 확보
- [wuji-version-compatibility](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility/) — 확보
- [wuji-product-introduction](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview/) — 확보
- [wuji-user-notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice/) — 확보
- [wuji-quick-start](https://docs.wuji.tech/docs/en/wuji-hand/latest/quick-start/) — 확보
- [wuji-hardware-integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration/) — 확보
- [wuji-control-guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide/) — 확보
- [wuji-sdk-reference](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/) — 확보
- [wuji-troubleshooting](https://docs.wuji.tech/docs/en/wuji-hand/latest/troubleshooting/) — 확보
- [wuji-appendix](https://docs.wuji.tech/docs/en/wuji-hand/latest/reference/) — 확보
- [sharpa-manual](https://sharpa-robotics.github.io/sharpa-docs/) — 확보
- [aloha-index](https://docs.trossenrobotics.com/aloha_docs/2.0/index.html) — 확보
- [aloha-getting_started-stationary-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/stationary/hardware_setup.html) — 확보
- [aloha-getting_started-stationary-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/stationary/software_setup.html) — 확보
- [aloha-getting_started-mobile-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/mobile/hardware_setup.html) — 확보
- [aloha-getting_started-mobile-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/mobile/software_setup.html) — 확보
- [aloha-getting_started-solo-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/solo/hardware_setup.html) — 확보
- [aloha-getting_started-solo-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/solo/software_setup.html) — 확보
- [aloha-operation-bringup_shutdown](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/bringup_shutdown.html) — 확보
- [aloha-operation-data_collection](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/data_collection.html) — 확보
- [aloha-troubleshooting](https://docs.trossenrobotics.com/aloha_docs/2.0/troubleshooting.html) — 확보
- [fci-libfranka-matrix](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html) — 확보
- [fci-ros2-matrix](https://frankarobotics.github.io/docs/doc/franka_ros2_jazzy/franka_ros2/doc/compatibility_matrix.html) — 확보
- [flexiv-rdk-what_is_rdk](https://www.flexiv.com/software/rdk/manual/v2.x/what_is_rdk.html) — 확보
- [flexiv-rdk-key_features](https://www.flexiv.com/software/rdk/manual/v2.x/key_features.html) — 확보
- [flexiv-rdk-environment_compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/environment_compatibility.html) — 확보
- [flexiv-rdk-system_requirements](https://www.flexiv.com/software/rdk/manual/v2.x/system_requirements.html) — 확보
- [flexiv-rdk-robot_software_compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/robot_software_compatibility.html) — 확보
- [flexiv-rdk-release_notes](https://www.flexiv.com/software/rdk/manual/v2.x/release_notes.html) — 확보
- [flexiv-rdk-download_rdk](https://www.flexiv.com/software/rdk/manual/v2.x/download_rdk.html) — 확보
- [flexiv-rdk-install_for_cpp](https://www.flexiv.com/software/rdk/manual/v2.x/install_for_cpp.html) — 확보
- [flexiv-rdk-install_for_python](https://www.flexiv.com/software/rdk/manual/v2.x/install_for_python.html) — 확보
- [flexiv-rdk-realtime_ubuntu](https://www.flexiv.com/software/rdk/manual/v2.x/realtime_ubuntu.html) — 확보
- [flexiv-rdk-set_up_the_robot](https://www.flexiv.com/software/rdk/manual/v2.x/set_up_the_robot.html) — 확보
- [flexiv-rdk-activate_rdk_server](https://www.flexiv.com/software/rdk/manual/v2.x/activate_rdk_server.html) — 확보
- [flexiv-rdk-enter_and_exit_remote_mode](https://www.flexiv.com/software/rdk/manual/v2.x/enter_and_exit_remote_mode.html) — 확보
- [flexiv-rdk-connect_user_computer](https://www.flexiv.com/software/rdk/manual/v2.x/connect_user_computer.html) — 확보
- [flexiv-rdk-verify_with_example_programs](https://www.flexiv.com/software/rdk/manual/v2.x/verify_with_example_programs.html) — 확보
- [flexiv-rdk-api_overview](https://www.flexiv.com/software/rdk/manual/v2.x/api_overview.html) — 확보
- [flexiv-rdk-control_modes](https://www.flexiv.com/software/rdk/manual/v2.x/control_modes.html) — 확보
- [flexiv-rdk-robot_states](https://www.flexiv.com/software/rdk/manual/v2.x/robot_states.html) — 확보
- [flexiv-rdk-robot_actions](https://www.flexiv.com/software/rdk/manual/v2.x/robot_actions.html) — 확보
- [flexiv-rdk-robot_description](https://www.flexiv.com/software/rdk/manual/v2.x/robot_description.html) — 확보
- [flexiv-rdk-digital_io_control](https://www.flexiv.com/software/rdk/manual/v2.x/digital_io_control.html) — 확보
- [flexiv-rdk-loss_of_connection](https://www.flexiv.com/software/rdk/manual/v2.x/loss_of_connection.html) — 확보
- [flexiv-rdk-free_drive](https://www.flexiv.com/software/rdk/manual/v2.x/free_drive.html) — 확보
- [flexiv-rdk-ros2_bridge](https://www.flexiv.com/software/rdk/manual/v2.x/ros2_bridge.html) — 확보
- [flexiv-rdk-faq](https://www.flexiv.com/software/rdk/manual/v2.x/faq.html) — 확보
- [flexiv-rdk-error_handling](https://www.flexiv.com/software/rdk/manual/v2.x/error_handling.html) — 확보
