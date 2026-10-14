"""Non-mutating technical validation for the project-authored spatial layer."""
from __future__ import annotations

import json
import math
from collections import Counter, deque
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from pyproj import Transformer
from shapely.geometry import LineString, Point

NETWORK_PATH = Path("data/network/canonical-network.geojson")
SCHEMA_PATH = Path("data/network/schema.json")
TRANSFORMER = Transformer.from_crs("EPSG:4326", "EPSG:3310", always_xy=True)


def _project_point(coordinates: list[float]) -> Point:
    return Point(*TRANSFORMER.transform(coordinates[0], coordinates[1]))


def _project_line(coordinates: list[list[float]]) -> LineString:
    return LineString([TRANSFORMER.transform(lon, lat) for lon, lat in coordinates])


def _connected(bus_ids: set[int], edges: list[tuple[int, int]]) -> bool:
    if not bus_ids:
        return False
    adjacency = {bus: set() for bus in bus_ids}
    for start, end in edges:
        if start in adjacency and end in adjacency:
            adjacency[start].add(end)
            adjacency[end].add(start)
    visited = {next(iter(bus_ids))}
    queue = deque(visited)
    while queue:
        node = queue.popleft()
        for neighbour in adjacency[node] - visited:
            visited.add(neighbour)
            queue.append(neighbour)
    return visited == bus_ids


def validate_spatial_layer(root: Path) -> dict[str, Any]:
    """Read and validate the release layer without mutating data or reports."""
    root = Path(root)
    network = json.loads((root / NETWORK_PATH).read_text(encoding="utf-8"))
    schema = json.loads((root / SCHEMA_PATH).read_text(encoding="utf-8"))
    errors = [f"schema: {item.json_path}: {item.message}" for item in Draft202012Validator(schema).iter_errors(network)]
    features = network.get("features", [])
    points = [feature for feature in features if feature.get("geometry", {}).get("type") == "Point"]
    lines = [feature for feature in features if feature.get("geometry", {}).get("type") == "LineString"]
    buses: dict[int, list[float]] = {}
    for feature in points:
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [])
        bus = props.get("bus")
        if not isinstance(bus, int) or isinstance(bus, bool):
            errors.append("point missing integer bus")
            continue
        if not (isinstance(coords, list) and len(coords) == 2 and all(isinstance(value, (int, float)) and math.isfinite(value) for value in coords)):
            errors.append(f"bus {bus} has invalid coordinates")
            continue
        if not (-180 <= coords[0] <= 180 and -90 <= coords[1] <= 90):
            errors.append(f"bus {bus} coordinate outside longitude/latitude bounds")
        buses[bus] = coords
    bus_set = set(buses)
    if bus_set != set(range(1, 31)):
        errors.append("bus IDs are not exactly 1..30")
    if {feature.get("properties", {}).get("bus_id") for feature in points} != {f"bus_{index:02d}" for index in range(1, 31)}:
        errors.append("bus_id values are not exactly bus_01..bus_30")

    endpoint_distances: list[float] = []
    lengths: list[float] = []
    edge_list: list[tuple[int, int]] = []
    branch_ids: set[int] = set()
    class_counts: Counter[str] = Counter()
    geometry_errors = 0
    for feature in lines:
        props = feature.get("properties", {})
        branch, fbus, tbus = props.get("branch"), props.get("fbus"), props.get("tbus")
        coords = feature.get("geometry", {}).get("coordinates", [])
        if not all(isinstance(value, int) and not isinstance(value, bool) for value in (branch, fbus, tbus)):
            errors.append("line missing integer branch/fbus/tbus")
            continue
        branch_ids.add(branch)
        expected_id = f"branch_{branch:02d}"
        if props.get("branch_id") != expected_id:
            errors.append(f"branch {branch} has invalid branch_id")
        kind = props.get("branch_type")
        if kind not in {"line", "link"}:
            errors.append(f"branch {branch} has invalid branch_type")
        else:
            class_counts[kind] += 1
        if fbus not in buses or tbus not in buses:
            errors.append(f"branch {branch} references an unknown bus")
            continue
        if not (isinstance(coords, list) and len(coords) >= 2):
            errors.append(f"branch {branch} has fewer than two vertices")
            continue
        if any(not (isinstance(vertex, list) and len(vertex) == 2 and all(isinstance(value, (int, float)) and math.isfinite(value) for value in vertex)) for vertex in coords):
            errors.append(f"branch {branch} has invalid coordinate vertices")
            continue
        geometry = _project_line(coords)
        if not geometry.is_valid or not geometry.is_simple or geometry.length <= 0:
            geometry_errors += 1
            errors.append(f"branch {branch} has invalid, non-simple, or zero-length geometry")
        lengths.append(geometry.length)
        endpoint_distances.extend((_project_point(coords[0]).distance(_project_point(buses[fbus])), _project_point(coords[-1]).distance(_project_point(buses[tbus]))))
        edge_list.append((fbus, tbus))
    if branch_ids != set(range(1, 42)):
        errors.append("branch IDs are not exactly 1..41")
    if class_counts != Counter({"line": 34, "link": 7}):
        errors.append("branch_type partition is not 34 lines and 7 links")
    if endpoint_distances and max(endpoint_distances) > 0.01:
        errors.append("canonical endpoint alignment exceeds 0.01 m")

    total_m = round(sum(lengths), 3)
    return {
        "validation_method": {"storage_crs": "EPSG:4326", "metric_crs": "EPSG:3310", "axis_order": "longitude,latitude", "transformer": "pyproj always_xy=True"},
        "errors": errors,
        "counts": {"buses": len(points), "branches": len(lines), "lines": class_counts["line"], "links": class_counts["link"]},
        "endpoint_alignment": {"max_distance_m": round(max(endpoint_distances, default=0.0), 6), "threshold_m": 0.01},
        "geometry": {"invalid_or_non_simple_or_zero_length": geometry_errors},
        "topology": {"connected": _connected(bus_set, edge_list)},
        "lengths_epsg_3310": {"total_m": total_m, "total_km": round(total_m / 1000, 6), "min_m": round(min(lengths), 3), "max_m": round(max(lengths), 3)},
    }
