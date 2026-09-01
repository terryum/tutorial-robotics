---
id: TXX
title: "Tutorial title"
phase: "Phase"
host: "registered-profile | mac/either | ws2-sim-train | ws2-robot-integration/ws1-robot-runtime"
prerequisites: []
gpu: "none | optional | required"
hardware: "none | read-only | motion-approval"
optional: false
repeatable: false
---

# TXX — Tutorial title

## Objective

State one executable learning objective.

## Prerequisites

- Tutorial status:
- Host profile:
- Phase gates:
- GPU:
- Hardware access:
- Read first:

## Concepts to explain

- mental model
- equations, units and frame conventions
- data/control flow
- what simulation can and cannot prove

## Required implementation targets

- reusable source module
- thin example/CLI
- tests or smoke tests
- persistent outputs
- Korean lesson report

## Execution procedure

1. preflight the registered host/profile and local readiness
2. implement the smallest reusable slice
3. test before scaling or touching hardware
4. execute the actual example
5. save reproducible commands, logs, metrics and visualizations
6. update shared and machine-local state

## Commands that must exist or be replaced by documented equivalents

- `pal run TXX --help`

## Visualization contract

Persist artifacts under `outputs/TXX/<run-id>/`. GUI-only success is insufficient; save PNG, MP4, CSV, JSON or Markdown evidence.

## Acceptance criteria

- [ ] prerequisites and profile were verified
- [ ] tests/smoke tests pass
- [ ] actual execution was verified
- [ ] persistent outputs and Korean report exist
- [ ] state/gates were updated with evidence

## Failure handling

Do not mark the tutorial complete when a dependency, GPU, GUI or hardware gate is absent. Record the exact command, environment, source commit and error, then use `pending-host` or `blocked-retry`.

## Completion note

Report the exact rerun command, output directory, key result, limitations and the next eligible tutorial or machine-handoff command. Complete only one tutorial per request unless the user explicitly requests more.
