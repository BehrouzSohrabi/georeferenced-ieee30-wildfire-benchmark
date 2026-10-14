# Pinned IGREFire asset-routing audit

**Scope:** internal source-audit clone `sources/IGREFire` at commit `194b15e2423e824a9a4447cb83c8e1cbef84dd0a` (159 tracked files; 91,024,976 bytes).  
**Audit finding:** the snapshot has no tracked `LICENSE`, `COPYING`, `NOTICE`, provenance manifest, dependency lockfile, or release outputs. Its README’s MIT claim points to no tracked LICENSE file. It is therefore an internal audit source, not a release artifact.

## Routing decisions

| Category | Evidence | Release treatment |
|---|---|---|
| FARSITE executable | `assets/FARSITE/FARSITE`; Mach-O arm64; 1,610,248 bytes; no version/supplier/license evidence | Exclude. Document its use only if relevant; provide an official acquisition pointer and user-supplied configuration route. |
| Copied IEEE/PYPOWER case assets and inherited GeoJSON | grid subtree includes case Python, 2 GeoJSON files, notebooks, and a bundled PYPOWER copy; no complete source-to-derived provenance chain | Exclude inherited copies. Release only the independently documented, project-authored georeferenced layer and regeneration/validation logic. |
| Landscape LCP rasters | four `.lcp` files plus companions; likely LANDFIRE-derived but no source-vintage or transformation record | Hold from archive until exact source/version, terms, attribution, and transformation evidence are recorded. |
| NSRDB weather CSVs | two CSVs identify NSRDB v3.2.2 but lack query/retrieval and attribution record | May be considered only after a version-specific provenance and attribution review. |
| Project-authored release package | new code, schemas, docs, tests, manifests, checksums, and independently created spatial records | Release after ownership/content review, project license, dependency lock, citation metadata, and a manifest. |
| Rerun outputs | none are tracked in the source snapshot | Do not claim or deposit outputs from this snapshot. Any future output requires cleared inputs, immutable run metadata, checksums, and independent validation. |

## Immediate conclusion

The public product is **not a repackaging of the upstream repository**. It is a clean project release centered on the new georeferenced IEEE-30 spatial benchmark and its documented, replaceable integration interfaces. Upstream and third-party components remain source-cited, user-obtained, or omitted according to their terms.
