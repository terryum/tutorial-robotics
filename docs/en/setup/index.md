<p align="right"><a href="../../ko/setup/index.md">한국어</a> | <a href="../../en/setup/index.md">ENGLISH</a></p>

# Hardware manual library and setup

The local library is `.local/manuals/<device>/` in this checkout. Originals, images and reading PDFs stay outside Git. Public files contain source URLs, revisions, acquisition times, SHA-256 and usage terms in `assets/manuals.json`, source-code references in `assets/manual-code-refs.json`, and our own explanations.

| Device | Setup | Acquired documents | Missing |
|---|---|---:|---|
| enlight | [enlight setup](enlight.md) | 28 | elements, orion, aegis, enlight-quick-start |
| fr3 | [fr3 setup](fr3.md) | 6 | — |
| g1 | [g1 setup](g1.md) | 4 | — |
| wuji | [wuji setup](wuji.md) | 9 | — |
| sharpa | [sharpa setup](sharpa.md) | 1 | — |
| aloha | [aloha setup](aloha.md) | 10 | — |

## List, import, download and verify

```bash
uv sync --locked --extra docs --extra manuals
python scripts/manuals.py list
python scripts/manuals.py import enlight-v01 --file "/path/to/Enlight Series User Manual_V0.1_en.pdf"
python scripts/manuals.py download fr3-product
python scripts/manuals.py verify
```

Identical bytes reuse an integrity-checked version. Changed bytes get a new SHA-256 directory without overwriting earlier files. Import IDs must exist in the manifest. PDF signature and parser checks reject HTML error pages saved as PDFs. Unavailable documents are listed separately; errors in acquired files produce a nonzero exit code.

Web entries retain `original.html`, `reading.html`, `reading.pdf` and `images/`. Reading HTML contains body text and local images with scripts removed. Outgoing links remain source navigation; this is not a mirror of linked websites. Videos are outside this collection. PDFs are labelled web conversions with reflowed text/tables, so pagination differs from vendor PDFs. G1 retains all official page images. Sharpa additionally retains all nine section bodies, the original application JS and extracted JSON.

## Offline examples and verification boundary

```bash
python -m pai_lab.manual_examples all
python -m pai_lab.manual_examples hands
pytest tests/test_manual_examples.py tests/test_manual_library.py
```

`all` validates teaching fixtures informed by SDK state shapes. It makes no connection, imports no SDK, enables no servo, changes no mode and writes no `pal` readiness/progress records. `hands` requires the existing pinned vendor cache and checks hashes, side-specific joints and root frames. Use the asset workflow if that cache is unavailable. Hardware lessons retain `reader_test_required`.

Checks cover valid data, reordering, missing/duplicate IDs, units, stale/future timestamps, incompatible revisions and camera misalignment. Partial Wuji frames report `None` and missing IDs, remaining incomplete. Synthetic clocks and budgets are illustrative and do not validate device communication or safety.

## Pinned code references

