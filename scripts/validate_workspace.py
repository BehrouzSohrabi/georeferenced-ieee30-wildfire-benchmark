#!/usr/bin/env python
"""Fail-fast structural validation for the initial benchmark workspace."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_DIRS = [
    "data/network", "data/landscape", "data/weather", "data/ignition",
    "data/simulation", "data/results", "src", "notebooks", "tests",
    "docs/gates", "docs/phase-0", "docs/literature", "docs/resources", "logs",
]
REQUIRED_FILES = [
    "README.md", ".gitignore", "docs/project-guideline-v1.0.md",
    "docs/PROJECT_STATUS.md", "docs/decisions.md", "docs/discrepancies.md",
    "docs/gates/phase_0.md", "docs/phase-0/phase-0-plan.md",
    "docs/phase-0/asset-inventory.csv", "docs/resources/source-registry.md",
]
ASSET_COLUMNS = {
    "asset_id", "relative_path", "asset_type", "size_bytes", "sha256",
    "provenance", "source_version", "license_or_terms", "release_status",
    "custodian", "notes",
}

errors: list[str] = []
for relative in REQUIRED_DIRS:
    if not (ROOT / relative).is_dir():
        errors.append(f"missing directory: {relative}")
for relative in REQUIRED_FILES:
    if not (ROOT / relative).is_file():
        errors.append(f"missing file: {relative}")

with (ROOT / "docs/phase-0/asset-inventory.csv").open(newline="", encoding="utf-8") as handle:
    reader = csv.DictReader(handle)
    if set(reader.fieldnames or []) != ASSET_COLUMNS:
        errors.append("asset inventory header does not match the governed schema")
    rows = list(reader)
    if not rows:
        errors.append("asset inventory has no initial governing-document row")

required_markers = {
    "README.md": ["synthetic research benchmark", "EPSG:4326", "EPSG:3310"],
    "docs/gates/phase_0.md": ["P0.1", "P0.5", "PI signature"],
    "docs/phase-0/phase-0-plan.md": ["Asset inventory", "Decision record", "Related-work matrix"],
}
for relative, markers in required_markers.items():
    content = (ROOT / relative).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in content:
            errors.append(f"{relative} missing required marker: {marker}")

if errors:
    print("WORKSPACE VALIDATION FAILED")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)
print("WORKSPACE VALIDATION PASSED")
print(f"root={ROOT}")
print(f"directories={len(REQUIRED_DIRS)} files={len(REQUIRED_FILES)} inventory_rows={len(rows)}")
