# Phase 0 scope freeze

**Decision date:** 2026-10-11  
**Owner:** Behrouz Sohrabi  
**Status:** Active. New features belong to v1.1 unless recorded as a decision change.

## Technical baseline

- Preserve the IGREFire study case for v1.0.0 and create a parameter-by-parameter diff to the paper's reference case.
- Electrical topology is authoritative. Branch 24 is `19 -> 20`, rating 32 MVA.
- The principal v1.0 contribution is the technically validated, reusable georeferenced IEEE 30-bus spatial system: bus locations, branch routes, stable IDs, topology crosswalks, and reproducible spatial-quality controls. Wildfire/grid pipelines are illustrative downstream applications, not the core manuscript claim.
- Retain standard electrical parameters. The spatial placement is a new illustrative research mapping, not a representation of a real utility network. Length-scaled reactance is deferred to v1.1.
- The release must state: "This is a synthetic research benchmark for comparing methods. The network placement and line routes are illustrative and do not represent any real utility asset or location. It is not for operational wildfire prediction, transmission planning, or real-grid decision-making."
- The project-authored georeferencing layer is released under CC BY 4.0; code is released under MIT. Third-party materials remain excluded unless separately cleared and documented.

## Release and rights

**Release candidate scope:** spatial layer only; all other payloads are omitted.
- Use a manifest-first release: project-authored code, schemas, documentation, checksums, and cleared outputs may be released.
- Do not bundle third-party inputs, executables, or IEEE Access text/figures without written clearance. If not cleared, distribute a source pointer, access date, checksum, and download/regeneration script instead.
- Behrouz Sohrabi owns the project; funder: none. University of Denver approval is confirmed by PI authorization recorded in `docs/phase-0/pi-asset-authorization.md`.
- Code license: MIT. Data license is deferred until input-level rights review completes.
- Provisional clearance review deadline: 2026-10-25; any extension requires a written decision-log entry.

## Simulation, publication, and roles

- Freeze archived original outputs; if present, checksum them. Rerun a stratified sample of at least 206 scenarios on a documented macOS-arm64 runner. If outputs are absent, prepare a full-rerun compute plan.
- Release final perimeters for all 4,116 scenarios; include other bulk outputs only if already available and within the repository size budget. Include one six-weather-condition time-resolved demonstration ignition.
- Provisional venue: *Scientific Data*. Recheck ESSD scope before treating it as a fallback; *Data in Brief* is the practical alternative.
- Repository and DOI provider: Zenodo. Author: Behrouz Sohrabi. An independent verifier remains required before final release.
