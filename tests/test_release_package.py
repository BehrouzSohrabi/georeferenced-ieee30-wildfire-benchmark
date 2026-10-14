import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.release_package import validate_release_archive, validate_release_manifest  # noqa: E402
from src.spatial_validation import validate_spatial_layer  # noqa: E402


class ReleasePackageTests(unittest.TestCase):
    def test_project_spatial_package_is_self_consistent(self):
        self.assertEqual(validate_release_manifest(ROOT), [])

    def test_hash_tampering_is_reported_with_asset_path(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            (fixture / "data/network").mkdir(parents=True)
            shutil.copy2(ROOT / "data/network/canonical-network.geojson", fixture / "data/network/canonical-network.geojson")
            manifest = json.loads((ROOT / "data/network/manifest.json").read_text(encoding="utf-8"))
            manifest["asset"]["sha256"] = "0" * 64
            (fixture / "data/network/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            errors = validate_release_manifest(fixture)

        self.assertEqual(errors, ["checksum mismatch: data/network/canonical-network.geojson"])

    def test_out_of_range_or_missing_line_endpoints_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            fixture = Path(temporary)
            (fixture / "data/network").mkdir(parents=True)
            network = json.loads((ROOT / "data/network/canonical-network.geojson").read_text(encoding="utf-8"))
            line = next(feature for feature in network["features"] if feature["geometry"]["type"] == "LineString")
            line["properties"].pop("tbus")
            payload = json.dumps(network)
            asset_path = fixture / "data/network/canonical-network.geojson"
            asset_path.write_text(payload, encoding="utf-8")
            import hashlib
            manifest = json.loads((ROOT / "data/network/manifest.json").read_text(encoding="utf-8"))
            manifest["asset"]["sha256"] = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            (fixture / "data/network/manifest.json").write_text(json.dumps(manifest), encoding="utf-8")

            errors = validate_release_manifest(fixture)

        self.assertEqual(errors, ["line feature 1 missing integer endpoint properties"])

    def test_canonical_layer_has_stable_public_identifiers_and_branch_classes(self):
        network = json.loads((ROOT / "data/network/canonical-network.geojson").read_text(encoding="utf-8"))
        points = [f for f in network["features"] if f["geometry"]["type"] == "Point"]
        lines = [f for f in network["features"] if f["geometry"]["type"] == "LineString"]
        self.assertEqual({f["properties"].get("bus_id") for f in points}, {f"bus_{n:02d}" for n in range(1, 31)})
        self.assertEqual({f["properties"].get("branch_id") for f in lines}, {f"branch_{n:02d}" for n in range(1, 42)})
        self.assertEqual({f["properties"].get("branch_type") for f in lines}, {"line", "link"})

    def test_spatial_validator_reports_canonical_geometry_evidence(self):
        report = validate_spatial_layer(ROOT)
        self.assertEqual(report["errors"], [])
        self.assertEqual(report["counts"], {"buses": 30, "branches": 41, "lines": 34, "links": 7})
        self.assertEqual(report["endpoint_alignment"]["max_distance_m"], 0.0)
        self.assertTrue(report["topology"]["connected"])
        self.assertEqual(report["lengths_epsg_3310"]["total_m"], 687388.234)

    def test_release_archive_is_frozen_and_clean(self):
        self.assertEqual(validate_release_archive(ROOT), [])


if __name__ == "__main__":
    unittest.main()
