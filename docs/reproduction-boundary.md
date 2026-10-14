# Reproduction boundary and cold-start protocol

## What this release reproduces now

A clean checkout of this repository can reproduce the **release-integrity and spatial-validation checks** for the distributed project-authored derivative:

```bash
uv run --with-requirements requirements.txt --with pytest pytest -q
uv run --with-requirements requirements.txt python scripts/validate_spatial_layer.py
python scripts/validate_release_package.py
```

The expected spatial technical-validation report is committed at `docs/phase-1/spatial-technical-validation.json`. The distributed GeoJSON, schema, manifests, validator, tests, licenses, and archive are included in the pre-release package.

## What this release does not yet claim

The project does **not** claim a clean-clone regeneration of `canonical-network.geojson` from upstream inputs. The builder depends on two source files from the pinned IGREFire snapshot that are deliberately excluded from this repository and release archive while their redistribution status is reviewed. The precise upstream URL, commit, expected source hashes, builder hashes, and transformation rules are recorded in `data/network/provenance.json`.

## Future cold-start regeneration gate

Before calling a future release regeneration-reproducible, an independent reviewer must:

1. obtain the upstream snapshot lawfully at the recorded commit;
2. verify the two input-file SHA-256 values in `data/network/provenance.json`;
3. use the recorded builder/library revisions and documented parameters;
4. regenerate the candidate GeoJSON in a clean environment;
5. compare its digest and validation report with the declared output; and
6. record any divergence, environment details, reviewer identity/role, and disposition in a signed release-review record.

No upstream payload should be copied into this repository or distributed archive unless an explicit rights review authorizes it.
