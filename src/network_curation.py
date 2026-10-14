"""Create a topology-authoritative canonical network layer from an audited source snapshot."""
from __future__ import annotations

import json
import math
import re
from pathlib import Path
from typing import Any

EARTH_RADIUS_M = 6_371_008.8


def _haversine_m(a: list[float], b: list[float]) -> float:
    lon1, lat1, lon2, lat2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    h = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_M * math.asin(math.sqrt(h))


def _case_branch_endpoints(case_file: Path) -> dict[int, tuple[int, int]]:
    """Parse numbered branch rows from the audited PYPOWER-style case file without executing it."""
    text = case_file.read_text(encoding="utf-8")
    match = re.search(r'ppc\["branch"\]\s*=\s*array\(\[(.*?)\]\)', text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"No numbered branch array found in {case_file}")
    endpoints: dict[int, tuple[int, int]] = {}
    row = re.compile(r"^\s*\[\s*(\d+)\s*,\s*(\d+).*?\]\s*,?\s*#\s*(\d+)\s*$")
    for line in match.group(1).splitlines():
        parsed = row.match(line)
        if parsed:
            fbus, tbus, branch = map(int, parsed.groups())
            endpoints[branch] = (fbus, tbus)
    if len(endpoints) != 41:
        raise ValueError(f"Expected 41 numbered case branches, found {len(endpoints)}")
    return endpoints


def canonicalize_network(base_geojson: Path, case_file: Path, output_geojson: Path) -> dict[str, list[int]]:
    """Emit a canonical layer whose branch labels and orientation agree with the electrical case."""
    network: dict[str, Any] = json.loads(base_geojson.read_text(encoding="utf-8"))
    endpoints = _case_branch_endpoints(case_file)
    buses = {
        int(feature["properties"]["bus"]): feature["geometry"]["coordinates"]
        for feature in network["features"]
        if feature["geometry"]["type"] == "Point"
    }
    corrected, reoriented, snapped = [], [], []
    for feature in network["features"]:
        if feature["geometry"]["type"] == "Point":
            props = feature["properties"]
            bus = int(props["bus"])
            props["bus_id"] = f"bus_{bus:02d}"
            continue
        if feature["geometry"]["type"] != "LineString":
            continue
        props = feature["properties"]
        branch = int(props["branch"])
        props["branch_id"] = f"branch_{branch:02d}"
        raw_type = str(props.get("type", "")).upper()
        if raw_type not in {"BRANCH", "LINK"}:
            raise ValueError(f"Branch {branch} has unsupported source type {raw_type!r}")
        props["branch_type"] = "line" if raw_type == "BRANCH" else "link"
        fbus, tbus = endpoints[branch]
        coords = feature["geometry"]["coordinates"]
        direct = _haversine_m(coords[0], buses[fbus]) + _haversine_m(coords[-1], buses[tbus])
        reverse = _haversine_m(coords[-1], buses[fbus]) + _haversine_m(coords[0], buses[tbus])
        if reverse < direct:
            coords = list(reversed(coords))
            feature["geometry"]["coordinates"] = coords
            reoriented.append(branch)
        start_gap, end_gap = _haversine_m(coords[0], buses[fbus]), _haversine_m(coords[-1], buses[tbus])
        if max(start_gap, end_gap) > 500.0:
            raise ValueError(f"Branch {branch} geometry endpoints do not match case buses {fbus}->{tbus}")
        if start_gap > 1.0 or end_gap > 1.0:
            coords[0], coords[-1] = buses[fbus], buses[tbus]
            snapped.append(branch)
        if int(props.get("fbus")) != fbus or int(props.get("tbus")) != tbus:
            corrected.append(branch)
        props["fbus"], props["tbus"] = fbus, tbus
    output_geojson.parent.mkdir(parents=True, exist_ok=True)
    output_geojson.write_text(json.dumps(network, indent=2) + "\n", encoding="utf-8")
    return {
        "corrected_branch_labels": corrected,
        "reoriented_branches": reoriented,
        "snapped_endpoint_branches": snapped,
    }
