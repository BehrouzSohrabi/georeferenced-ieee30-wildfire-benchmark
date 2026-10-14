# Discrepancy log

Record observed differences from Sohrabi et al. (2024) without silently normalizing them. A difference is a finding pending explanation.

| ID | Date found | Artifact/metric | Reference value or behavior | Recomputed value or behavior | Suspected cause | Resolution/status | Evidence |
|---|---|---|---|---|---|---|---|
| D-0001 | 2026-10-11 | Total source branch-line length | 702 km reported target | 683.737 km using haversine screening on 34 `BRANCH` GeoJSON polylines | Different length method, corridor geometry, or paper definition; required EPSG:3310 calculation has not been performed | Open. Recompute using the selected canonical geometry in EPSG:3310; explain any remaining difference | `docs/phase-0/research/grid-source-audit.md` |
| D-0002 | 2026-10-11 | GeoJSON variants | Base and labeled variants are expected to represent the same topology | Base branch 24 was labeled `19 -> 29`; electrical case, labeled GeoJSON, and geometry establish `19 -> 20` | Labeling inconsistency in base source | Resolved in generated canonical network; regression test verifies branch 24. Original snapshot remains unchanged for provenance | `scripts/build_canonical_network.py`; `docs/phase-1/network-canonicalization-report.json` |
