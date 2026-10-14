#!/usr/bin/env python
"""Validate the project-authored spatial release package."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.release_package import validate_release_archive, validate_release_manifest

errors = validate_release_manifest(ROOT) + validate_release_archive(ROOT)
if errors:
    print("RELEASE PACKAGE VALIDATION FAILED")
    print("\n".join(f"- {error}" for error in errors))
    raise SystemExit(1)
print("RELEASE PACKAGE VALIDATION PASSED")
