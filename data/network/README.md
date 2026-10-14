# Georeferenced IEEE 30-bus spatial layer

`canonical-network.geojson` is the project-authored geospatial benchmark layer for the IEEE 30-bus test system.

## Contents

- 30 bus point features
- 41 branch-route LineString features
- WGS 84 longitude/latitude coordinates (EPSG:4326)
- Stable `bus_id` and `branch_id` identifiers (`bus_01`…`bus_30`, `branch_01`…`branch_41`)
- Electrical endpoint fields (`fbus`, `tbus`) reconciled to the selected IEEE-30 study topology
- Explicit `branch_type` classification (`line` or `link`) for all branch routes

## Intended use

This is an illustrative, synthetic research mapping. It is intended for reproducible spatial-overlay and grid-method benchmarking. Users may replace compatible fuel, weather, ignition, fire-model, or grid-analysis components while recording those components' provenance and licenses.

It does not represent a real utility network or support operational wildfire prediction, transmission planning, or real-grid decisions.

## Attribution

Cite the repository dataset release and cite the underlying IEEE 30-bus test-system source separately. This GeoJSON is the project’s spatial/georeferencing contribution; it does not redistribute a FARSITE executable or copied PYPOWER/MATPOWER source files.
