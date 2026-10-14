# Project status and agent board

**Last updated:** 2026-10-11  
**Authoritative scope:** `docs/project-guideline-v1.0.md`  
**Current phase:** Phase 0 — gate packet ready for independent review; spatial-layer technical-validation foundation active  
**Gate state:** Ready for independent review

## Phase 0 work board

| ID | Work package | Owner | State | Completion evidence / next dependency |
|---|---|---|---|---|
| P0-WP01 | Workspace and governance controls | Main coordinator | Complete | Workspace validator passes; guideline checksum, templates, and monitor exist. |
| P0-WP02 | Related-work comparison | Main coordinator after Research agent A | Complete | `docs/phase-0/research/related-work-matrix.md`; 5 comparators and 3 differentiators; main-reviewed. |
| P0-WP03 | Rights and compliance reconnaissance | Main coordinator | Internal approval recorded; external terms routed | `docs/phase-0/pi-asset-authorization.md`; direct case/FARSITE redistribution terms remain open. |
| P0-WP04 | Data-descriptor venue screening | Main coordinator | Complete—official-source refreshed | `docs/phase-0/venue-requirements.md`; Scientific Data remains provisional first choice; Zenodo release design is bounded by the recorded policy. |
| P0-WP05 | Asset inventory and source audit | Main coordinator | Complete for pinned snapshot; release routing defined | `docs/phase-0/igrefire-asset-routing-audit.md`; the source snapshot itself remains non-release and contains no archived outputs. |
| P0-WP06 | PI decisions and sign-off | Behrouz Sohrabi | Decisions recorded; gate packet in preparation | `docs/phase-0/scope-freeze.md`; the project-authored spatial layer is packaged; independent Phase 0 review remains. |

## Completed evidence

- Workspace scaffold, Phase-0 controls and gate template: **main-verified**.
- Governing guideline copied unchanged and SHA-256 captured: **main-verified**.
- IGREFire audit snapshot cloned and pinned to commit `194b15e2423e824a9a4447cb83c8e1cbef84dd0a`: **main-verified**.
- IGREFire file manifest generated: 159 tracked files, 91,024,976 bytes: **main-verified**.
- Grid source audit: **main-verified preliminary evidence** — 30 points, 41 branches, 34 `BRANCH` + 7 `LINK`; the project-owned canonical spatial-layer build and release manifest remain to be completed.
- Comparator hardening: **main-verified** — 12 focused comparator regressions and 19 repository tests pass; schema validation and evidence-preserving diffs are implemented.
- External fire tooling and data are explicitly excluded from the public package unless separately cleared.
- Reproducibility architecture audit: **main-reviewed recommendation** — native FARSITE is macOS-arm64-only in the snapshot; portable locked environment, manifests, and CI do not yet exist.
- Static compilation passed; the sole placeholder test passed only under a modern compatibility environment, not a reproducible locked environment: **main-verified with limitation**.

## Coordination rules

- An agent result is **reported**, not accepted, until the main coordinator verifies its sources/artifact.
- Agents must report unknowns and blockers rather than infer facts.
- Do not acquire restricted data, publish files, contact institutions/coauthors, mint a DOI, or submit work without explicit PI authorization.
- New ideas are logged for v1.1 after Phase 0 scope freeze.

## Current execution boundaries

- No further PI approval is pending for the project-authored benchmark layer.
- The remaining gate work is mechanical: create and validate the manifest, schema, data dictionary, and clean-room release contents.
- Do not claim or ship any unverified legacy fire outputs.
- FARSITE, copied IEEE/PYPOWER files, and third-party data remain excluded unless their applicable release terms are independently documented.

## Next coordinator checkpoint

Build and test the machine-readable release manifest and spatial-layer validation package; then prepare the Phase 0 evidence packet for independent review.
