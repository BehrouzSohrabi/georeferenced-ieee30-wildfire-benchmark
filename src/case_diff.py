"""Deterministic, evidence-preserving comparison for MATPOWER-style case tables."""
from __future__ import annotations

from collections import defaultdict
from collections.abc import Sequence
from typing import Any

_TABLE_ORDER = {"baseMVA": 0, "bus": 1, "gen": 2, "branch": 3, "gencost": 4}
_EXPECTED_WIDTH = {"bus": 13, "gen": 21, "branch": 13}


def compare_case_tables(study: dict, reference: dict) -> dict:
    """Compare two MATPOWER cases without hiding malformed or ambiguous input."""
    differences: list[dict[str, Any]] = []
    shape_mismatches: list[dict[str, Any]] = []
    schema_errors: list[dict[str, Any]] = []
    key_set_differences: list[dict[str, Any]] = []
    duplicate_keys: list[dict[str, Any]] = []

    for case_name, case in (("study", study), ("reference", reference)):
        schema_errors.extend(_validate_schema(case_name, case))

    if study["baseMVA"] != reference["baseMVA"]:
        differences.append(_difference("baseMVA", (), None, study["baseMVA"], reference["baseMVA"]))

    study_gen, study_gen_index = _key_rows(study["gen"], "gen")
    reference_gen, reference_gen_index = _key_rows(reference["gen"], "gen")
    table_keyed = {
        "bus": (_key_rows(study["bus"], "bus")[0], _key_rows(reference["bus"], "bus")[0]),
        "gen": (study_gen, reference_gen),
        "branch": (_key_rows(study["branch"], "branch")[0], _key_rows(reference["branch"], "branch")[0]),
    }

    for table, (study_rows, reference_rows) in table_keyed.items():
        _record_shape_mismatch(table, study[table], reference[table], shape_mismatches)
        if table == "bus":
            duplicate_keys.extend(_duplicate_bus_evidence(study["bus"], reference["bus"]))
        _record_key_set_difference(table, study_rows, reference_rows, key_set_differences)
        _compare_keyed_rows(table, study_rows, reference_rows, differences)

    study_gencost, study_unpaired = _gencost_by_generator_key(study["gencost"], study_gen_index)
    reference_gencost, reference_unpaired = _gencost_by_generator_key(reference["gencost"], reference_gen_index)
    _record_shape_mismatch("gencost", study["gencost"], reference["gencost"], shape_mismatches)
    _record_key_set_difference("gencost", study_gencost, reference_gencost, key_set_differences)
    _compare_keyed_rows("gencost", study_gencost, reference_gencost, differences)

    gencost_association_mismatches = []
    for case_name, case, unpaired in (("study", study, study_unpaired), ("reference", reference, reference_unpaired)):
        if len(case["gencost"]) != len(case["gen"]):
            gencost_association_mismatches.append({
                "case": case_name,
                "gencost_row_count": len(case["gencost"]),
                "generator_row_count": len(case["gen"]),
                "unpaired_gencost_rows": unpaired,
            })

    differences.sort(key=_difference_sort_key)
    shape_mismatches.sort(key=lambda item: _TABLE_ORDER[item["table"]])
    key_set_differences.sort(key=lambda item: _TABLE_ORDER[item["table"]])
    duplicate_keys.sort(key=lambda item: tuple(item["key"]))
    schema_errors.sort(key=lambda item: ({"reference": 0, "study": 1}[item["case"]], _TABLE_ORDER[item["table"]], item["row_index"]))
    gencost_association_mismatches.sort(key=lambda item: item["case"])
    return {
        "difference_count": len(differences), "differences": differences,
        "shape_mismatches": shape_mismatches, "schema_validation_errors": schema_errors,
        "key_set_differences": key_set_differences, "duplicate_keys": duplicate_keys,
        "gencost_association_mismatches": gencost_association_mismatches,
    }


def _validate_schema(case_name: str, case: dict) -> list[dict[str, Any]]:
    errors = []
    for table, expected_width in _EXPECTED_WIDTH.items():
        for row_index, row in enumerate(case[table]):
            if len(row) != expected_width:
                errors.append(_schema_error(case_name, table, row_index, expected_width, len(row)))
    for row_index, row in enumerate(case["gencost"]):
        expected = _gencost_expected_width(row)
        if expected is None or len(row) != expected:
            errors.append(_schema_error(case_name, "gencost", row_index, "4 + NCOST" if expected is None else expected, len(row)))
    return errors