| Repository | Commit | License finding |
|---|---|---|
| [flexiv_rdk](https://github.com/flexivrobotics/flexiv_rdk/tree/ff92fe421e19daee6cdf27794a332c8fef7cf831) | `ff92fe421e19` | Apache-2.0 |
| [libfranka](https://github.com/frankarobotics/libfranka/tree/e88d08f64cbf842b8f53c0b551963684064038d6) | `e88d08f64cbf` | Apache-2.0 |
| [franka_ros2](https://github.com/frankarobotics/franka_ros2/tree/6cedf7f1a2ca280c433f643eae697be23eb2a15e) | `6cedf7f1a2ca` | Apache-2.0 |
| [unitree_sdk2_python](https://github.com/unitreerobotics/unitree_sdk2_python/tree/65691c8a8bc53b98d3976dba4dbf9d5d20b2e7f5) | `65691c8a8bc5` | BSD-3-Clause |
| [wuji-sdk](https://github.com/wuji-technology/wuji-sdk/tree/b0e48652dd94f4bc33df61cdc23a6d5dc598f93d) | `b0e48652dd94` | MIT |
| [sharpa-wave-sdk](https://github.com/sharpa-robotics/sharpa-wave-sdk/tree/1c48c44ab7aa08e495bf603e8b68dc5290d01328) | `1c48c44ab7aa` | NOASSERTION - consult vendor; license not established |
| [aloha](https://github.com/Interbotix/aloha/tree/4fa6b2c4428f5334441a7bee5ab2b2e8071cff93) | `4fa6b2c4428f` | MIT |

Existing source/model pins are unchanged. The public Sharpa SDK repository provides an installation README; packaged examples and their license need separate verification.

## Document inventory

- `enlight-v01` — acquired
- [elements](https://flexiv.com/uploaded/en/resource/file/2024/09/20/kppxbf5nmd.pdf) — unavailable
- [orion](https://hub.flexiv.com/login) — unavailable
- [aegis](https://hub.flexiv.com/login) — unavailable
- [enlight-quick-start](https://hub.flexiv.com/login) — unavailable
- [flexiv-rdk-manual](https://www.flexiv.com/software/rdk/manual/v2.x/index.html) — acquired
- [fr3-product](https://www.franka.de/hubfs/Product%20Manual%20Franka%20Research%203_R02210_1.5_EN-1.pdf) — acquired
- [fci-compatibility](https://frankarobotics.github.io/docs/compatibility.html) — acquired
- [fci-install](https://frankarobotics.github.io/docs/doc/libfranka/docs/installation.html) — acquired
- [fci-robot-network](https://frankarobotics.github.io/docs/doc/libfranka/docs/getting_started.html) — acquired
- [g1-user](https://marketing.unitree.com/article/en/G1/User_Manual.html) — acquired
- [g1-remote](https://marketing.unitree.com/article/en/G1/Remote_Control.html) — acquired
- [g1-battery-charger](https://marketing.unitree.com/article/en/G1/Battery_Charger.html) — acquired
- [g1-waist-fastener](https://marketing.unitree.com/article/en/G1/Lumbar_fasteners.html) — acquired
- [wuji-version-compatibility](https://docs.wuji.tech/docs/en/wuji-hand/latest/version-compatibility/) — acquired
- [wuji-product-introduction](https://docs.wuji.tech/docs/en/wuji-hand/latest/overview/) — acquired
- [wuji-user-notice](https://docs.wuji.tech/docs/en/wuji-hand/latest/user-notice/) — acquired
- [wuji-quick-start](https://docs.wuji.tech/docs/en/wuji-hand/latest/quick-start/) — acquired
- [wuji-hardware-integration](https://docs.wuji.tech/docs/en/wuji-hand/latest/hardware-integration/) — acquired
- [wuji-control-guide](https://docs.wuji.tech/docs/en/wuji-hand/latest/control-guide/) — acquired
- [wuji-sdk-reference](https://docs.wuji.tech/docs/en/wuji-hand/latest/sdk-reference/) — acquired
- [wuji-troubleshooting](https://docs.wuji.tech/docs/en/wuji-hand/latest/troubleshooting/) — acquired
- [wuji-appendix](https://docs.wuji.tech/docs/en/wuji-hand/latest/reference/) — acquired
- [sharpa-manual](https://sharpa-robotics.github.io/sharpa-docs/) — acquired
- [aloha-index](https://docs.trossenrobotics.com/aloha_docs/2.0/index.html) — acquired
- [aloha-getting_started-stationary-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/stationary/hardware_setup.html) — acquired
- [aloha-getting_started-stationary-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/stationary/software_setup.html) — acquired
- [aloha-getting_started-mobile-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/mobile/hardware_setup.html) — acquired
- [aloha-getting_started-mobile-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/mobile/software_setup.html) — acquired
- [aloha-getting_started-solo-hardware_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/solo/hardware_setup.html) — acquired
- [aloha-getting_started-solo-software_setup](https://docs.trossenrobotics.com/aloha_docs/2.0/getting_started/solo/software_setup.html) — acquired
- [aloha-operation-bringup_shutdown](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/bringup_shutdown.html) — acquired
- [aloha-operation-data_collection](https://docs.trossenrobotics.com/aloha_docs/2.0/operation/data_collection.html) — acquired
- [aloha-troubleshooting](https://docs.trossenrobotics.com/aloha_docs/2.0/troubleshooting.html) — acquired
- [fci-libfranka-matrix](https://frankarobotics.github.io/docs/doc/libfranka/docs/compatibility_matrix.html) — acquired
- [fci-ros2-matrix](https://frankarobotics.github.io/docs/doc/franka_ros2_jazzy/franka_ros2/doc/compatibility_matrix.html) — acquired
- [flexiv-rdk-what_is_rdk](https://www.flexiv.com/software/rdk/manual/v2.x/what_is_rdk.html) — acquired
- [flexiv-rdk-key_features](https://www.flexiv.com/software/rdk/manual/v2.x/key_features.html) — acquired
- [flexiv-rdk-environment_compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/environment_compatibility.html) — acquired
- [flexiv-rdk-system_requirements](https://www.flexiv.com/software/rdk/manual/v2.x/system_requirements.html) — acquired
- [flexiv-rdk-robot_software_compatibility](https://www.flexiv.com/software/rdk/manual/v2.x/robot_software_compatibility.html) — acquired
- [flexiv-rdk-release_notes](https://www.flexiv.com/software/rdk/manual/v2.x/release_notes.html) — acquired
- [flexiv-rdk-download_rdk](https://www.flexiv.com/software/rdk/manual/v2.x/download_rdk.html) — acquired
- [flexiv-rdk-install_for_cpp](https://www.flexiv.com/software/rdk/manual/v2.x/install_for_cpp.html) — acquired
- [flexiv-rdk-install_for_python](https://www.flexiv.com/software/rdk/manual/v2.x/install_for_python.html) — acquired
- [flexiv-rdk-realtime_ubuntu](https://www.flexiv.com/software/rdk/manual/v2.x/realtime_ubuntu.html) — acquired
- [flexiv-rdk-set_up_the_robot](https://www.flexiv.com/software/rdk/manual/v2.x/set_up_the_robot.html) — acquired
- [flexiv-rdk-activate_rdk_server](https://www.flexiv.com/software/rdk/manual/v2.x/activate_rdk_server.html) — acquired
- [flexiv-rdk-enter_and_exit_remote_mode](https://www.flexiv.com/software/rdk/manual/v2.x/enter_and_exit_remote_mode.html) — acquired
- [flexiv-rdk-connect_user_computer](https://www.flexiv.com/software/rdk/manual/v2.x/connect_user_computer.html) — acquired
- [flexiv-rdk-verify_with_example_programs](https://www.flexiv.com/software/rdk/manual/v2.x/verify_with_example_programs.html) — acquired
- [flexiv-rdk-api_overview](https://www.flexiv.com/software/rdk/manual/v2.x/api_overview.html) — acquired
- [flexiv-rdk-control_modes](https://www.flexiv.com/software/rdk/manual/v2.x/control_modes.html) — acquired
- [flexiv-rdk-robot_states](https://www.flexiv.com/software/rdk/manual/v2.x/robot_states.html) — acquired
- [flexiv-rdk-robot_actions](https://www.flexiv.com/software/rdk/manual/v2.x/robot_actions.html) — acquired
- [flexiv-rdk-robot_description](https://www.flexiv.com/software/rdk/manual/v2.x/robot_description.html) — acquired
- [flexiv-rdk-digital_io_control](https://www.flexiv.com/software/rdk/manual/v2.x/digital_io_control.html) — acquired
- [flexiv-rdk-loss_of_connection](https://www.flexiv.com/software/rdk/manual/v2.x/loss_of_connection.html) — acquired
- [flexiv-rdk-free_drive](https://www.flexiv.com/software/rdk/manual/v2.x/free_drive.html) — acquired
- [flexiv-rdk-ros2_bridge](https://www.flexiv.com/software/rdk/manual/v2.x/ros2_bridge.html) — acquired
- [flexiv-rdk-faq](https://www.flexiv.com/software/rdk/manual/v2.x/faq.html) — acquired
- [flexiv-rdk-error_handling](https://www.flexiv.com/software/rdk/manual/v2.x/error_handling.html) — acquired
