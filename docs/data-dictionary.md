# Data dictionary — georeferenced IEEE 30-bus spatial layer

**Version:** 0.1.0-pre-release  
**Primary file:** `data/network/canonical-network.geojson`  
**Storage CRS / axis order:** WGS 84 (EPSG:4326), `[longitude, latitude]`  
**Metric-validation CRS:** California Albers (EPSG:3310)

## Feature collection

| Entity | Count | Geometry | Stable identifier |
|---|---:|---|---|
| Bus | 30 | `Point` | `bus_id` (`bus_01`…`bus_30`) |
| Branch route | 41 | `LineString` | `branch_id` (`branch_01`…`branch_41`) |

GeoJSON follows RFC 7946 coordinate conventions. It has no GeoJSON `crs` object because RFC 7946 fixes geographic coordinates to WGS 84; the CRS contract is repeated here and in `manifest.json`.

## Bus-point properties

| Field | Type | Meaning | Domain / unit |
|---|---|---|---|
| `bus_id` | string | Project-stable public bus key | `bus_01`…`bus_30`; never reuse or renumber within a release lineage |
| `bus` | integer | IEEE-30 topology bus number used by the crosswalk | 1–30 |
| `type` | string | Source-derived illustrative point category | `GEN`, `SUBSTATION`, or `NODE`; not an operational asset classification |
| `OBJECTID` | integer | Source-snapshot local feature identifier | Retained for provenance only; do not use as a stable key |

## Branch-route properties

| Field | Type | Meaning | Domain / unit |
|---|---|---|---|
| `branch_id` | string | Project-stable public branch-route key | `branch_01`…`branch_41`; never reuse or renumber within a release lineage |
| `branch` | integer | IEEE-30 study-topology branch index | 1–41 |
| `fbus` | integer | Electrical from-bus number and route start endpoint | 1–30 |
| `tbus` | integer | Electrical to-bus number and route end endpoint | 1–30 |
| `branch_type` | string | Project-normalized route class | `line` (34) or `link` (7) |
| `type` | string | Source-snapshot class retained for provenance | `BRANCH` or `LINK` |
| `length` | numeric | Source-snapshot route-length attribute | Source units are not asserted by this release; use computed EPSG:3310 lengths for analysis |
| `Shape_Length` | numeric | Source-snapshot geometry-length attribute | Source units are not asserted by this release; use computed EPSG:3310 lengths for analysis |
| `OBJECTID` | integer | Source-snapshot local feature identifier | Retained for provenance only; do not use as a stable key |

## Quality contract

The reproducible validator (`scripts/validate_spatial_layer.py`) verifies the complete numeric-ID sets, stable-ID formatting, 34/7 route-class partition, coordinate bounds, geometry validity/non-self-intersection, positive geometry length, endpoint alignment to `fbus`/`tbus` points within 0.01 m in EPSG:3310, and graph connectivity. Its generated report is `docs/phase-1/spatial-technical-validation.json`.

This synthetic spatial layer is not an actual utility map or an operational wildfire/grid decision product. It does not distribute the upstream IEEE case, FARSITE, or third-party environmental payloads.
