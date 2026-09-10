# Capability and safety gates

These gates describe evidence, not a required sequence of named computers. Learners progress through the catalog DAG; local eligibility is calculated from capabilities and `.local/progress.json`.

| Gate | Scope | Persistent? | Required evidence |
|---|---|---:|---|
| `CORE_CURRICULUM_VERIFIED` | Stage 1 | yes | 25 headless lesson checks on a supported host, including bootstrap and pendulum artifacts |
| `SIMULATION_RUNTIME_VERIFIED` | selected Stage 2 track | yes | matching ROS/GPU/Isaac maintainer or reader evidence |
| `CANDIDATE_DEPLOYMENT_BUNDLE_READY` | one explicit robot/task/policy | yes | sample or real candidate manifest, hashes, deterministic vectors, limits, rollback |
| `RUNTIME_OFFLINE_VALIDATED` | runtime host | yes | rebuild, offline replay, command sink, shadow, rollback |
| `ROBOT_READ_ONLY_VALIDATED_<ROBOT>` | one physical robot | yes | model/firmware/SDK identity and sanitized state summary |
| `LOW_RISK_VALIDATED_<ROBOT>` | one approved action | no | dated run card and one bounded action result |

`sim-deploy-01` teaches the bundle contract with the committed small sample candidate. It does not require every GPU track. The same checks must later be applied to a selected robot's actual candidate.

Hardware motion/contact approval is never inherited, global, or permanent. `hw-common-01` and `hw-common-02` precede only the robot track being used. `hw-enlight-wuji-01` is eligible only when both devices and both read-only gates are present.

No gate is production approval.
