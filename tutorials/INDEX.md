# Public Tutorial Index

This registry is closed over public tutorials: every prerequisite is available in this repository.

| ID | Robot/group | Title | Prerequisites |
|---|---|---|---|
| [T30](aloha/T30_aloha_simulation_and_act.md) | `aloha` | ALOHA simulation and ACT | [T28, T29] |
| [T00](common/T00_repository_bootstrap_and_host_audit.md) | `common` | Repository bootstrap and host audit | [] |
| [T01](common/T01_mujoco_hello_world_pendulum_state_and_timestep.md) | `common` | MuJoCo hello world: pendulum state and timestep | [T00] |
| [T02](common/T02_download_and_pin_public_robot_sources.md) | `common` | Download and pin the public robot sources | [T00] |
| [T03](common/T03_multi-model_inspector_and_asset_validation.md) | `common` | Multi-model inspector and asset validation | [T01, T02] |
| [T04](common/T04_unified_viewer_and_deterministic_renderer.md) | `common` | Unified viewer and deterministic renderer | [T03] |
| [T17](common/T17_ros_2_fundamentals_topics_qos_services_actions_and_tf.md) | `common` | ROS 2 fundamentals: communication, parameters, lifecycle, URDF, and TF | [T00, T02] |
| [T19](common/T19_mujoco_ros_2_bridge.md) | `common` | MuJoCo–ROS 2 bridge | [T04, T17] |
| [T20](common/T20_rosbag_episode_recorder_and_deterministic_replay.md) | `common` | Rosbag episode recorder and deterministic replay | [T19] |
| [T21](common/T21_common_embodiment_api_across_simulation_and_ros_2.md) | `common` | Common embodiment API across simulation and ROS 2 | [T15, T19] |
| [T23](common/T23_minimal_continuous-action_ppo_from_scratch.md) | `common` | Minimal continuous-action PPO from scratch | [T22] |
| [T28](common/T28_lerobot-style_episode_dataset_from_simulation.md) | `common` | LeRobot-style episode dataset from simulation | [T20, T21] |
| [T29](common/T29_behavioral_cloning_baseline.md) | `common` | Behavioral cloning baseline | [T28] |
| [T32A](common/T32A_vla_protocol_and_mock_policy_client_on_macbook.md) | `common` | VLA protocol, small SmolVLA experiment, and policy client on MacBook | [T28] |
| [T32C](common/T32C_smolvla_finetuning_and_policy_server_on_ws2.md) | `common` | SmolVLA fine-tuning and policy server on WS2 | [T32A] |
| [T32D](common/T32D_pi0_or_groot_remote_inference_on_ws2.md) | `common` | Optional π₀ or GR00T remote inference on WS2 | [T32C] |
| [T33](cross-robot/T33_import_public_robot_assets_into_isaac_sim.md) | `cross-robot` | Import public robot assets into Isaac Sim | [T04] |
| [T34](cross-robot/T34_isaac_camera_lighting_and_synthetic_manufacturing_dataset.md) | `cross-robot` | Isaac camera, lighting, and synthetic manufacturing dataset | [T33] |
| [T35A](cross-robot/T35A_ws2_candidate_deployment_bundle_and_promotion_gate.md) | `cross-robot` | WS2 candidate deployment bundle and promotion gate | [T26, T27, T32C, T34, T35] |
| [T35B](cross-robot/T35B_robot_runtime_bootstrap_offline_replay_and_shadow_dry_run.md) | `cross-robot` | Robot runtime bootstrap, offline replay, and shadow dry-run | [T35A] |
| [T35](cross-robot/T35_mujoco_isaac_sim-to-sim_validation.md) | `cross-robot` | MuJoCo–Isaac sim-to-sim validation | [T24, T33] |
| [T36](cross-robot/T36_real-hardware_read-only_integration_gate.md) | `cross-robot` | Real-hardware read-only integration gate | [T35B] |
| [T05](fr3/T05_fr3_model_anatomy.md) | `fr3` | FR3 model anatomy | [T04] |
| [T06](fr3/T06_fr3_joint-space_pd_control.md) | `fr3` | FR3 joint-space PD control | [T05] |
| [T07](fr3/T07_gravity_compensation_and_feedforward.md) | `fr3` | Gravity compensation and feedforward | [T06] |
| [T08](fr3/T08_fr3_forward_kinematics_jacobian_and_inverse_kinematics.md) | `fr3` | FR3 forward kinematics, Jacobian, and inverse kinematics | [T07] |
| [T09](fr3/T09_fr3_cartesian_and_operational-space_control.md) | `fr3` | FR3 Cartesian and operational-space control | [T08] |
| [T10](fr3/T10_contact_and_friction_laboratory_with_cosmetic_objects.md) | `fr3` | Contact and friction laboratory with cosmetic objects | [T09] |
| [T22](fr3/T22_gymnasium_fr3_reach_environment.md) | `fr3` | Gymnasium FR3 reach environment | [T08, T21] |
| [T24](fr3/T24_ppo_on_fr3_reach.md) | `fr3` | PPO on FR3 reach | [T23] |
| [T16A](sharpa-wave/T16A_wuji_sharpa_retargeting_and_demonstration_recording.md) | `sharpa-wave` | Wuji/Sharpa hand retargeting and demonstration recording | [T14, T16, T28, T30] |
| [T16](sharpa-wave/T16_wuji_versus_sharpa_model_comparison.md) | `sharpa-wave` | Wuji versus Sharpa model comparison | [T14] |
| [T25](unitree-g1/T25_unitree_g1_model_playback_and_motion-data_pipeline.md) | `unitree-g1` | Unitree G1 model playback and motion-data pipeline | [T03, T04] |
| [T26](unitree-g1/T26_unitree_g1_ppo_and_motion_imitation_on_nvidia_workstation.md) | `unitree-g1` | Unitree G1 PPO and motion imitation on NVIDIA workstation | [T25] |
| [T14](wuji-hand2/T14_wuji_hand_2_joints_named_poses_and_synergies.md) | `wuji-hand2` | Wuji Hand 2 joints, named poses, and synergies | [T04] |
| [T15](wuji-hand2/T15_wuji_contact_sensing_and_virtual_tactile_observation.md) | `wuji-hand2` | Wuji contact sensing and virtual tactile observation | [T10, T14] |
| [T27](wuji-hand2/T27_wuji_in-hand_ppo_on_nvidia_workstation.md) | `wuji-hand2` | Wuji in-hand PPO on NVIDIA workstation | [T15, T23] |
| [T38](wuji-hand2/T38_wuji_hand_2_beta_2_hardware_adapter_and_tactile_calibration.md) | `wuji-hand2` | Wuji Hand 2 Beta 2 hardware adapter and tactile calibration | [T15, T27, T36] |
| [T42A](wuji-hand2/T42A_wuji_cosmetics_dexterity_training_and_candidate_bundle.md) | `wuji-hand2` | Wuji cosmetics dexterity simulation and candidate bundle | [T16A, T27, T32C, T35A] |
| [T42B](wuji-hand2/T42B_wuji_cosmetics_dexterity_shadow_and_gated_real_evaluation.md) | `wuji-hand2` | Wuji cosmetics dexterity shadow and gated real evaluation | [T38, T42A] |
