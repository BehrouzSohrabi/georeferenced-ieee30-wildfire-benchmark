# Scientific Data and DOI-repository requirements

**Status:** official-source refresh complete  
**Access date:** 2026-10-11  
**Primary venue:** *Scientific Data* (Data Descriptor)

## Official sources

- [Scientific Data submission guidelines](https://www.nature.com/sdata/publish/submission-guidelines)
- [Scientific Data data policies](https://www.nature.com/sdata/policies/data-policies)
- [Scientific Data repository guidance](https://www.nature.com/sdata/policies/repositories)

## Verified requirements applied to this release

1. Use the Data Descriptor structure: Abstract; Background & Summary; Methods; Data Records; Technical Validation; Data Availability; Code Availability; and the required author, funding, and competing-interest declarations. Usage Notes are optional.
2. Deposit primary data in a preservation repository with a stable persistent identifier (normally a DOI), direct HTTPS download, and public access. Data must be anonymously downloadable for review and public by the later review/publication stages.
3. Data Records must enumerate files, formats, fields, directories, metadata, and formal citations for external inputs.
4. Technical Validation must document coordinate/CRS QA, topology and identifier checks, schema validation, provenance/completeness checks, and reproducibility tests.
5. Code Availability is required. The deposited code statement must name the version/release and disclose any restrictions.
6. Non-sensitive deposited data normally require CC0, CC BY, or an equivalent open license. Upstream restrictions are not overridden by repository or journal policy.
7. Repository data—not supplementary files—should carry substantive datasets. Supplementary text/figures/small tables are one PDF limited to 10 MB; exceptionally large datasets over 1 TB have special routing.

## Release consequence for the benchmark

The DOI archive will be a clean-room package containing only project-authored or independently cleared materials: the georeferenced spatial layer, schema/data dictionary, provenance and rights manifests, checksums, validation code, reproducible build instructions, and approved examples. It will not contain FARSITE, copied IEEE case files, or another restricted upstream payload.

Each optional fuel/weather component must name exact source version, retrieval date/query, checksum, transformation, attribution, terms URL, and inclusion status. If an input cannot be openly redistributed, the release provides a precise acquisition pointer and regeneration interface rather than the payload.

## Practical release checklist

Before Zenodo deposit, independently verify that every distributed file has a rights status, license, source/version, checksum, and data-dictionary entry; the archive downloads anonymously; hashes match; the build works from a clean environment; and restricted material is absent from code examples, tests, archives, and generated outputs.
