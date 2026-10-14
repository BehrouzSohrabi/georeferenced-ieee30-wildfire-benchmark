# Original-output archive and macOS rerun protocol

## Current evidence

The pinned IGREFire tree (`194b15e2423e824a9a4447cb83c8e1cbef84dd0a`) does **not** contain an original output archive: no `outputs/`, scenario ledger, `scenarios.csv`, FARSITE logs, perimeters, arrival-time grids, or runner/environment evidence was found. Its `.gitignore` excludes `outputs/*` and `archive/*`.

The tree contains a Mach-O arm64 FARSITE executable at `assets/FARSITE/FARSITE` (SHA-256 `156dd6b62d9f5f3bb67a26536a21856198642208197dc258a7e44eadd373870d`), but this is not proof of an original run machine and is not cleared for redistribution.

The source pipeline writes an aggregate `FARSITE.log` and then deletes perimeters and arrival-time products after a run. Therefore **do not invoke the original pipeline against a recovered archive**.

## Archive-first protocol

If original runs are recovered from lab storage, copy them byte-for-byte into a read-only archival bag before inspection. Include:

- source snapshot and Git bundle;
- original output tree, records ledger, scenario manifest, and logs;
- per-scenario `.run`, `.input`, `.raws`, ignition shapefile plus sidecars, landscape and weather inputs;
- sorted SHA-256 manifest with normalized relative paths, byte size, content type, and source location;
- a machine-readable `archive-manifest.json` with archive ID, source commit, scenario IDs, inputs, outputs, checksums, status, known gaps, and runner evidence references.

If no original archive can be located, label future execution a **reconstruction**, not a rerun.

## Minimum 206-scenario rerun design

Build the population from the frozen original scenario manifest. Stratify by six weather conditions (`Fall`, `Summer`, `Wind-N`, `Wind-E`, `Wind-S`, `Wind-W`) and 41 line IDs. Select exactly 206 scenarios deterministically:

1. Select five distinct weather-condition scenarios for each line (205 selections).
2. Allocate omitted weather conditions cyclically so condition counts differ by at most one.
3. Add one sixth-condition selection from the omitted strata with the lowest deterministic SHA-256 score **among conditions underrepresented after step 2**, preserving the at-most-one count difference.
4. Within each line/weather stratum choose the candidate minimizing `SHA256("IGREFire-rerun-v1|<scenario_id>|<frozen-manifest-sha256>")`.
5. Release `selection.csv` with all candidate scores, ranks, eligibility, selected flag, and replacement reasoning.

### Implemented selector

`src/scenario_selection.py` is a Python-standard-library-only implementation. It accepts a frozen UTF-8 CSV with required `scenario_id`, `line_id`, and `weather_id` columns, calculates the SHA-256 of the exact manifest bytes, and rejects duplicate scenario IDs, unsupported weather IDs, blank identifiers, and any line missing one of the six required weather strata. The score is exactly `SHA256("IGREFire-rerun-v1|<scenario_id>|<frozen-manifest-sha256>")`.

For a 41-line production manifest, run:

```text
python scripts/select_validation_scenarios.py path/to/frozen-scenario-manifest.csv path/to/selection.csv
```

The script requires 41 distinct line IDs by default, emits all candidates rather than only selected rows, and prints the frozen manifest SHA-256. Lines are sorted by `line_id`; cyclic omissions use the documented weather order above. The sixth selection is the minimum score among the omitted strata belonging to the currently underrepresented weather conditions, preserving final condition-count balance (difference at most one). Its output columns are `scenario_id`, `line_id`, `weather_id`, `manifest_sha256`, `score`, `rank`, `eligibility`, `selected`, `selection_reason`, and `replacement_reason`. No source manifest or selection was created here because the original-output archive is absent.

Each rerun must use an isolated directory and retain all raw products before cleanup. Capture command arguments, stdout/stderr, start/end UTC, exit code, environment hash, and SHA-256 inventory. For final perimeters report area, centroid displacement, IoU, symmetric difference, Hausdorff/boundary distances. For intensity grids report coverage, RMSE, MAE, bias, correlation, and burned-area IoU.

## Required macOS-arm64 runner evidence

At execution time record `sw_vers`, `uname -a`, arm64 capability, sanitized hardware/software profile, locale/timezone, Python version and locked environment, exact Git commit/status, FARSITE binary hash and inspection (`file`, `codesign`, `spctl`, `otool -L`), command transcript, and per-scenario status/logs.
