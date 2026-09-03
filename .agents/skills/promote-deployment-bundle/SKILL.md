---
name: promote-deployment-bundle
description: Validate and promote a reproducible candidate deployment bundle after required simulation and policy gates pass.
---

# Promote Deployment Bundle

Require completed prerequisite gates and a clean, reproducible source revision. Build a manifest containing source commits, environment lock or image digest, model and dataset hashes, interface versions, limits, and rerun commands.

Promotion never grants hardware command authority. Run offline replay and command-sink validation, keep large artifacts outside Git, and commit only manifests, checksums, small evidence, and adapter code.
