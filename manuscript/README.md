# IEEE-format working manuscript

This directory contains an evidence-gated IEEEtran manuscript for the project-authored **georeferenced IEEE 30-bus spatial layer**. It is a working draft, not a submission-ready manuscript.

## Scope

The manuscript reports only verified spatial-layer evidence: the 30 synthetic bus points, 41 synthetic branch routes, ID/topology crosswalks, schema and manifest, EPSG:3310 spatial QA, release checksums, and documented limitations. It treats wildfire--grid simulations as optional downstream use, never as the principal dataset claim.

## Contents

- `ieee30_spatial_benchmark.tex` — IEEEtran manuscript source.
- `references.bib` — cited, reviewable references.
- `figures/spatial-layer-map.{pdf,png}` — evidence-derived map from the canonical GeoJSON.
- `figures/release-workflow.{pdf,png}` — conceptual release-control workflow.
- `ieee30_spatial_benchmark.pdf` — compiled working-draft PDF.

## Rebuild

1. Install a TeX distribution with `IEEEtran`, `booktabs`, `amsmath`, and standard graphics support (MiKTeX was used for the checked build).
2. From the repository root, run `python scripts/generate_manuscript_figures.py` using `requirements.txt`.
3. From this directory, run `pdflatex ieee30_spatial_benchmark.tex`, `bibtex ieee30_spatial_benchmark`, then run `pdflatex` twice more.

The checked draft builds to three pages without LaTeX errors or unresolved citation placeholders. Its bibliography and author/affiliation/funding metadata still require final scholarly and institutional review before submission.
