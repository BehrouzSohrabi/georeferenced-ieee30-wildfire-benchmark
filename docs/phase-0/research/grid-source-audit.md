# Preliminary Phase 1 grid-source audit

**Source snapshot:** `IGREFire` commit `194b15e2423e824a9a4447cb83c8e1cbef84dd0a`  
**Audit status:** main-verified source facts; not yet a release-quality network layer.  
**Method:** read-only parsing of both GeoJSON files and source case inventory; calculations below are geodesic screening values, not the required EPSG:3310 release calculation.

## Observed files

- `data/grid/IEEE_30_bus_system.geojson`
- `data/grid/IEEE_30_bus_system_labeled.geojson`
- `data/grid/IEEE_30_bus_system.py`
- `data/grid/IEEE_30_bus_system_costs.py`
- `data/grid/IEEE_30_bus_system_piecewise.py`
- `data/grid/IEEE_30_bus_system_check.json`

## Main-verified screening results

| Check | Result | Interpretation |
|---|---:|---|
| GeoJSON features | 71 | 30 `Point` features + 41 `LineString` features |
| Explicit line types | 34 `BRANCH`, 7 `LINK` | Matches the guideline’s 34-line/7-link topology target |
| Unique branch IDs | 41 | IDs span the full branch set; endpoint mapping still needs a canonical table test |
| GeoJSON `crs`/`bbox` members | absent | Coordinate ranges look like lon/lat; document EPSG:4326 explicitly in derived release records rather than relying on GeoJSON convention |
| All-line haversine screening length | 686.119 km | Not comparable to the required California Albers calculation |
| `BRANCH`-only haversine screening length | 683.737 km | 2.32% below the paper’s 702 km target; must be recomputed from canonical polylines in EPSG:3310 and either reconciled or logged |
| Sum of source `length` attributes | 1,025.7 (units unspecified) | Not suitable as a length metric without unit/provenance evidence |

## Known data-quality risk

The two GeoJSON variants are not yet demonstrated equivalent. Audit evidence found at least one attribute disagreement in the labeled version (`tbus` for branch 24). Canonical source selection and branch-by-branch crosswalk are required before Phase 1 output generation.

## Minimum Phase 1 implementation plan

1. Freeze the selected electrical case and create a machine-readable canonical branch table (`branch_id`, `from_bus`, `to_bus`, `type`, ratings, electrical parameters, source commit).
2. Generate `buses.csv`/GeoJSON and `branches.csv`/GeoJSON from scripts—not hand edits—with stable zero-padded IDs.
3. Explicitly tag output coordinate reference systems: EPSG:4326 storage and EPSG:3310 length calculations.
4. In CI, enforce: 30 buses; 41 branches; 34/7 type split; valid geometry; all endpoints within 1 m of their matched bus in EPSG:3310; study-box bounds; and a branch-table equality test against the case file.
5. Compute length only after the canonical geometry decision. If its 34-line total is outside 702 km ±0.5%, add an explained discrepancy rather than changing data silently.
6. Run a pinned base-case ACOPF regression after the case variant and solver are frozen.

## Evidence boundary

This audit does not establish the upstream license of any source file, the intended electrical case variant, EPSG:3310 lengths, endpoint tolerance, or base ACOPF objective.
