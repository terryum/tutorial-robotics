"""Thin entry point for hw-wuji-01."""

from __future__ import annotations

import argparse
from pathlib import Path
from uuid import uuid4

from pai_lab.catalog import ROOT
from pai_lab.lessons import run_lesson


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--samples", type=int, default=64)
    parser.add_argument(
        "--output-dir", type=Path, default=ROOT / ".local/runs/hw-wuji-01" / uuid4().hex
    )
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--variant", type=float, default=1.0)
    args = parser.parse_args()
    result = run_lesson(
        "hw-wuji-01",
        output_dir=args.output_dir,
        seed=args.seed,
        samples=args.samples,
        variant=args.variant,
        headless=args.headless,
    )
    print(f"lesson={result.lesson_id} metric={result.metric_value} digest={result.artifact_digest}")


if __name__ == "__main__":
    main()
