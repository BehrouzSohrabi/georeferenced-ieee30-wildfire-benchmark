# IGREFire reproducibility and test-architecture audit

**Scope:** read-only audit of the pinned source snapshot and the governing project guideline.  
**Snapshot observed:** Git commit `194b15e2423e824a9a4447cb83c8e1cbef84dd0a` (“changed formulations”, 2023-07-13); working tree was clean after the audit. No files were changed, no packages installed, and FARSITE was not run.

## Observed evidence

### Entry points and execution flow

| Area | Evidence observed |
|---|---|
| Interactive application entry point | Root `main.py` documents and implements `python main.py`. It collects configuration interactively, then allows progressive or selected-stage execution. The README says `python main.py` launches a GUI, but the actual root entry point is terminal-interactive; `src/GUI.py` is a stub. |
| Pipeline orchestration | `src/main.py:Analysis.run()` executes: input generation → FARSITE → MATPOWER preparation → AC/DC OPF → report. |
| Fire simulation | `src/FARSITE.py` constructs `./assets/FARSITE/FARSITE <run_dir>FARSITE.run`, invokes it with `subprocess.run(..., shell=True)`, and appends stdout/stderr to a generated FARSITE log. |
| Grid/impact processing | `src/MATPOWER.py` reads FARSITE intensity rasters or an alternate impact file, determines affected branches/nodes, then writes modified PYPOWER-style case files. |
| Power system solving | `src/powerflow.py` imports vendored `assets.pypower.runopf.runopf` for ACOPF and `assets.pypower.rundcopf.rundcopf` for DCOPF. |
| Inputs | `src/inputs.py` generates ignition files, weather stream files, FARSITE input files, run files, and scenario records. |
| Case data | `data/grid/IEEE_30_bus_system.py` defines 30 buses, six generators, and **41 branches**. `IEEE_30_bus_system_costs.py` contains georeferencing-related branch-length comments but needs independent validation against the guideline’s line/link classification. |

### Dependencies and pins

| Area | Evidence observed | Reproducibility assessment |
|---|---|---|
| Direct Python requirements | `requirements.txt` pins 11 packages exactly: `pyinstaller==3.4`, `requests==2.28.2`, `fbs==1.1.9`, `numpy==1.24.2`, `shapely==2.0.1`, `pyproj==3.4.1`, `pyshp==2.3.1`, `pandas==1.5.3`, `pandastable==0.13.1`, `rasterio==1.3.6`, `scipy==1.10.1`. | Direct pins are a useful starting point, but there is no Python-version pin, transitive dependency lock, wheel hashes, OS package manifest, or resolver artifact. |
| Additional imported libraries | Application imports also include `geopandas` (`src/report.py`) and `shapefile`/PyShp (`src/inputs.py`). | `geopandas` is imported but is not directly declared in `requirements.txt`; it may arrive transitively, which is not a reproducible dependency declaration. |
| OPF dependency | Vendored PYPOWER reports version **5.1.4**, dated 2018-06-27, at `assets/pypower/ppver.py`. | This conflicts with README text claiming “PyPower version 1.2.3.” The vendored source revision/license and its relation to an upstream source should be recorded. |
| Packaging / lock assets | Only `requirements.txt` was found. No `pyproject.toml`, `setup.py`, `setup.cfg`, `Pipfile.lock`, `poetry.lock`, `conda` environment/lock, Dockerfile, Compose file, or CI workflow was found. | Not presently clean-machine reproducible. |

### Operating-system assumptions and external executables

| Area | Evidence observed | Implication |
|---|---|---|
| FARSITE executable | `assets/FARSITE/FARSITE` is a **Mach-O 64-bit arm64 executable** (not Windows or Linux). SHA-256: `156dd6b62d9f5f3bb67a26536a21856198642208197dc258a7e44eadd373870d`. | The snapshot cannot execute its bundled FARSITE binary on the Windows audit host. It is also not portable to standard Linux CI. |
| Hard-coded executable path | `src/config.py:56` sets `self.FARSITE = './assets/FARSITE/FARSITE'`. | Assumes project-root current working directory and a compatible executable at that relative path. |
| Process invocation | `src/FARSITE.py:19–25` uses a shell-formatted command with `shell=True`; output is redirected manually. | Path quoting and shell behavior are OS-sensitive. The return code is not checked. |
| File/path conventions | The README provides Windows and macOS/Linux virtual-environment activation commands. Code primarily uses forward-slash relative paths. | Documentation recognizes multiple OSes, but executable availability currently does not. |
| FARSITE configuration | `assets/templates/FARSITE_input` sets `SPOTTING_SEED: 253114` and `NUMBER_PROCESSORS: 4`. | There is a nominal seed, but the external program version/build and parallel determinism are not captured in a manifest. |

