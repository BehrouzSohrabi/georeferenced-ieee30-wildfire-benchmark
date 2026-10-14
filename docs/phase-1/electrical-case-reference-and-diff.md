# Electrical-case reference and diff specification

## Selected reference

The comparison reference is MATPOWER `data/case30.m`, pinned to commit `2e0ef79a6c4526858ee923491d92781ad4507fb7`. This is the closest upstream reference to the configured IGREFire case `data/grid/IEEE_30_bus_system.py`; it is not an assertion that the upstream case file may be redistributed.

`case_ieee30.m` is not the selected reference because it differs substantially in row ordering/content and would obscure the small study-case modifications.

## Direct audit finding

The preserved IGREFire study case differs from MATPOWER `case30` in exactly two observed values:

| Entity | Parameter | IGREFire | MATPOWER case30 |
|---|---|---:|---:|
| Bus 3 | `Pd` | 3.0 MW | 2.4 MW |
| Branch 1 → 2 | `RATE_A` | 20 MVA | 130 MVA |

The following otherwise matched in the direct audit: `baseMVA` (100.0), all generator parameters, all generator-cost parameters, all other bus parameters, and all other branch parameters. These differences are preserved—not normalized—in v1.0.0 to maintain the study case.

## Required deterministic comparison artifact

The project must generate JSON plus Markdown/CSV from the exact local case and a fetched/pinned reference. Record source URLs, paths, commits, and SHA-256 hashes. Compare without mutation:

- `baseMVA` exactly;
- all 13 `bus` columns keyed by `BUS_I`;
- all 21 `gen` columns keyed by `(GEN_BUS, occurrence)`;
- all 13 `branch` columns keyed by directed `(F_BUS, T_BUS, occurrence)`; and
- all `gencost` columns paired with their generator key.

Match rows by these stable entity keys rather than array index. Do not reorder branch endpoints because orientation can affect taps and phase shift. Report shape/key mismatches separately; never silently truncate or pad. Use exact numerical comparison, then stable-sort output by entity type, key, and column index.

**Acceptance condition:** the generated parameter-diff report identifies the two preserved modifications above and no undocumented deviations. Any other result creates or updates an entry in `docs/discrepancies.md`.
