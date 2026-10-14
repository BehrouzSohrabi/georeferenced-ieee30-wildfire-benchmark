## Outcome
I screened **five peer-reviewed data-description venues** against a reproducible, georeferenced wildfire–power-grid benchmark, using current official publisher/journal guidance where accessible (checked October 2026). **Scientific Data** is the clearest overall fit; **ESSD** is a strong Earth-system-focused option if the wildfire/geospatial data and validation are central.

### Conservative ranking

| Rank | Venue | Fit for wildfire–grid benchmark | Bottom line |
|---:|---|---|---|
| 1 | **Scientific Data** | Excellent; cross-disciplinary dataset descriptors and explicit validation/code sections | Best primary target. |
| 2 | **Earth System Science Data (ESSD)** | Excellent for georeferenced wildfire/Earth-system data; grid layer must be framed as part of an Earth-system-relevant data product | Strong if the manuscript can meet its unusually demanding uncertainty/validation expectations. |
| 3 | **Geoscience Data Journal** | Good for wildfire/geospatial datasets; power-grid component is plausible but not expressly confirmed | Worth a pre-submission scope check before investing heavily. |
| 4 | **Data in Brief** | Broad, practical fallback for a citable data release | Suitable, but less benchmark-/reproducibility-specific and less technically demanding. |
| 5 | **GigaScience (Data Note)** | Formal data-note model and strong repository linkage, but scope fit is uncertain for a non-life-science wildfire–grid product | Do not prioritize without editorial confirmation of scope. |

---

## Verified venue guidance

### 1. Scientific Data — **recommended**
- **Scope fit:** Peer-reviewed, open-access journal for descriptions of datasets across sciences and data-oriented social sciences. Its primary **Data Descriptor** format is designed for repository-hosted datasets and supports interdisciplinary environmental/infrastructure benchmarks.
- **Article type:** **Data Descriptor**.
- **Repository / DOI expectations:** Data must be available to editors/referees at submission and publicly shared at final publication. By the second review round, data must be public in a formal repository meeting journal policy. External datasets, including the focal dataset, must be formally cited.
- **Code / reproducibility:** A mandatory **“Code Availability”** subsection must say whether/how custom code can be accessed and explain restrictions. Repository deposition is strongly encouraged over supplementary files.
- **Technical validation:** Mandatory **“Technical Validation”** section describing experiments, analyses, or checks supporting dataset technical quality, with figures/tables where needed. This is ideal for spatial alignment checks, event matching, topology/asset QA, coverage analyses, splits, leakage controls, and benchmark baselines.
- **Licensing / open data:** Its policy identifies open-download repositories and open licenses such as **CC BY / CC0 or equivalent** as the standard route for unrestricted data. Controlled access is only applicable where justified (e.g., sensitive data).
- **Official URLs:**
  - Submission guide: https://www.nature.com/sdata/submission-guidelines
  - Data policy: https://www.nature.com/sdata/policies/data-policies
  - Referee/descriptor criteria: https://www.nature.com/sdata/policies/for-referees

### 2. Earth System Science Data (ESSD) — **recommended if Earth-system framing is primary**
- **Scope fit:** International interdisciplinary journal publishing original datasets that advance reuse of high-quality data beneficial to Earth-system sciences. Wildfire, land surface, meteorology, smoke, hazard, and georeferenced exposure/infrastructure layers can fit; the manuscript should make the Earth-system data contribution—not only grid application—the center of gravity.
- **Article type:** **Data description paper**.
- **Repository / DOI expectations:** At submission, data need either a functional DOI or a repository review link; data citation and direct manuscript links are mandatory. At publication, all data must have a functional DOI and citation. Repositories must provide long-term access.
- **Code / reproducibility:** The journal explicitly treats model code and related research objects as part of the reproducibility network and asks authors to consider depositing software/model code in reliable DOI-issuing repositories. It is prudent to archive the benchmark-generation pipeline, spatial joins, schemas, environment lockfile, and evaluation scripts alongside the dataset.
- **Technical validation:** Especially demanding. Data-description papers must address both internal variability and deviation from truth, include validation against independent data where possible, and explain uncertainty/evaluation. Reviewers are instructed to assess the dataset itself, not just the manuscript.
- **Licensing / open data:** Data should be under a non-restrictive license such as **CC0 or CC BY**; must not impose coercive use conditions. Accessibility should have minimal barriers to reuse.
- **Official URLs:**
  - Manuscript types: https://www.earth-system-science-data.net/about/manuscript_types.html
  - Data policy: https://www.earth-system-science-data.net/policies/data_policy.html
  - Review criteria: https://www.earth-system-science-data.net/peer_review/review_criteria.html
  - Repository criteria: https://www.earth-system-science-data.net/policies/repository_criteria.html

