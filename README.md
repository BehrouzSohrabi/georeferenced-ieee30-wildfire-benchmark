# Georeferenced IEEE 30-Bus Wildfire Benchmark

A reproducible, synthetic spatial dataset built around a **new, project-authored georeferencing of the IEEE 30-bus test system**. Its principal contribution is the technically documented and validated placement of bus points and branch routes, with stable spatial identifiers, topology crosswalks, coordinate rules, and reproducible quality controls. Wildfire–grid workflows are illustrative downstream uses of this reusable georeferenced system, not the central dataset claim; users may substitute compatible landscape, fuel, weather, ignition, fire-model, or grid-analysis components while preserving provenance and reproducibility.

## Status

**Phase:** 0 — scoping, audit, and decisions (started 2026-10-11)  
**Release status:** Not yet public; no DOI or production dataset has been minted.  
**Governing plan:** [`docs/project-guideline-v1.0.md`](docs/project-guideline-v1.0.md)

## Core principles

- Scripted provenance; no manual editing of released data or manuscript values.
- WGS84 storage (EPSG:4326); metric calculations in California Albers (EPSG:3310).
- Stable, zero-padded identifiers and open, documented formats.
- Explicit discrepancy and decision logs.
- Independent gate review and cold-start reproduction before release.

## Repository layout

```text
 data/       released inputs and derived records (not yet populated)
 docs/       governance, gates, provenance, resources, literature, and data documentation
 notebooks/  reproducible demonstrations
 scripts/    pipeline and validation entry points
 src/        package/source code
 tests/      automated tests
 logs/       reproducible run records (not source data)
```

## Current work

See [`docs/PROJECT_STATUS.md`](docs/PROJECT_STATUS.md) and [`docs/phase-0/phase-0-plan.md`](docs/phase-0/phase-0-plan.md). No claim in this repository should be treated as validated until its Phase gate is signed.

## Safety and intended use

This is a synthetic research benchmark for comparing methods. The network placement and line routes are illustrative and do not represent any real utility asset or location. It is not for operational wildfire prediction, transmission planning, or real-grid decision-making.
