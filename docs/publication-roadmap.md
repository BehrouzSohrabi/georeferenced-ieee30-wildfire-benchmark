# Publication and archival-release roadmap

## Objective

Publish a citable archival release of the project-authored, synthetic georeferenced IEEE 30-bus spatial layer and submit an evidence-gated IEEE-format manuscript describing its construction, validation, scope, and reuse boundaries. The wildfire/grid workflow remains an illustrative consumer, not the dataset’s core validity claim.

## Current verified position

- The public source repository is `https://github.com/BehrouzSohrabi/georeferenced-ieee30-wildfire-benchmark`.
- The current GitHub state is a **pre-release candidate**, not a DOI-minted archival dataset.
- Spatial integrity evidence is implemented and reported in `docs/phase-1/spatial-technical-validation.json`.
- The IEEEtran working manuscript is under `manuscript/`; it is a draft until independent technical review and venue-specific submission checks are complete.

## Release gates

1. **Independent spatial review:** A reviewer who did not author the validator reruns the release build and records a signed, commit-pinned verdict.
2. **Cold-start reproduction:** Clone the public repository in a clean environment and run the documented commands using only tracked project files.
3. **Rights and provenance closure:** Confirm that every released file is project-authored or redistributed under a documented compatible license; retain excluded third-party inputs as pointers only.
4. **Archive deposition:** Create a versioned release in an archival service that mints a DOI, attach the deterministic ZIP and `SHA256SUMS`, and update `CITATION.cff` with the DOI and release date.
5. **Release tag:** Tag the exact reviewed commit (e.g., `v1.0.0`) only after the preceding gates pass.
6. **Manuscript review:** Obtain independent power-systems/GIS review; revise against actionable concerns; select a venue only after matching its current scope and author guidelines.

## Explicitly excluded from the v1.0 spatial-layer claim

- operational wildfire prediction;
- real-utility location, corridor, planning, or reliability claims;
- FARSITE, ACOPF, risk-ranking, or scenario-performance validation;
- redistribution of third-party case, environmental, model, or article payloads without clearance.
