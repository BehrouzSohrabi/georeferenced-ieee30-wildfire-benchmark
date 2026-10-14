# Datasheet — Georeferenced IEEE 30-bus spatial layer

## Motivation

This dataset provides a project-authored, inspectable spatial georeferencing of the standard IEEE 30-bus test-system topology. It supports reproducible spatial-method research where coordinates and route geometry are needed but must not be confused with real utility infrastructure.

## Composition

The release contains a GeoJSON FeatureCollection with 30 bus points and 41 branch routes, a schema, a file manifest, a reproducible builder, a spatial validator, tests, and release-integrity metadata. The 41 routes contain 34 `line` and 7 `link` classes.

## Collection and processing

The dataset is built from a pinned non-release source snapshot using `scripts/build_canonical_network.py`. The builder reconciles branch endpoints to the selected topology, corrects the documented branch-24 label inconsistency, reorients routes to `fbus`→`tbus`, and snaps only source endpoints within 500 m to their associated bus coordinate. Stable `bus_id`, `branch_id`, and normalized `branch_type` fields are added by the project.

## Validation

The published technical validator uses EPSG:3310 for metric checks. At the current pre-release build, it reports: 30 buses, 41 routes, 34 lines, 7 links; a connected 30-node electrical graph; zero invalid/non-simple/zero-length geometries; maximum endpoint mismatch of 0.0 m under a 0.01 m criterion; and total route length of 687.388234 km. These are spatial-layer integrity checks, not validation of a wildfire, ACOPF, risk, or operational model.

## Intended uses

Appropriate uses include spatial-overlay methods, reproducible GIS demonstrations, topology-aware geospatial algorithms, and illustrative wildfire/grid research interfaces. Users can substitute separately licensed landscape, weather, ignition, fire-model, and grid-analysis components while preserving provenance.

## Limitations and prohibited inferences

The placement and corridors are synthetic and illustrative. They do not identify utility assets, establish physical line characteristics, validate any fire simulation, support operational wildfire prediction, transmission planning, or real-grid decisions. `length` and `Shape_Length` are retained source attributes with undocumented units; analysis must use metric lengths recomputed from geometry in EPSG:3310.

## Distribution and maintenance

The project-authored spatial layer is CC BY 4.0; code is MIT. Third-party IEEE case files, FARSITE, PYPOWER/MATPOWER copies, and environmental payloads are excluded unless separately cleared. Version changes must preserve stable IDs and document any geometry or topology change in the changelog and discrepancy log.
