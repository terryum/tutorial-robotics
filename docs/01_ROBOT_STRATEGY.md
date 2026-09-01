# Robot Strategy

## 1. Core portfolio

| ID | Role | Native/public strengths | Main tutorials | Transfer target |
|---|---|---|---|---|
| `wuji_hand2_beta2` | real target | URDF, MJCF, USD, 20 DoF, tactile-oriented model and RL repo | T14–T16A, T27, T33, T38, , T42A–T42B | Wuji Hand 2 |
| `unitree_g1_29dof` | reference | official MuJoCo/Isaac RL and deployment examples | T25–T26 | whole-body learning concepts |
| `sharpa_wave` | reference | URDF/MJCF/USD, tactile dynamics and retargeting examples | T16, T16A | Wuji comparison |

## 2. Priority and proxy rule

```text
→ Wuji Hand 2
→ ALOHA/ACT
→ G1 PPO
→ Sharpa comparison
→ H2 Plus watchlist
```

- FR3 is a 7-DoF control textbook, **not** a dynamically equivalent Enlight.
- Sharpa is a comparison/reference hand; Wuji remains the primary target hand.

## 3. What transfers

- task-space pose/action conventions
- episode and dataset schema
- camera naming and time synchronization
- evaluator definitions
- control architecture patterns
- reward and observation design principles
- logging, visualization, and deployment gates

## 4. What does not transfer without identification

- PD/impedance gains
- torque/current/velocity limits
- friction, damping and armature values
- payload and link inertia
- latency and control frequency
- collision/contact solver assumptions
- tactile calibration and scale
- policy action normalization or policy weights

## 5. Curriculum allocation

- manipulator control/contact: **40%**
- Wuji dexterity/tactile: **20%**
- IL/VLA data pipeline: **10%**
- G1 locomotion/whole-body RL: **5%**

These percentages guide tutorial emphasis. They do not remove required acceptance tests.

## 6. H2 Plus policy

`Unitree H2 Plus` is recorded as a watchlist model. Codex may add it only after an upstream audit confirms reproducible public assets, runnable code, stable file paths, and a clear advantage over G1 for the specific lesson.
