#!/usr/bin/env python
"""Build a deterministic, manifest-first spatial-layer release archive."""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
MANIFEST_PATH = DIST / "release-manifest.json"
REQUIRED_ADDITIONS = {
    "data/network/provenance.json",
    "docs/technical-scope-and-evidence.md",
    "docs/data-dictionary.md",
    "docs/datasheet.md",
    "docs/reproduction-boundary.md",
    "docs/phase-1/spatial-technical-validation.json",
    "pytest.ini",
    "requirements.txt",
    "scripts/build_canonical_network.py",
    "scripts/build_release_package.py",
    "scripts/validate_release_package.py",
    "scripts/validate_spatial_layer.py",
    "src/network_curation.py",
    "src/release_package.py",
    "src/spatial_validation.py",
    "tests/test_branch24_regression.py",
    "tests/test_endpoint_snap_regression.py",
    "tests/test_release_package.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    paths = {asset["path"] for asset in manifest["assets"]} | REQUIRED_ADDITIONS
    assets = []
    for relative in sorted(paths):
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"release asset is missing: {relative}")
        if relative.startswith("sources/") or any(term in relative.lower() for term in ("farsite", "pypower", "matpower")):
            raise ValueError(f"restricted release asset: {relative}")
        assets.append({"path": relative, "sha256": sha256(source), "role": "release file"})
    manifest["assets"] = assets
    manifest_bytes = (json.dumps(manifest, indent=2) + "\n").encode("utf-8")
    MANIFEST_PATH.write_bytes(manifest_bytes)

    archive = DIST / manifest["release_name"]
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as package:
        for asset in assets:
            relative = asset["path"]
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            package.writestr(info, (ROOT / relative).read_bytes(), compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
        info = zipfile.ZipInfo("release-manifest.json", date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        package.writestr(info, manifest_bytes, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    (DIST / "SHA256SUMS").write_text(f"{sha256(archive)}  {archive.name}\n", encoding="utf-8", newline="\n")
    print(json.dumps({"archive": archive.name, "assets": len(assets), "sha256": sha256(archive)}, sort_keys=True))


if __name__ == "__main__":
    main()
