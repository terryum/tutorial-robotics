# Robotics stack modernization — 2026-11-13

## Objective
Reproducible cross-host installation and FR3 VLA training/evaluation.

## Current facts
Mac arm64; Core Python 3.12.13/MuJoCo 3.12.0; 17 GiB disk free.
No new WS1/WS2 execution evidence. GR00T 2 code announced for December.

## Work items
- [x] Immutable code/weight revisions and isolated stack CLI
- [x] Installation trigger and release-candidate handoff
- [x] Portable tests and explicit smoke/performance separation
- [ ] Native GPU profile dependency/install/runtime acceptance
- [ ] Model neural inference and supported 32 GB training acceptance
- [ ] FR3/Robotiq task, dataset generator and model-specific converters
- [ ] Full training/resume/independent WS1 evaluation and bilingual catalog lessons
- [ ] Optional ASPIRE/Flora/SimFoundry runtime adapters

## Resume
Read setup/LATEST_ROBOTICS_UPDATE.md, inspect actual host/OS and ignored receipts.
Keep pending items pending until implemented and measured. No fabricated completion.
