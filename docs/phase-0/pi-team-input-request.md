# PI/team decision request — Phase 0 scope freeze

**Project:** Georeferenced IEEE 30-Bus Wildfire Benchmark  
**Decision deadline:** Before Phase 1 release-quality curation begins  
**Reply format:** Answer each item with **Approve / Choose / Hold / Need more information**, plus a short rationale and any supporting link or document.

## A. Scope and canonical technical sources

1. **Canonical IEEE 30-bus case:** Which exact file/version is authoritative for v1.0.0?
   - Current candidates: IGREFire `data/grid/IEEE_30_bus_system.py`, the costs/piecewise variants, MATPOWER `case30`/`case_ieee30`, or ICSEG.
   - Confirm whether the project should preserve the source-study case exactly or create a documented derivative.

2. **Canonical geographic network geometry:** May the project use the IGREFire base GeoJSON as the starting candidate, with an independently generated canonical release layer?
   - The base and labeled GeoJSON variants disagree on branch 24’s `tbus`; identify the correct endpoint or authorize resolution against the chosen electrical case.
   - Confirm the intended interpretation of 34 `BRANCH` versus 7 `LINK` features.

3. **Electrical-parameter policy:** Approve either:
   - **A:** retain standard electrical impedances; geography is topology/visualization only; or
   - **B:** add a separately labelled experimental variant that scales reactance with line length.

4. **Benchmark claim boundary:** Approve this intended-use statement: *synthetic research benchmark for method comparison; not an operational wildfire forecast, transmission-planning model, or real-grid decision tool.*

## B. Rights, release, and data-availability architecture

5. **Release architecture while rights are checked:** Approve a default **manifest-first** public design:
   - publish project-authored code, schemas, documentation, tests, and independently cleared/generated outputs;
   - do **not** bundle inherited IEEE case files, LANDFIRE/NSRDB data, FARSITE binary, or article figures/text unless item-level rights are documented;
   - provide acquisition/regeneration instructions and provenance hashes for excluded third-party inputs.

6. **Permissions owner and evidence:** Name the person/office responsible for confirming, in writing:
   - USDA grant 22-CS-11221636-121 data-sharing conditions;
   - University of Denver, Quanta Technology, and Pyrologix IP/release requirements;
   - coauthor approval for public release;
   - rights for the exact chosen IEEE case, FARSITE distribution, LANDFIRE products, and NSRDB extracts.
   Supply existing approvals/terms if available.

7. **Provisional licenses:** Subject to the rights review, approve or change these provisional choices:
   - project-authored code: BSD-3-Clause or MIT;
   - project-authored data/documentation: CC BY 4.0;
   - third-party assets: excluded until their exact terms permit inclusion.

## C. Computing and reproducibility

8. **FARSITE execution path:** The snapshot’s bundled binary is macOS arm64 and cannot run on the Windows build host. Choose the authorized route:
   - a documented macOS-arm64 native runner;
   - a separately licensed/supported Windows or Linux FARSITE environment;
   - defer full FARSITE reruns and first build portable grid/metadata/ACOPF layers only.
   Name the environment owner and confirm access to it.

9. **Output-retention and compute budget:** Approve whether v1.0.0 archives final perimeters only (recommended baseline) or also arrival-time/intensity/time-resolved outputs; identify storage/repository size constraints and compute ownership for 4,116 scenarios plus the 5% rerun sample.

## D. Publication and governance

10. **Target venue:** Approve **Scientific Data — Data Descriptor** as the provisional target, with **ESSD** as the fallback if Earth-system framing dominates; or select another venue.

11. **Repository / DOI provider and embargo:** Choose Zenodo, Figshare, an institutional repository, or another provider. State whether deposit must remain private/embargoed until acceptance.

12. **People and sign-off:** Name:
   - PI/project lead and final decision authority;
   - grid-modeling lead;
   - fire-modeling lead;
   - data steward;
   - corresponding author;
   - independent verifier who did not build the dataset.
   Also provide preliminary CRediT roles, ORCIDs if available, funding text, and competing-interest wording (including Quanta/Pyrologix affiliations).

## Known technical facts requiring acknowledgement

- The source has 30 points and 41 branches (34 `BRANCH`, 7 `LINK`).
- Source geometry requires canonicalization; branch 24 differs between two GeoJSON variants.
- Haversine screening gives 683.737 km for the 34 branches; EPSG:3310 recomputation and reconciliation to the paper’s 702 km are still required.
- No release claim is being made for inherited inputs or executable assets.

## Reply template

```text
1. Canonical case: ...
2. Canonical geometry / branch 24: ...
3. Electrical policy: A / B / other
4. Intended-use statement: approve / edits
5. Manifest-first release architecture: approve / edits
6. Rights owner and existing approvals: ...
7. Provisional licenses: ...
8. FARSITE execution route and owner: ...
9. Archive scope / compute / storage: ...
10. Target venue: ...
11. Repository, DOI, embargo: ...
12. Roles, independent verifier, CRediT/funding/COI: ...
```
