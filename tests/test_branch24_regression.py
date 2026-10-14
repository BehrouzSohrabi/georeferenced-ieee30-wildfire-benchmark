import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.network_curation import canonicalize_network  # noqa: E402


class Branch24RegressionTest(unittest.TestCase):
    def test_branch_24_label_matches_authoritative_case_and_geometry(self):
        source = ROOT / "sources" / "IGREFire" / "data" / "grid"
        output = ROOT / "data" / "network" / "canonical-network.geojson"
        result = canonicalize_network(
            base_geojson=source / "IEEE_30_bus_system.geojson",
            case_file=source / "IEEE_30_bus_system.py",
            output_geojson=output,
        )
        self.assertEqual(result["corrected_branch_labels"], [24])
        network = json.loads(output.read_text(encoding="utf-8"))
        branch_24 = next(
            f for f in network["features"]
            if f["geometry"]["type"] == "LineString"
            and int(f["properties"]["branch"]) == 24
        )
        self.assertEqual(int(branch_24["properties"]["fbus"]), 19)
        self.assertEqual(int(branch_24["properties"]["tbus"]), 20)
        bus_20 = next(
            f["geometry"]["coordinates"] for f in network["features"]
            if f["geometry"]["type"] == "Point"
            and int(f["properties"]["bus"]) == 20
        )
        self.assertEqual(branch_24["geometry"]["coordinates"][-1], bus_20)


if __name__ == "__main__":
    unittest.main()
