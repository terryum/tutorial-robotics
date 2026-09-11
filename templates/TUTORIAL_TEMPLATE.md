---
id: TXX
title: "Title"
phase: "Phase"
mode: "development | robot-runtime | any"
requires: [dev_core]
preferred_execution: "portable-or-full-development-host | full-gpu-linux-host | robot-runtime-host"
gpu: "none | optional | required"
hardware: "none | read-only | motion-approval"
---

# TXX — Title

## Objective

## Prerequisites

- Tutorial status:
- Required capabilities: see front matter
- Hardware gate:
- Read first:

## Concepts to explain

## Required implementation targets

## Execution procedure

1. preflight local capabilities and environment
2. implement small deterministic baseline
3. add host-specific acceleration only as a separate configuration
4. test, execute, visualize and report

## Acceptance criteria

- [ ] prerequisites, mode and capabilities verified
- [ ] tests/smoke tests pass
- [ ] actual execution verified
- [ ] persistent outputs and Korean report exist
- [ ] shared progress updated

## Capability mismatch

Keep local status `capability-unavailable`, record the local mismatch under `.local/`, and let `$run-next-tutorial` scan for another eligible row. Use `blocked-retry` only for a reproducible failure on a host that should support this tutorial.
