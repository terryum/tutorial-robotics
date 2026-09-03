---
name: update-upstreams
description: Audit and deliberately update pinned public vendor sources without modifying or pushing vendor repositories.
---

# Update Upstreams

Treat vendor repositories as read-only dependencies. Inspect the current pin, remote release or commit, license, and local cleanliness before proposing an update.

Do not modify vendor content. Update only the pin, source manifest, checksum, adapters, and tests in this repository. Run boundary and regression checks, and document any asset redistribution restriction. Never initialize every vendor source merely for T00.