### Current test architecture and observed run result

| Area | Evidence observed |
|---|---|
| Test inventory | Only `test/test_config.py` was found. It imports `src.config` and asserts `None == None`; it does not exercise configuration, data, FARSITE, OPF, metrics, or outputs. |
| Test framework | Standard-library `unittest`; no `pytest` configuration, test markers, fixtures, golden data, coverage configuration, CI workflow, or test matrix exists. |
| Test execution | `python -m unittest discover -s test -v` was run read-only. It failed during discovery: `ModuleNotFoundError: No module named 'pandas'` when importing `src.config`. No assertion ran. This establishes that the audit host lacks the declared runtime environment; it does **not** establish an application logic failure. |
| Side effects | Git status remained clean after the audit/test command. No source changes were made. |

### Determinism, provenance, and logging

| Mechanism | Evidence observed | Assessment |
|---|---|---|
| FARSITE seed | Template contains `SPOTTING_SEED: 253114`. | Helpful but insufficient: it is not surfaced in a scenario/run manifest and the executable/build is not versioned in run output. |
| Python random state | `src/MATPOWER.py` calls `random.uniform()` for branch-impact probability; no `random.seed()` was found. | Nondeterministic if that code path is used. |
| Synthetic weather date | `src/inputs.py:153` anchors synthetic weather to `datetime.now()`; no run-specified start date is required. | Output dates, weather rows, generated files, and checksums can vary by run date. |
| Synthetic weather random code | `src/utils.py` contains random weather curves, although current functions return constants before those random statements. | Current behavior is effectively constant for those functions, but the dead random code makes future changes risky without explicit seed control. |
| Records and scenario status | `Config` stores a start timestamp and elapsed time in records; inputs create a scenarios CSV; stages update record status. | Useful operational tracking, but it is not the guideline-required immutable run manifest with input/output checksums, executable metadata, solver metadata, and per-scenario failure semantics. |
| Logs | FARSITE stdout/stderr append to a generated log file. Console progress/status is printed. | Captures output, but no structured log, command line/environment capture, explicit return-code gate, or log checksum was observed. |
| Output retention | FARSITE cleanup removes several file prefixes, including `_Perimeters`. | This may conflict with the guideline’s requirement that final perimeters be archived; confirm the exact FARSITE filenames and cleanup behavior before production runs. |

## Guideline requirements that drive the test plan

The governing guideline requires, among other items:

- **Phase 1:** 41 branches (34 lines, 7 links), correct endpoints; study-box and ≤1 m endpoint checks; total line length 702 km within 0.5% or explained; base ACOPF reference objective within 0.1%; valid GIS data.
- **Phase 2:** complete layer provenance/alignment; deterministic synthetic-weather checksum from a recorded seed; 686 ignitions; wind-convention fire-direction test; launchable FARSITE configuration.
- **Phase 3:** 4,116 scenario statuses, logs, runtime, checksums; ≥206 scenario reruns with perimeter-area difference ≤1% and IoU ≥0.99 (or stochastic distribution); clean-machine environment rebuild; valid perimeter geometry/CRS.
- **Phase 4:** table reproduction and discrepancy log; per-scenario convergence; bounded nonnegative curtailment; consistent zero-demand treatment; **hand-computed toy 3-bus unit tests passing in CI**; independent metric implementation agreement.

---

# Recommended future work — staged clean-environment architecture

> The items below are recommendations, **not implemented facts** about the current snapshot.

## 1. Separate portable analysis from native FARSITE execution

Use two execution profiles with the same manifest schema:

