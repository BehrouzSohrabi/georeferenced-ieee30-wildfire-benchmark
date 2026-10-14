import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.case_diff import compare_case_tables  # noqa: E402


def _bus(bus_id, pd=0.0):
    return [bus_id, 1, pd] + [0.0] * 10


def _gen(bus, pg=0.0, marker=0.0):
    return [bus, pg, 0.0, 100.0, -100.0, 1.0, 100.0, 1.0, 100.0, 0.0, marker] + [0.0] * 10


def _branch(from_bus, to_bus, rate_a=100.0, marker=0.0):
    return [from_bus, to_bus, 0.0, 0.0, 0.0, rate_a, 0.0, 0.0, 0.0, 0.0, 1.0, -360.0, 360.0 + marker]


def _gencost(*coefficients):
    return [2, 0.0, 0.0, len(coefficients), *coefficients]


class CaseDiffTests(unittest.TestCase):
    def test_reports_parameter_change_by_stable_bus_key(self):
        study = {"baseMVA": 100.0, "bus": [[3, 1, 3.0]], "gen": [], "branch": [], "gencost": []}
        reference = {"baseMVA": 100.0, "bus": [[3, 1, 2.4]], "gen": [], "branch": [], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["difference_count"], 1)
        self.assertEqual(report["differences"][0], {"table": "bus", "key": [3], "column_index": 2, "study": 3.0, "reference": 2.4})

    def test_reports_branch_change_by_directed_endpoint_key(self):
        study = {"baseMVA": 100.0, "bus": [], "gen": [], "branch": [[1, 2, 0, 0, 0, 20]], "gencost": []}
        reference = {"baseMVA": 100.0, "bus": [], "gen": [], "branch": [[1, 2, 0, 0, 0, 130]], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["difference_count"], 1)
        self.assertEqual(report["differences"][0], {"table": "branch", "key": [1, 2, 0], "column_index": 5, "study": 20, "reference": 130})

    def test_reports_shape_mismatches_without_truncating_rows(self):
        study = {"baseMVA": 100.0, "bus": [[1, 2]], "gen": [], "branch": [], "gencost": []}
        reference = {"baseMVA": 100.0, "bus": [[1, 2, 3]], "gen": [], "branch": [], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["shape_mismatches"], [{"table": "bus", "study_shape": [1, [2]], "reference_shape": [1, [3]]}])
        self.assertEqual(report["difference_count"], 0)

    def test_reports_duplicate_bus_keys_without_losing_duplicate_row_evidence(self):
        study = {"baseMVA": 100.0, "bus": [[1, 10], [1, 20]], "gen": [], "branch": [], "gencost": []}
        reference = {"baseMVA": 100.0, "bus": [[1, 10]], "gen": [], "branch": [], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["duplicate_keys"], [{
            "table": "bus", "key": [1],
            "study_rows": [[1, 10], [1, 20]], "reference_rows": [[1, 10]],
        }])

    def test_reports_key_set_differences_for_unmatched_bus_rows(self):
        study = {"baseMVA": 100.0, "bus": [[3, 1]], "gen": [], "branch": [], "gencost": []}
        reference = {"baseMVA": 100.0, "bus": [[2, 1]], "gen": [], "branch": [], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["key_set_differences"], [{"table": "bus", "study_only": [[3]], "reference_only": [[2]]}])

    def test_keys_generators_and_costs_by_bus_and_occurrence(self):
        study = {
            "baseMVA": 100.0, "bus": [], "gen": [[2, 10], [1, 20], [2, 30]], "branch": [],
            "gencost": [[2, 0, 0, 1, 100], [2, 0, 0, 1, 200], [2, 0, 0, 1, 300]],
        }
        reference = {
            "baseMVA": 100.0, "bus": [], "gen": [[2, 10], [1, 25], [2, 30]], "branch": [],
            "gencost": [[2, 0, 0, 1, 100], [2, 0, 0, 1, 250], [2, 0, 0, 1, 300]],
        }

        report = compare_case_tables(study, reference)

        self.assertEqual(report["differences"], [
            {"table": "gen", "key": [1, 0], "column_index": 1, "study": 20, "reference": 25},
            {"table": "gencost", "key": [1, 0], "column_index": 4, "study": 200, "reference": 250},
        ])

    def test_reports_unpaired_gencost_rows_even_when_both_cases_match(self):
        case = {"baseMVA": 100.0, "bus": [], "gen": [[1, 20]], "branch": [], "gencost": [[2, 0, 0, 1, 100], [2, 0, 0, 1, 200]]}

        report = compare_case_tables(case, case)

        self.assertEqual(report["gencost_association_mismatches"], [
            {"case": "reference", "gencost_row_count": 2, "generator_row_count": 1,
             "unpaired_gencost_rows": [{"row_index": 1, "row": [2, 0, 0, 1, 200]}]},
            {"case": "study", "gencost_row_count": 2, "generator_row_count": 1,
             "unpaired_gencost_rows": [{"row_index": 1, "row": [2, 0, 0, 1, 200]}]},
        ])

    def test_reports_gencost_association_and_key_set_mismatch(self):
        study = {"baseMVA": 100.0, "bus": [], "gen": [[2, 10], [1, 20]], "branch": [], "gencost": [[2, 0, 0, 1, 100]]}
        reference = {"baseMVA": 100.0, "bus": [], "gen": [[2, 10], [1, 20]], "branch": [], "gencost": [[2, 0, 0, 1, 100], [2, 0, 0, 1, 200]]}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["shape_mismatches"], [{"table": "gencost", "study_shape": [1, [5]], "reference_shape": [2, [5, 5]]}])
        self.assertEqual(report["key_set_differences"], [{"table": "gencost", "study_only": [], "reference_only": [[1, 0]]}])

    def test_reports_zero_length_and_ragged_rows_as_schema_validation_errors(self):
        study = {
            "baseMVA": 100.0, "bus": [[], _bus(2)[:-1]], "gen": [[1] * 20], "branch": [[1, 2]],
            "gencost": [[], [2, 0.0, 0.0, 3, 1.0, 2.0]],
        }
        reference = {"baseMVA": 100.0, "bus": [], "gen": [], "branch": [], "gencost": []}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["schema_validation_errors"], [
            {"case": "study", "table": "bus", "row_index": 0, "expected_width": 13, "actual_width": 0},
            {"case": "study", "table": "bus", "row_index": 1, "expected_width": 13, "actual_width": 12},
            {"case": "study", "table": "gen", "row_index": 0, "expected_width": 21, "actual_width": 20},
            {"case": "study", "table": "branch", "row_index": 0, "expected_width": 13, "actual_width": 2},
            {"case": "study", "table": "gencost", "row_index": 0, "expected_width": "4 + NCOST", "actual_width": 0},
            {"case": "study", "table": "gencost", "row_index": 1, "expected_width": 7, "actual_width": 6},
        ])

    def test_validates_expected_matpower_widths_even_when_cases_are_equal(self):
        case = {"baseMVA": 100.0, "bus": [[1] * 12], "gen": [[1] * 20], "branch": [[1] * 12], "gencost": [[2, 0.0, 0.0, 2, 1.0]]}

        report = compare_case_tables(case, case)

        self.assertEqual(report["shape_mismatches"], [])
        self.assertEqual(report["schema_validation_errors"], [
            {"case": "reference", "table": "bus", "row_index": 0, "expected_width": 13, "actual_width": 12},
            {"case": "reference", "table": "gen", "row_index": 0, "expected_width": 21, "actual_width": 20},
            {"case": "reference", "table": "branch", "row_index": 0, "expected_width": 13, "actual_width": 12},
            {"case": "reference", "table": "gencost", "row_index": 0, "expected_width": 6, "actual_width": 5},
            {"case": "study", "table": "bus", "row_index": 0, "expected_width": 13, "actual_width": 12},
            {"case": "study", "table": "gen", "row_index": 0, "expected_width": 21, "actual_width": 20},
            {"case": "study", "table": "branch", "row_index": 0, "expected_width": 13, "actual_width": 12},
            {"case": "study", "table": "gencost", "row_index": 0, "expected_width": 6, "actual_width": 5},
        ])

    def test_preserves_unpaired_gencost_row_contents(self):
        case = {"baseMVA": 100.0, "bus": [], "gen": [_gen(1)], "branch": [], "gencost": [_gencost(100), _gencost(200, 3)]}

        report = compare_case_tables(case, case)

        self.assertEqual(report["gencost_association_mismatches"], [
            {"case": "reference", "gencost_row_count": 2, "generator_row_count": 1,
             "unpaired_gencost_rows": [{"row_index": 1, "row": _gencost(200, 3)}]},
            {"case": "study", "gencost_row_count": 2, "generator_row_count": 1,
             "unpaired_gencost_rows": [{"row_index": 1, "row": _gencost(200, 3)}]},
        ])

    def test_generator_and_parallel_branch_comparison_is_order_independent(self):
        study = {"baseMVA": 100.0, "bus": [], "gen": [_gen(1, 10, 2), _gen(1, 20, 1)],
                 "branch": [_branch(1, 2, 90, 2), _branch(1, 2, 100, 1)], "gencost": [_gencost(10), _gencost(20)]}
        reference = {"baseMVA": 100.0, "bus": [], "gen": [_gen(1, 20, 1), _gen(1, 10, 2)],
                     "branch": [_branch(1, 2, 100, 1), _branch(1, 2, 90, 2)], "gencost": [_gencost(20), _gencost(10)]}

        report = compare_case_tables(study, reference)

        self.assertEqual(report["difference_count"], 0)
        self.assertEqual(report["key_set_differences"], [])


if __name__ == "__main__":
    unittest.main()
