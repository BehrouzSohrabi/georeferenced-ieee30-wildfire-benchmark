# Source registry (Phase 0)

This registry captures discovery and verification routes. Inclusion is not permission to redistribute material.

| ID | Resource | Role | Canonical/official URL | Access date | Verification status | Notes |
|---|---|---|---|---|---|---|
| SRC-0001 | Sohrabi et al., *A Wildfire Progression Simulation and Risk-Rating Methodology for Power Grid Infrastructure* | Source-study bibliographic identity | https://doi.org/10.1109/ACCESS.2024.3439724 | 2026-10-11 | Metadata located; full bibliographic/rights check pending | IEEE Access article; guideline states CC BY-NC-ND 4.0. Do not reuse figures or text without confirmed terms/permission. |
| SRC-0002 | GridMod RTS-GMLC | Comparator discovery | https://github.com/GridMod/RTS-GMLC | 2026-10-11 | Repository located; row-level verification pending | Comparator only; no assertion yet about geospatial fields or license. |
| SRC-0003 | LANDFIRE data portal | Potential landscape source | https://landfire.gov/data | 2026-10-11 | Official portal located; terms/product version check pending | Capture exact product, access date, metadata, and terms before use. |
| SRC-0004 | NREL NSRDB | Potential weather source | https://nsrdb.nrel.gov/background | 2026-10-11 | Official portal located; access/attribution terms pending | Record exact endpoint, dataset, and retrieval parameters. |
| SRC-0005 | MATPOWER | Candidate IEEE 30-bus case provenance | https://github.com/MATPOWER/matpower | 2026-10-11 | Repository/license located; case-file-specific terms pending | MATPOWER code is BSD-3-Clause; case data may have separate terms. Verify exact `case30` provenance. |
| SRC-0006 | USDA Forest Service FARSITE | Candidate fire-simulation software provenance | https://research.fs.usda.gov/firelab/products/dataandtools/farsite | 2026-10-11 | Official product page located; version/distribution terms pending | Record exact executable/version and configuration files before Phase 3. |
| SRC-0007 | Zenodo | Candidate DOI repository | https://zenodo.org/ | 2026-10-11 | Official service page located; account/deposit requirements pending | Candidate only; PI must select repository/DOI provider in D0.2. |

## Rules

1. Prefer DOI, publisher, official agency, official repository, or primary project pages.
2. Search-result snippets are discovery aids, not substantive evidence.
3. Record the exact version, retrieval/access date, and any file checksum once an input is acquired.
4. Rights status is not settled until documented in `docs/phase-0/rights-compliance-memo.md` and reviewed by the authorized humans.
