# Phase 0 execution plan: scoping, audit, and decisions

## Objective

Establish what exists, what may be released, and the bounded claim for Dataset v1.0.0.

## Scope boundary

In scope: the synthetic georeferenced IEEE 30-bus wildfire co-simulation benchmark described by Sohrabi et al. (IEEE Access, 2024, DOI: 10.1109/ACCESS.2024.3439724), its reproducible data/code pipeline, and a peer-reviewed data descriptor.

Out of scope until a post-gate v1.1 decision: a geographically accurate operational network, real-time fire prediction, live grid operations, or unapproved third-party data redistribution.

## Work packages and acceptance tests

1. **Asset inventory** — Inventory source repo and lab-storage assets; record path, cryptographic checksum, size, provenance, version, license, releasability, and custodian. *Pass: each intended release file has known provenance and compatible license.*
2. **Decision record** — Resolve case variant, coordinate rules, license strategy, repository/DOI provider, target venue, and stable IDs. *Pass: PI-signed decisions.*
3. **Related-work matrix** — Verify at least four comparator records and document three concrete differentiators. *Pass: no row relies only on search snippets.*
4. **Rights/compliance memo** — Confirm funder, institution, coauthor, and upstream conditions in writing. *Pass: evidence or named blocker for every category.*
5. **Venue checklist** — Capture data-availability, technical-validation, format, and size rules from official instructions. *Pass: ranked shortlist with URLs and access date.*
6. **Authorship and CRediT** — Draft contribution/competing-interest/funding input for human review. *Pass: authors review and approve.*

## Phase-0 gate evidence

- `asset-inventory.csv`
- `decision-record.md`
- `related-work-matrix.csv`
- `rights-compliance-memo.md`
- `venue-requirements.md`
- `authorship-credit.md`
- `../gates/phase_0.md`

## Escalation rules

- License conflict, missing upstream provenance, or missing permission: mark affected asset **hold—do not release**.
- Material disagreement with source-paper outputs: record in `docs/discrepancies.md`; do not overwrite results.
- Any scope extension: record in `docs/v1.1-backlog.md`; do not add it to v1.0.0 without a new PI-approved gate.