1. **Portable Python profile** — GIS validation, input generation, spatial impact rules, PYPOWER AC/DC OPF, metrics, report generation, and all unit/integration tests.  
   - Recommended baseline: a Linux `micromamba`/Conda container built from an explicit lock.
   - This is suitable for ordinary CI runners.

2. **Native FARSITE profile** — actual fire runs on a controlled **macOS arm64** executor compatible with the observed Mach-O arm64 binary, unless a separately licensed/validated Linux or Windows FARSITE build is obtained.  
   - Pin the executable SHA-256, vendor/version, platform, architecture, and all invocation settings.
   - Treat this as a separate runner image/VM specification rather than claiming the current binary is container-portable.

This avoids pretending that a Linux container can execute the bundled macOS binary while still making all non-fire computation reproducible in conventional CI.

## 2. Environment specification and lock strategy

Create these artifacts:

- `environment.yml`: human-maintained direct dependencies, Python version, Conda channels, and platform notes.
- `conda-lock.yml` (or per-platform explicit lock files): fully resolved packages for at least `linux-64` and `osx-arm64`.
- A small `requirements-dev.in`/lock only if pip-only test tools are needed; include hashes for pip artifacts.
- `containers/python/Dockerfile`: image digest-pinned base, non-root user, locale/timezone defaults, and locked environment installation.
- `docs/environment/farsite-macos-arm64.md`: native FARSITE provisioning, license/provenance, SHA-256 verification, architecture check, and acceptance command.

The first validated lock should use a Python release compatible with the pinned scientific stack; do not select a version merely by convention. Record the actual `python --version`, Conda lock digest, and OS image digest in every run.

## 3. Data manifest and immutable run manifests

Add two layers of provenance:

### Dataset manifest

`data/manifest-v1.csv` or Parquet, with at least:

```text
logical_id,relative_path,role,sha256,bytes,media_type,crs,resolution,source_url,
source_version,access_date,license,transform_script,transform_commit
```

Required roles include topology GeoJSON, grid-case source, weather inputs, LCP landscape inputs, barriers, ignition set, FARSITE templates, and reference/golden outputs.

The audit computed hashes for the current data inputs, so this can be seeded from the snapshot rather than manually transcribed. Keep derived caches and `__pycache__` out of the release manifest.

### Per-run manifest

`runs/<run_id>/run-manifest.json` plus `scenario-manifest.parquet`:

```text
run_id,scenario_id,ign_id,line_id,weather_id,stage,status,started_at_utc,
ended_at_utc,runtime_s,seed,command,exit_code,input_sha256,output_sha256,
farsite_binary_sha256,farsite_version,platform,architecture,
python_version,environment_lock_sha256,git_commit,solver,solver_options
```

Make output hashes content hashes and normalize paths/timestamps out of deterministic comparison files.

## 4. Deterministic runner design

Replace interactive production execution with a noninteractive, configuration-file-driven runner:

```text
igrefire run --config configs/benchmark-v1.yaml --stage inputs|fire|impact|opf|metrics
             --run-dir runs/<run_id> --seed <integer> --resume
```

Recommended behavior:

- Resolve every relative path against the configuration file, not process CWD.
- Require an explicit `run_id`, seed, synthetic-weather start timestamp, input manifest digest, and environment lock digest.
- Use `subprocess.run([...], check=False, shell=False)` for FARSITE; store command argv, exit code, stdout/stderr paths, and failure reason.
- Generate each scenario in an isolated scenario directory; use atomic writes and a resumable manifest state machine.
- Keep final perimeters/arrival/intensity products needed for publication; archive rather than silently delete required products.
- Canonicalize CSV/JSON/GeoPackage-derived comparison extracts before hashing.
- Enforce deterministic numeric settings: solver choice/version/options, tolerance, maximum iterations, BLAS/thread limits where needed, fixed locale/timezone (`UTC`), and thread count.
- Record a seed hierarchy, e.g., `run_seed → weather_seed, scenario_seed(scenario_id), FARSITE spotting_seed`.

## 5. CI tiers

