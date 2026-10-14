# Release candidate contents

The v0.1.0-pre-release package contains only the project-authored spatial benchmark derivative and the code/documentation needed to inspect its distributed form:

- `data/network/canonical-network.geojson`, schema, manifest, README, and machine-readable provenance record;
- spatial and release validators;
- canonicalization code and its regression tests, while **not** redistributing the upstream inputs required to execute the canonicalization builder;
- data dictionary, datasheet, technical scope, reproduction boundary, licenses, citation metadata, and release-integrity metadata.

The public GitHub repository is a **pre-release candidate**. Its ZIP is a deterministic inspection artifact, not a DOI-backed archival release. The package intentionally excludes FARSITE; copied IEEE/PYPOWER/MATPOWER files; upstream source snapshot files; and un-cleared fuel, weather, landscape, and historical-output files.

See `docs/reproduction-boundary.md` for the distinction between validation of the distributed derivative and a future independent clean-room regeneration gate.
