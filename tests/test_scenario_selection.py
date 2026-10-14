import csv
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.scenario_selection import (  # noqa: E402
    REQUIRED_WEATHER_IDS,
    ScenarioSelectionError,
    select_validation_scenarios,
    write_selection_csv,
)


class ScenarioSelectionTests(unittest.TestCase):
    def _write_manifest(self, directory: Path, lines=("line_01", "line_02")) -> Path:
        path = directory / "scenario-manifest.csv"
        rows = []
        for line_id in lines:
            for weather_id in REQUIRED_WEATHER_IDS:
                # Two candidates per stratum ensure ranks and score tie-breaks are observable.
                rows.append({"scenario_id": f"{line_id}_{weather_id}_b", "line_id": line_id, "weather_id": weather_id})
                rows.append({"scenario_id": f"{line_id}_{weather_id}_a", "line_id": line_id, "weather_id": weather_id})
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["scenario_id", "line_id", "weather_id"])
            writer.writeheader()
            writer.writerows(reversed(rows))
        return path

    def test_selects_five_weather_strata_per_line_and_one_lowest_omitted_candidate(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = self._write_manifest(Path(temporary))
            expected_manifest_sha256 = hashlib.sha256(manifest.read_bytes()).hexdigest()
            result = select_validation_scenarios(manifest)

        selected = [row for row in result.rows if row["selected"] == "true"]
        self.assertEqual(result.manifest_sha256, expected_manifest_sha256)
        self.assertEqual(len(selected), 11)
        self.assertEqual(sum(row["selection_reason"] == "lowest-score sixth-condition selection" for row in selected), 1)
        for line_id in ("line_01", "line_02"):
            line_selected = [row for row in selected if row["line_id"] == line_id]
            self.assertIn(len(line_selected), (5, 6))
            self.assertEqual(len({row["weather_id"] for row in line_selected}), len(line_selected))

        selected_by_stratum = {(row["line_id"], row["weather_id"]): row for row in selected}
        for line_id in ("line_01", "line_02"):
            for weather_id in REQUIRED_WEATHER_IDS:
                candidates = [
                    row for row in result.rows
                    if row["line_id"] == line_id and row["weather_id"] == weather_id
                ]
                self.assertEqual(min(candidates, key=lambda row: row["score"])["rank"], "1")
                if (line_id, weather_id) in selected_by_stratum:
                    self.assertEqual(selected_by_stratum[(line_id, weather_id)]["rank"], "1")

    def test_41_line_population_selects_exactly_206_scenarios(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = self._write_manifest(
                Path(temporary),
                lines=tuple(f"line_{number:02d}" for number in range(1, 42)),
            )
            result = select_validation_scenarios(manifest, expected_line_count=41)

        selected = [row for row in result.rows if row["selected"] == "true"]
        self.assertEqual(len(selected), 206)
        weather_counts = {weather: sum(row["weather_id"] == weather for row in selected) for weather in REQUIRED_WEATHER_IDS}
        self.assertLessEqual(max(weather_counts.values()) - min(weather_counts.values()), 1)

    def test_is_reproducible_for_differently_ordered_input_rows_and_writes_auditable_csv(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = self._write_manifest(directory)
            first = select_validation_scenarios(manifest)
            output = directory / "selection.csv"
            write_selection_csv(first, output)
            second = select_validation_scenarios(manifest)
            with output.open(newline="", encoding="utf-8") as handle:
                rows = list(csv.DictReader(handle))

        self.assertEqual(first.rows, second.rows)
        self.assertEqual(rows, first.rows)
        self.assertEqual(
            list(rows[0]),
            ["scenario_id", "line_id", "weather_id", "manifest_sha256", "score", "rank", "eligibility", "selected", "selection_reason", "replacement_reason"],
        )
        self.assertTrue(all(row["manifest_sha256"] == first.manifest_sha256 for row in rows))
        self.assertTrue(all(row["eligibility"] in {"eligible", "not-selected: non-minimum score"} for row in rows))

    def test_rejects_missing_required_weather_stratum_with_clear_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            manifest = self._write_manifest(Path(temporary), lines=("line_01",))
            content = manifest.read_text(encoding="utf-8")
            manifest.write_text("\n".join(line for line in content.splitlines() if "Wind-W" not in line) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(ScenarioSelectionError, "line_01.*Wind-W"):
                select_validation_scenarios(manifest)

    def test_rejects_duplicate_scenario_ids_and_unknown_weather_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = directory / "scenario-manifest.csv"
            manifest.write_text(
                "scenario_id,line_id,weather_id\n"
                "scen_001,line_01,Fall\n"
                "scen_001,line_01,Monsoon\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ScenarioSelectionError, "duplicate scenario_id.*scen_001"):
                select_validation_scenarios(manifest)

            manifest.write_text(
                "scenario_id,line_id,weather_id\nscen_001,line_01,Monsoon\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ScenarioSelectionError, "unsupported weather_id.*Monsoon"):
                select_validation_scenarios(manifest)


if __name__ == "__main__":
    unittest.main()
