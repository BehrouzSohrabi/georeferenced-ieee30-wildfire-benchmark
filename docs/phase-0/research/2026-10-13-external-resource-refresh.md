# External-resource refresh — 13 October 2026

**Purpose:** Phase 0 refresh of release-routing evidence. This note is a provenance/release-risk record, not legal advice or legal clearance.

## Verified routing posture

| Dependency | v1.0.0 routing | Basis / action |
|---|---|---|
| MATPOWER `case30.m` | Pointer-only | MATPOWER's code license excludes its case files. Preserve exact upstream revision and cite it; do not include copied case data without independent rights review. |
| FARSITE executable/source | Excluded | The official Forest Service/FRAMES materials identify FARSITE as unsupported separately and no current redistributable binary/source license was verified. Do not ship the binary from the source snapshot. |
| LANDFIRE layers | User-obtained unless layer-level clearance is recorded | Preserve exact product/version, metadata, citation, access date, checksum, transformations, and terms. Do not mirror bulk rasters by default. |
| NSRDB inputs | User-obtained unless source-specific redistribution terms and attribution are captured | Release a script plus exact query/version/location/time range/variables; never publish credentials. |
| Sohrabi et al. (2024), DOI 10.1109/ACCESS.2024.3439724 | Pointer-only | Cite/link the article. Do not bundle its PDF, figures, maps, tables, or adapted material as release payload. |

## Official sources checked

- MATPOWER repository and license: <https://github.com/MATPOWER/matpower>, <https://github.com/MATPOWER/matpower/blob/master/LICENSE>
- MATPOWER `case30.m`: <https://github.com/MATPOWER/matpower/blob/master/data/case30.m>
- FARSITE: <https://research.fs.usda.gov/firelab/products/dataandtools/farsite>; <https://www.frames.gov/catalog/908>
- LANDFIRE: <https://landfire.gov/data>; <https://landfire.gov/data/FullExtentDownloads>
- NSRDB: <https://nsrdb.nrel.gov/>; <https://developer.nrel.gov/docs/solar/nsrdb/guide/>
- IEEE Access article: <https://doi.org/10.1109/ACCESS.2024.3439724>

**Access date:** 2026-10-13.

## Release consequence

The v0.1.0 spatial-layer pre-release remains a deliberately thin, project-authored package. This resource refresh does not grant clearance to expand its payload. Any later inclusion requires an updated clearance-register row with exact version, official terms, attribution, reviewer, decision date, and evidence path.
