# Independent review — electrical-case comparator

**Review date:** 2026-10-11  
**Scope:** `src/case_diff.py` and `tests/test_case_diff.py`  
**Reviewer role:** independent read-only audit

## Verdict

**Resolved on 2026-10-11.** The original review correctly blocked release use. New regression tests first demonstrated the reported failures; the corrective implementation now passes the full suite. A provenance-bearing artifact generator remains a separate pipeline deliverable, but the in-memory comparator no longer suppresses the reviewed malformed/ambiguous-input evidence.

## Required corrections

1. Preserve full row evidence for duplicate `BUS_I` rows; a duplicate marker alone must not hide differing values.
2. Replace key-column `IndexError` behavior for empty/ragged rows with structured validation findings.
3. Validate canonical MATPOWER table widths: bus 13, generator 21, and branch 13; validate gencost row structure from its declared model/`NCOST`.
4. Preserve values of unpaired excess gencost rows, rather than reporting only row counts.
5. Make generator and parallel-branch comparison independent of source row ordering, or report/enforce an explicit canonical ordering rule.
6. Build the provenance-bearing JSON/Markdown/CSV artifact path after the comparator passes the above data-integrity checks.

## Verified positive baseline

For the preserved IGREFire case compared with bundled PYPOWER `case30`, the current valid-input result contains exactly two differences:

- Bus 3 `Pd`: 3.0 MW versus 2.4 MW.
- Branch 1→2 `RATE_A`: 20 MVA versus 130 MVA.

The review did not approve treating this valid-case result as sufficient coverage. A corrective TDD work package is active.