def _schema_error(case: str, table: str, row_index: int, expected_width: Any, actual_width: int) -> dict[str, Any]:
    return {"case": case, "table": table, "row_index": row_index, "expected_width": expected_width, "actual_width": actual_width}


def _gencost_expected_width(row: Sequence[Any]) -> int | None:
    if len(row) < 4 or not isinstance(row[3], (int, float)) or int(row[3]) != row[3] or row[3] < 0:
        return None
    ncost, model = int(row[3]), row[0]
    return 4 + (2 * ncost if model == 1 else ncost)


def _key_rows(rows: Sequence[Sequence[Any]], table: str) -> tuple[dict[tuple[Any, ...], Sequence[Any]], dict[int, tuple[Any, ...]]]:
    """Create order-independent keys by canonically sorting valid row contents."""
    key_columns = {"bus": 1, "gen": 1, "branch": 2}[table]
    valid = [(index, row) for index, row in enumerate(rows) if len(row) >= key_columns]
    if table == "bus":
        grouped: dict[Any, list[tuple[int, Sequence[Any]]]] = defaultdict(list)
        for index, row in valid:
            grouped[row[0]].append((index, row))
        keyed, index_keys = {}, {}
        for bus, entries in grouped.items():
            if len(entries) == 1:
                index, row = entries[0]
                keyed[(bus,)] = row
                index_keys[index] = (bus,)
        return keyed, index_keys

    grouped = defaultdict(list)
    for index, row in valid:
        base = (row[0],) if table == "gen" else (row[0], row[1])
        grouped[base].append((index, row))
    keyed, index_keys = {}, {}
    for base, entries in grouped.items():
        for occurrence, (index, row) in enumerate(sorted(entries, key=lambda pair: (tuple(pair[1]), pair[0]))):
            key = (*base, occurrence)
            keyed[key] = row
            index_keys[index] = key
    return keyed, index_keys


def _duplicate_bus_evidence(study_rows: Sequence[Sequence[Any]], reference_rows: Sequence[Sequence[Any]]) -> list[dict[str, Any]]:
    def groups(rows):
        result = defaultdict(list)
        for row in rows:
            if row:
                result[row[0]].append(list(row))
        return result
    study_groups, reference_groups = groups(study_rows), groups(reference_rows)
    duplicate_ids = sorted(key for key in study_groups.keys() | reference_groups.keys() if len(study_groups[key]) > 1 or len(reference_groups[key]) > 1)
    return [{"table": "bus", "key": [key], "study_rows": study_groups[key], "reference_rows": reference_groups[key]} for key in duplicate_ids]


def _gencost_by_generator_key(rows: Sequence[Sequence[Any]], generator_index_keys: dict[int, tuple[Any, ...]]) -> tuple[dict[tuple[Any, ...], Sequence[Any]], list[dict[str, Any]]]:
    keyed, unpaired = {}, []
    for index, row in enumerate(rows):
        key = generator_index_keys.get(index)
        if key is None:
            unpaired.append({"row_index": index, "row": list(row)})
        else:
            keyed[key] = row
    return keyed, unpaired


def _record_shape_mismatch(table, study_rows, reference_rows, output):
    study_shape, reference_shape = _table_shape(study_rows), _table_shape(reference_rows)
    if study_shape != reference_shape:
        output.append({"table": table, "study_shape": study_shape, "reference_shape": reference_shape})


def _table_shape(rows):
    return [len(rows), [len(row) for row in rows]]


def _record_key_set_difference(table, study_rows, reference_rows, output):
    study_only, reference_only = sorted(study_rows.keys() - reference_rows.keys()), sorted(reference_rows.keys() - study_rows.keys())
    if study_only or reference_only:
        output.append({"table": table, "study_only": [list(key) for key in study_only], "reference_only": [list(key) for key in reference_only]})


def _compare_keyed_rows(table, study_rows, reference_rows, differences):
    for key in sorted(study_rows.keys() & reference_rows.keys()):
        for column_index, (study_value, reference_value) in enumerate(zip(study_rows[key], reference_rows[key])):
            if study_value != reference_value:
                differences.append(_difference(table, key, column_index, study_value, reference_value))


def _difference(table, key, column_index, study, reference):
    return {"table": table, "key": list(key), "column_index": column_index, "study": study, "reference": reference}


def _difference_sort_key(item):
    return (_TABLE_ORDER[item["table"]], tuple(item["key"]), -1 if item["column_index"] is None else item["column_index"])