### 3. Geoscience Data Journal — **credible alternative**
- **Scope fit:** Covers Earth-system datasets across meteorology, oceanography, atmospheric/ocean chemistry, cryosphere, biosphere, land-surface science, and geology. Wildfire/geospatial layers are clearly adjacent; the power-grid component should be presented as an interoperable exposure/impact layer supporting geoscience reuse.
- **Article type:** **Data Paper**.
- **Repository / DOI expectations:** The required Data Accessibility Statement must include a persistent identifier—e.g., dataset DOI or repository accession number—and relevant data citations. Its repository guidance expects DOI assignment and preservation appropriate to the dataset’s scientific value.
- **Code / reproducibility:** Data accessibility is explicit. I did **not** verify an equally explicit, journal-specific mandatory code-availability section from accessible official guidance; archive code/workflows with the data and document it in the accessibility statement/manuscript.
- **Technical validation:** Data papers are expected to describe dataset creation, quality, and reuse, but I did not verify a prescribed dedicated “Technical Validation” heading comparable to Scientific Data’s. Include a rigorous validation section regardless.
- **Licensing / open data:** The journal is open access; however, I could not verify a dataset-specific mandatory license formulation from the accessible official author guidance. Use a permissive repository license (preferably CC BY 4.0 or CC0 where feasible) and confirm during submission.
- **Official URLs:**
  - Author guidelines: https://rmets.onlinelibrary.wiley.com/hub/journal/20496060/about/author-guidelines
  - Repository guidance: https://rmets.onlinelibrary.wiley.com/hub/journal/20496060/guidelines-for-repositories
  - Scope summary: https://www.rmets.org/geoscience-data-journal

### 4. Data in Brief — **broad fallback**
- **Scope fit:** Multidisciplinary venue specifically for describing and sharing data from any field that may be useful to another researcher. Appropriate for a citable benchmark release, though less purpose-built for extensive benchmark methodology than Scientific Data/ESSD.
- **Article type:** **Data Article**.
- **Repository / DOI expectations:** All described data must be publicly available—via the article, a public repository, or Mendeley Data. The official guide says Mendeley Data provides a final dataset DOI when formally published, linked to the article.
- **Code / reproducibility:** The guide emphasizes enough methods detail to understand creation of the data and how derived data/statistics were generated. I did not find an explicit journal-level code-release mandate in the verified guide; deposit benchmark construction/evaluation code independently and cite it.
- **Technical validation:** Data Articles are reviewed for **clarity and completeness**, and data are assessed on utility/reuse rather than research significance. The guide does not specify a standalone mandatory validation section; include validation/QA explicitly for credibility.
- **Licensing / open data:** Public availability is mandatory in the guide. I did not verify a fixed dataset-license requirement in the current official guide; select and state an open repository license, ideally CC BY 4.0/CC0 when source-data rights permit.
- **Official URLs:**
  - Official journal: https://www.sciencedirect.com/journal/data-in-brief
  - Official Data in Brief author quick guide (June 2024): https://researcheracademy.elsevier.com/uploads/2024-07/Quick_guide_Data_in_brief.pdf
  - Current author template: https://researcheracademy.elsevier.com/uploads/2024-07/data-in-brief-article-template.docx

### 5. GigaScience — **only with scope confirmation**
- **Scope fit:** Its **Data Note** highlights exceptional datasets with detailed production, validation, and reuse documentation, and can link all data through GigaDB. However, GigaScience’s traditional emphasis is life/biomedical and large-scale biological data; a wildfire–power-grid benchmark is not an obvious scope match.
- **Article type:** **Data Note**.
- **Repository / DOI expectations:** Official author guidance requires datasets, materials, and methods supporting results to be deposited in publicly accessible repositories, including GigaDB. The Data Note page says all data can be linked to the article through GigaDB.
- **Code / reproducibility:** The journal’s guidance requires supporting materials and methods to be publicly accessible; a reproducible workflow/code release is therefore strongly aligned. I could not independently confirm a current, Data-Note-specific mandatory code-statement wording because Oxford Academic’s pages were Cloudflare-blocked during verification.
- **Technical validation:** The official Data Note description explicitly calls for detailed methodology for data production, **validation**, and potential reuse.
- **Licensing / open data:** GigaScience is open access and GigaDB is positioned as an open data repository, but I could not verify the exact current dataset-license requirement from the live repository guidance during this check. Confirm current GigaDB terms before considering submission.
- **Official URLs:**
  - Data Note: https://academic.oup.com/gigascience/pages/data_note
  - Instructions to authors: https://academic.oup.com/gigascience/pages/instructions_to_authors
  - GigaDB submission guidance: https://gigadb.org/guide

## Evidence gaps / cautions
- **Oxford Academic (GigaScience)** and **Wiley (Geoscience Data Journal)** author-guidance pages were technically blocked to direct retrieval during this check. Their official search-indexed descriptions and URLs were verified, but exact current wording—especially code and dataset-license requirements—should be rechecked manually immediately before submission.
- **Data in Brief**: official guide clearly mandates public availability, but I did not find a fixed dataset-license or code-release mandate. Treat explicit code archival and a permissive data license as best practice, not verified journal requirements.
- **Geoscience Data Journal**: repository PID expectations are explicit, but a dedicated technical-validation section and code requirement were not verified.
- **Scope is the principal risk** for GigaScience; it ranks last despite a strong Data Note model.
- For all venues, separately confirm that third-party wildfire, meteorological, and grid-asset inputs can legally be redistributed under the selected benchmark license.

## Files
- No local files were created or modified.