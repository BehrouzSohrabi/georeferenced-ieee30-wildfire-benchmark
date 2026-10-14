# Dataset positioning and asset boundary

## What this project contributes

The contribution is a **project-authored, georeferenced spatial benchmark layer for the IEEE 30-bus test system**. The standard IEEE 30-bus electrical test case already exists; this project does not claim to create or own it.

The new benchmark layer consists of:

- an illustrative WGS84 placement of the buses and branch corridors;
- stable identifiers and an electrical-topology crosswalk;
- documented coordinate reference systems, length calculations, and geometry-quality controls;
- a documented interface for overlaying the spatial system with selected landscape, fuel, weather, ignition, fire-perimeter, and grid-analysis records;
- scripts, manifests, checksums, tests, and documentation that make the georeferencing inspectable and let users substitute compatible downstream inputs for method comparison.

Wildfire progression, ACOPF, outage, and risk-analysis pipelines are example applications of the spatial layer. They are not asserted as the central contribution of this release and are not a prerequisite for reuse of the georeferenced system.

## What this project does not claim or distribute by default

- It does not claim ownership of the IEEE 30-bus case data.
- It does not claim ownership of FARSITE, publish its executable/source, or represent FARSITE as a project asset.
- It does not represent an actual transmission system, utility corridor, or operational wildfire prediction system.
- It does not automatically redistribute third-party landscape, fuel, weather, software, article text, or figures.

## Extensibility

Users may use the benchmark framework to replace or modify components—for example fuel/landscape layers, weather conditions, ignition rules, spatial corridors, outage rules, solvers, or metrics—subject to the terms of the substituted resources. Every such variation should preserve source metadata, license/attribution records, CRS/units, IDs, scenario manifests, and reproducible regeneration scripts.

## Intended claim

The appropriate claim is: this release provides a synthetic, georeferenced IEEE 30-bus wildfire–grid **benchmark framework and spatial dataset** that makes the project’s mapping and analysis workflow inspectable, reproducible, and extensible for method comparison.
