# IGREFire source snapshot audit

**Audit date:** 2026-10-11  
**Source URL:** https://github.com/BehrouzSohrabi/IGREFire  
**Pinned commit:** `194b15e2423e824a9a4447cb83c8e1cbef84dd0a`  
**Commit timestamp:** 2023-07-13T13:51:37-06:00  
**Clone location:** `sources/IGREFire` (local working copy; do not edit as a release artifact)

## Confirmed contents

- 159 tracked files and 15 commits at the captured revision.
- Georeferenced network artifacts: two GeoJSON files and IEEE 30-bus Python case variants.
- Landscape inputs: four `.lcp` files at 30, 60, 90, and 120 m; the 30-m file is 61,174,484 bytes.
- Historical weather CSVs for 2021 summer and fall.
- FARSITE templates and a bundled `assets/FARSITE/FARSITE` executable.
- Bundled PYPOWER source and an interactive Python analysis pipeline.

## Initial audit findings

1. **No repository `LICENSE` file was found.** The README's MIT statement is not evidence of an included license. Do not redistribute any copied source/data/binary pending an explicit rights decision.
2. The README contains release-blocking template placeholders, including a fake DOI, `Your Name`, an incomplete author list, unspecified dependency versions, and `https://....`.
3. The repository includes a `.DS_Store` file; it must not enter the clean dataset release.
4. Its only discovered test is a placeholder assertion. It exercises imports but does not validate benchmark calculations.
5. Static `compileall` passed. The sole unit test passed only in a modern compatibility environment (`pandas 2.2.3`, `pyproj 3.6.1`, `shapely 2.0.6`) while the runner still inherited NumPy 2.4.6. That confirms only the placeholder test can import the code—not reproducibility of the pinned 2023 requirements. A clean lockfile/container is required.
6. FARSITE binary provenance, version, license, and redistribution rights are unverified. Treat it as a restricted audit artifact, not a candidate release file.

## Next actions

- Generate and retain `igrefire-source-file-inventory.csv` with a hash for every snapshot file.
- Extract the 30-bus geometry and case metadata into clean candidate release layers; preserve source-to-derived provenance.
- Validate topology, CRS, branch classification, length, and ACOPF behavior independently.
- Obtain PI/coauthor/institution approval and upstream licenses before releasing any inherited files.
