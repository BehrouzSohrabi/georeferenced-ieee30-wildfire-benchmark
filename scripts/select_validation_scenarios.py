#!/usr/bin/env python
"""Create the auditable 206-scenario validation selection from a frozen CSV."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scenario_selection import ScenarioSelectionError, select_validation_scenarios, write_selection_csv  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="frozen UTF-8 scenario-manifest CSV")
    parser.add_argument("output", type=Path, help="destination selection.csv")
    parser.add_argument(
        "--expected-line-count",
        type=int,
        default=41,
        help="required number of line IDs (default: 41; pass 0 to disable)",
    )
    args = parser.parse_args()
    try:
        result = select_validation_scenarios(
            args.manifest,
            expected_line_count=None if args.expected_line_count == 0 else args.expected_line_count,
        )
        write_selection_csv(result, args.output)
    except ScenarioSelectionError as error:
        parser.error(str(error))

    print(f"manifest_sha256={result.manifest_sha256}")
    print(f"candidate_rows={len(result.rows)}")
    print(f"selected_rows={result.selected_count}")
    print(f"selection_csv={args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