| Tier | Trigger | Scope | Requires FARSITE? | Gate |
|---|---|---|---|---|
| **Tier 0 — static/provenance** | Every PR | Config schema, manifest schema, data-hash verification, no untracked generated data, formatting/lint/type checks if adopted | No | Fast, <5 min |
| **Tier 1 — unit** | Every PR | Phase 1–4 unit tests, including toy 3-bus ACOPF and metrics | No | Fast, <10 min |
| **Tier 2 — integration / golden** | Every PR or nightly | Small checked-in fixture: topology → ignitions/weather → mocked/precomputed fire impact → case modification → ACOPF → metrics; compare canonical golden outputs | No external executable | <20 min |
| **Tier 3 — native fire smoke** | Scheduled/manual on macOS arm64 | One or a few controlled FARSITE scenarios; validate command, status, logs, checksum/tolerance, geometry/CRS | Yes | Native executor |
| **Tier 4 — reproducibility sample** | Release candidate | ≥206 reruns (5% requirement), perimeter-area and IoU calculations, determinism report | Yes | Native executor/compute |
| **Tier 5 — full release** | Tagged release | All 4,116 scenarios, archival manifest/checksums, published-table comparison, clean-machine rebuild evidence | Yes | Native executor/compute |

### Practical first CI milestone

Implement **Tier 0 + Tier 1** first, without FARSITE:

1. Build the locked portable Python environment.
2. Run manifest/schema and topology checks.
3. Run the 3-bus ACOPF, spatial-rule, metric, and weather-determinism tests.
4. Verify that a tiny fixture’s precomputed impact data leads to stable ACOPF/metric golden outputs.
5. Publish JUnit results and the resolved-lock digest as CI artifacts.

This is the smallest milestone that directly addresses the presently nonfunctional test environment and establishes a reliable test boundary before native FARSITE automation.

---

# Concrete Phase 1–4 test matrix

| Phase | Test | Fixture / method | Expected assertion |
|---|---|---|---|
| P1 | Case topology cardinality | IEEE-30 case and canonical branch table | Exactly 41 branches; explicit 34 line / 7 link classification; each `(from_bus, to_bus)` matches canonical table. |
| P1 | Coordinate and geometry validity | Buses/branches GeoJSON | All coordinates within 37.6–38.1 N and 120.7–120.0 W; each line endpoint is ≤1 m from its associated bus; no invalid geometries. |
| P1 | Length validation | Reproject lines to EPSG:3310 | Sum line length within 0.5% of 702 km, or test reads approved discrepancy record. |
| P1 | Base ACOPF regression | Canonical chosen case and pinned solver options | Solver converges; objective is within 0.1% of the versioned reference value; solver status/options saved. |
| P1 | Case-loading safety | Valid and malformed case fixtures | Valid case loads; malformed/non-whitelisted case is rejected. Avoid arbitrary `exec` for future external case inputs. |
| P2 | Layer provenance completeness | Dataset manifest | Every required layer has version, source, access date, CRS, extent, resolution, and checksum. |
| P2 | Raster alignment | Small raster metadata fixture plus release raster metadata | All required layers have common CRS, aligned grid origin/cell size, and identical required extent. |
| P2 | Synthetic weather determinism | Fixed config, fixed start timestamp, fixed seed | Two clean runs yield byte-identical/canonical-hash-identical weather files; changing seed changes only allowed stochastic fields. |
| P2 | Ignition generation | Canonical topology and 1 km rule | Exactly 686 ignition points; per-line counts sum to 686; point distance/chainage reconciles with line length. |
| P2 | Wind convention | Tiny synthetic weather + prevalidated expected fire orientation or controlled native smoke fixture | Spread direction matches documented “from”/“toward” convention. |
| P2 | FARSITE input generation | One minimal scenario | Generated `.input` and `.run` resolve all files, preserve seed/timestep/resolution, and can be parsed by a preflight validator. |
| P3 | Scenario manifest completeness | Full generated scenario table | Exactly 4,116 unique `(ign_id, weather_id)` scenarios; no duplicate IDs; every scenario has terminal status. |
| P3 | Runner resume/idempotence | Small fixture run directory | Re-running completed work does not alter completed canonical outputs; failed scenarios record a reason and can resume. |
| P3 | Logging/provenance | One mocked/native scenario | Manifest contains command, exit code, runtime, input/output hashes, lock digest, Git commit, binary hash, seed, and log locations. |
| P3 | Native determinism sample | ≥206 release-candidate scenarios | Final perimeter-area delta ≤1% and IoU ≥0.99; otherwise versioned distribution/report for stochastic behavior. |
| P3 | Geometry/archive validation | Perimeter archive | All geometries valid, declared CRS present, expected scenario/output linkage exists, every archived output has checksum. |
| P3 | Clean rebuild | Fresh CI/container or independent machine | Locked environment creates successfully and fixture pipeline completes without preexisting outputs. |
| P4 | Spatial impact rule | Hand-drawn line/perimeter fixtures | Intersecting line marked affected; nonintersecting/touching cases follow explicitly documented rule; node rule is tested separately. |
| P4 | Case modification | Small network case | `trip` sets intended branch status out of service; `degrade` changes only specified ratings by exact factor; unaffected rows remain unchanged. |
| P4 | ACOPF convergence and bounds | Toy and IEEE-30 fixtures | Status recorded; curtailment is nonnegative and ≤ total demand; nonconvergence has defined handling. |
| P4 | Zero-demand metrics | Fixture containing zero-demand bus | Explicit denominator policy is applied consistently to risk and vulnerability, with no divide-by-zero/NaN leak. |
| P4 | Metric algebra | Hand-computed matrices | Susceptibility, risk, vulnerability, means, and weather aggregation equal manually specified expected values. |
| P4 | Independent implementation | Separate simple/reference metric function | Exact agreement for canonical fixture inputs; keep implementation independent enough to avoid shared-bug confirmation. |
| P4 | Published tables | Released intermediates/golden reference | ≥95% of entries within ±0.001; all differences emitted to a structured discrepancy log. |

