import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.network_curation import canonicalize_network  # noqa: E402


class EndpointSnapRegressionTest(unittest.TestCase):
    def test_nearby_source_endpoint_is_snapped_to_authoritative_bus_coordinate(self):
        source = ROOT / "sources" / "IGREFire" / "data" / "grid"
        output = ROOT / "data" / "network" / "canonical-network.geojson"
        result = canonicalize_network(
            base_geojson=source / "IEEE_30_bus_system.geojson",
            case_file=source / "IEEE_30_bus_system.py",
            output_geojson=output,
        )
        self.assertEqual(result["snapped_endpoint_branches"], [1, 3, 5, 6])
        network = json.loads(output.read_text(encoding="utf-8"))
        branch_1 = next(
            f for f in network["features"]
            if f["geometry"]["type"] == "LineString"
            and int(f["properties"]["branch"]) == 1
        )
        bus_2 = next(
            f["geometry"]["coordinates"] for f in network["features"]
            if f["geometry"]["type"] == "Point"
            and int(f["properties"]["bus"]) == 2
        )
        self.assertEqual(branch_1["geometry"]["coordinates"][-1], bus_2)


if __name__ == "__main__":
    unittest.main()
