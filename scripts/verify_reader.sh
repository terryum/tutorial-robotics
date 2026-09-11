#!/bin/sh
set -eu
mkdir -p .local/reader-redesign
.venv/bin/python scripts/verify_course.py --profile core --local-dir .local/reader-redesign/course > .local/reader-redesign/core-verification.log 2>&1
