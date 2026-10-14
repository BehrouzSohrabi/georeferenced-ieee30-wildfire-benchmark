#!/usr/bin/env python
"""Emit the reproducible technical-validation report for the spatial layer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.spatial_validation import validate_spatial_layer

report = validate_spatial_layer(ROOT)
output = ROOT / "docs" / "phase-1" / "spatial-technical-validation.json"
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(json.dumps(report, sort_keys=True))
if report["errors"]:
    raise SystemExit(1)
