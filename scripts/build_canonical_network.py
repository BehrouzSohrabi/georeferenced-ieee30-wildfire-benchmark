#!/usr/bin/env python
"""Build the internal topology-authoritative canonical network layer."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.network_curation import canonicalize_network

SOURCE = ROOT / "sources" / "IGREFire" / "data" / "grid"
OUTPUT = ROOT / "data" / "network" / "canonical-network.geojson"
REPORT = ROOT / "docs" / "phase-1" / "network-canonicalization-report.json"


def main() -> None:
    result = canonicalize_network(
        base_geojson=SOURCE / "IEEE_30_bus_system.geojson",
        case_file=SOURCE / "IEEE_30_bus_system.py",
        output_geojson=OUTPUT,
    )
    result.update({
        "source_geojson": "sources/IGREFire/data/grid/IEEE_30_bus_system.geojson",
        "topology_case": "sources/IGREFire/data/grid/IEEE_30_bus_system.py",
        "output": "data/network/canonical-network.geojson",
        "endpoint_policy": "Reorient geometry to fbus-to-tbus and snap endpoints within 500 m to authoritative bus coordinates.",
    })
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
