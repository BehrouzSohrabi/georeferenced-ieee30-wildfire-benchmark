# Independent read-only Phase 2 wildfire-input / FARSITE audit

**Scope audited:** `C:\Users\Polinomy\Documents\research\georeferenced-ieee30-wildfire-benchmark\sources\IGREFire`  
**Method:** inspected repository files, binary headers, CSV structure, source, templates, notebooks, and git-tracked state. **Did not execute FARSITE, modify files, or download data.**

## Present inputs and artifacts

### Landscape

| Exact path | Size | Observed format / metadata |
|---|---:|---|
| `data/landscape/IEEE_30_bus_system_resolution_30.lcp` | 61,174,484 B | Binary FARSITE LCP; header-derived 30 m grid, **2062 × 1854**; bounds (LCP-coordinate metres) `[-30911.389836, -27770.387402, 30948.610164, 27849.612598]` |
| `data/landscape/IEEE_30_bus_system_resolution_60.lcp` | 15,330,452 B | Binary FARSITE LCP; 60 m, **1032 × 928**; bounds `[-971.389836, -800.387402, 60948.610164, 54879.612598]` |
| `data/landscape/IEEE_30_bus_system_resolution_90.lcp` | 6,831,172 B | Binary FARSITE LCP; 90 m, **689 × 619**; bounds `[-971.389836, -800.387402, 61038.610164, 54909.612598]` |
| `data/landscape/IEEE_30_bus_system_resolution_120.lcp` | 3,845,524 B | Binary FARSITE LCP; 120 m, **517 × 464**; bounds `[-31.389836, -740.387402, 62008.610164, 54939.612598]` |
| `data/landscape/IEEE_30_bus_system_resolution_90.prj` | 453 B | NAD83 / Albers WKT: central meridian `-120.35`, standard parallels `37.6`, `38.1`, latitude of origin `37.85`, metre units. |
| `data/landscape/IEEE_30_bus_system_resolution_90.lcp.aux.xml` | 1,192 B | FlamMap6-created PAM metadata; eight bands: Elevation (m), Slope (deg), Aspect (deg), Fuel Model (class), Canopy Cover (%), Stand Height (m×10), Canopy Base Height (m×10), Canopy Bulk Density (kg/m³×100). |

**Important evidence limits:** only the **90 m** LCP has a `.prj` and `.aux.xml`. No sidecar CRS/layer/unit metadata accompanies 30/60/120 m LCPs. The four LCP header extents are not identical, so their mutual alignment is **not established** merely from filenames/resolution.

### Grid / potential ignition source

| Path | Size | Evidence |
|---|---:|---|
| `data/grid/IEEE_30_bus_system.geojson` | 58,421 B | 71 features: 30 points and 41 lines; 34 lines have `properties.type == "branch"` with IDs `1–10, 17–35, 37–41`. No declared CRS member; GeoJSON coordinates span `[-120.644907978, 37.637515861, -120.035673650, 38.056803427]`. |
| `data/grid/IEEE_30_bus_system_labeled.geojson` | 115,873 B | Same feature and coordinate extent counts; extra labels/properties. |

### Weather source CSVs

| Exact path | Size | Data period / cadence | Wind metadata |
|---|---:|---|---|
| `data/weather/38.45_-120.90_2021_summer.csv` | 309,626 B | 2,208 rows, 2021-07-01 00:30 through 2021-09-30 23:30; hourly records at `Minute=30` | NSRDB v3.2.2 metadata says degrees and m/s. Direction values `2–353`; speed `0.5–4.2 m/s`. |
| `data/weather/38.45_-120.90_2021_fall.csv` | 308,717 B | 2,208 rows, 2021-10-01 00:30 through 2021-12-31 23:30; hourly records at `Minute=30` | NSRDB v3.2.2 metadata says degrees and m/s. Direction values `1–358`; speed `0.2–6.5 m/s`. |

Both files state `Source=NSRDB`, location `38.45, -120.9`, time zone/local time zone `-8`, elevation `212`, and include `Year, Month, Day, Hour, Minute, Temperature, Relative Humidity, Precipitable Water, Wind Direction, Wind Speed, Cloud Type` plus radiation fields. There are no missing values in the inspected six FARSITE-relevant columns.

**Wind convention:** source metadata establishes numeric **degrees** but does **not** explicitly state “from” versus “to” in this repository. The code passes/rounds the source `Wind Direction` directly into RAWS; no direction conversion is evidenced. A commented synthetic example assigns `N=0`, `E=90`, `S=180`, `W=270`, but this is not a documented source-wind convention.

### FARSITE executable and templates

| Path | Size | Evidence |
|---|---:|---|
| `assets/FARSITE/FARSITE` | 1,610,248 B | Mach-O 64-bit **arm64** executable—not a Windows executable. No executable version/provenance manifest is present. |
| `assets/templates/FARSITE_raws` | 81 B | Metric RAWS template with elevation and row-count placeholders. |
| `assets/templates/FARSITE_input` | 801 B | Input template with configurable timestep/resolutions, fixed spotting controls, and `SPOTTING_SEED: 253114`; fixed `NUMBER_PROCESSORS: 4`. |
| `assets/templates/FARSITE_run` | 60 B | Six-field run template: landscape, input, ignition, barrier, output dir, terminal `0`. |

No generated `FARSITE.raws`, `FARSITE.input`, `FARSITE.run`, ignition Shapefile, scenario table, FARSITE output raster, or FARSITE log is tracked/present. `.gitignore` excludes `outputs/*`.