## Required toy 3-bus ACOPF test

Use a deliberately lossless, uncongested three-bus ACOPF fixture so the expected active dispatch and cost are hand-computable while the solver still executes its AC formulation.

**Fixture specification**

- Bus 1: reference/generator bus.
- Bus 2: PV/generator bus.
- Bus 3: PQ load bus with `Pd = 100 MW`, `Qd = 0`.
- Lines: 1–3 and 2–3, `r = 0`, `x = 0.01 p.u.`, adequate thermal limits (e.g., ≥100 MW), voltage magnitudes fixed/limited to 1.0 p.u. for the fixture, sufficient reactive limits.
- Generator active-power bounds: 0–100 MW each.
- Costs:
  - `C1(P1) = P1² + 10P1`
  - `C2(P2) = 2P2² + 8P2`

**Hand-computed reference**

With no active losses, `P1 + P2 = 100`. Equal marginal cost gives:

```text
2P1 + 10 = 4P2 + 8
P1 + P2 = 100
```

Expected optimum:

```text
P1 = 199/3 = 66.333333333 MW
P2 = 101/3 = 33.666666667 MW
objective = 22799/3 = 7599.666666667
```

**Assertions**

1. ACOPF reports success/convergence.
2. Active balance holds within an explicitly set numerical tolerance.
3. `Pg1`, `Pg2`, and objective equal the hand result within tolerance.
4. Both generator bounds and voltage/reactive limits are satisfied.
5. Repeated solves under the locked environment produce identical solver-status and canonical numeric output within the declared tolerance.
6. A companion infeasible variant (e.g., lower generator maxima below 100 MW) reports a controlled non-converged/infeasible status and is recorded correctly rather than producing silently invalid curtailment/metrics.

## Key audit blockers before Phase 3/4 claims

1. The current bundled FARSITE binary is macOS arm64 only, while this audit ran on Windows.
2. The existing test suite is only a placeholder and could not import without the declared environment.
3. No lockfile/container/CI configuration exists.
4. No structured run/data manifest exists to meet checksum, status, runtime, or environment evidence requirements.
5. Randomness and time dependence are not centrally controlled.
6. README PYPOWER version documentation conflicts with the vendored PYPOWER version.
7. Current cleanup behavior should be checked to ensure required perimeter outputs are not discarded.

## Files created or modified

**None.** The audit was read-only.