## What can be regenerated from source (but is not present)

`src/inputs.py` can construct, from an explicit `Config`:

1. ignition polygon Shapefiles along branch lines;
2. FARSITE RAWS files from either the two CSVs or synthetic conditions;
3. FARSITE input files from `FARSITE_input`;
4. one `FARSITE.run` per ignition × weather combination;
5. an intended scenarios CSV.

For CSV weather, the generator selects `farsite_start : farsite_start + farsite_burn_periods`, emits year/month/day/hour, formats the source’s 30-minute records as `HH00`, rounds wind speed and direction, divides precipitable water by 100, and maps cloud type by a local lookup table. Source defaults in `src/config.py` are: 60 m landscape, bounds `[-120.7, 37.6, -120, 38.1]`, timestep 240 min, start row 0, 24 burn-hour rows, and one fuel-moisture row `[[0,6,7,8,60,90]]`.

This is **not sufficient to reproduce a prior benchmark run**: no `outputs/records.csv`, saved `scenarios.csv`, committed config, input manifest, generated RAWS, ignition files, or run logs exist.

## Determinism / operational findings

- **Some determinism is configured:** template seed `253114` and fixed FARSITE controls are present.
- **Not fully established:** binary version/build/hash, FARSITE platform/version, full run configuration, exact input file hashes, environment, and output checksums are absent. Fixed `NUMBER_PROCESSORS: 4` also needs documented validation for cross-host repeatability.
- **Synthetic weather is not reproducible as a dated stream:** `src/inputs.py:153` bases its start date on `datetime.now()`. In the current helper implementation, temperature/humidity/wind-speed functions return constants before their random code, but dates still vary with execution day.
- **FARSITE runner evidence is inadequate for Phase 3:** `src/FARSITE.py` appends stdout/stderr to a shared log but does not record command exit codes, binary identity, input hashes, or per-scenario success status. It removes many output files after a run, including `_ArrivalTime*`, while `notebooks/visualization.ipynb` references `_ArrivalTime.asc`.
- **Operational blocker:** the only bundled FARSITE executable is arm64 Mach-O, while the audit host is Windows 10. It is not directly runnable on this host.
- **Additional source blocker:** `Config.save_scenarios()` calls `update_record(scenarios=...)`, but records use the field `scenarios_rows`; `update_record` rejects unknown columns. As written, that is a likely `KeyError` before scenario CSV saving unless the code/record schema differs at execution time.
- **Barrier default ambiguity:** the default `barriers_file` is `None`, but run-template generation writes `0` only when it is exactly `''`; a default run may render `None` as the barrier token.

## Phase 2 / Phase 3 pass-criteria gap assessment

| Criterion | Status from repository evidence | Gap |
|---|---|---|
| Layer alignment | **Not demonstrated** | Topology is geographic GeoJSON without declared CRS; only 90 m LCP has Albers CRS metadata; other LCPs lack sidecars; no transformation/control-point/alignment report; ignition Shapefiles would be generated without a `.prj`. |
| 686 ignitions | **Not demonstrated** | No generated ignition Shapefiles, ignition inventory, scenario CSV, or saved `ignition_points_distance/number` setting. Code can generate a variable count over 34 branch features. |
| 6 weather conditions | **Not demonstrated** | Exactly two source CSVs exist. No six-condition manifest/config exists. Defaults define two synthetic directions (`N`,`S`); a commented example gives four directions, not six. |
| 4,116 scenarios | **Arithmetic target consistent** | `686 × 6 = 4,116`, but no generated scenario table verifies the count or its one-to-one mapping. |
| Logged, reproducible FARSITE runs | **Not demonstrated / blocked** | No outputs/logs tracked; runner logging lacks provenance and exit status; bundled binary is incompatible with the Windows audit host. |

## Minimum acquisition and metadata plan

1. **Freeze a run manifest** (CSV/JSON/YAML under version control): benchmark ID, exact LCP selected, CRS, header bounds/dimensions/resolution, topology file and CRS, 686 ignition IDs/coordinates/radii, six named weather conditions, FARSITE options, fuel moistures, crown method, barrier policy, and expected `4,116` rows.
2. **Provide authoritative spatial metadata:** `.prj` and layer/unit descriptions for **every** LCP; document whether all landscape layers are co-registered; publish a tested GeoJSON-to-LCP coordinate transformation and an alignment/control-point report.
3. **Provide/record raw input provenance:** source URLs or acquisition identifiers where permitted, acquisition dates, licenses/rights determination, and cryptographic hashes for landscapes, topology, weather CSVs, templates, executable, generated RAWS, ignition Shapefile component sets, and run files. This audit makes **no redistribution-rights claim**.
4. **Commit or archive generated Phase 2 evidence:** `records.csv`, scenario table, six RAWS/input files, all ignition Shapefile components (including `.prj`), exact run files, and a count-validation report proving 686/6/4,116.
5. **Use a supported, pinned FARSITE environment:** record executable release/build/hash and OS/container; validate fixed seed/processor behavior; retain per-scenario command, start/end time, exit code, stdout/stderr, and output checksums. Do not delete benchmark-required output rasters.
6. **Fix or document generator behavior before claiming reproducibility:** resolve `scenarios` vs. `scenarios_rows`, explicit no-barrier token, weather timestamps/minute handling, wind-direction convention, and synthetic date behavior.

## Files changed

**None.**