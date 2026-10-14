"""Deterministic, stdlib-only selection of the minimum 206-scenario rerun sample.

The input manifest is treated as frozen bytes: its SHA-256 is included in every
candidate score so a selection cannot be silently reused for a changed manifest.
"""
from __future__ import annotations

import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

REQUIRED_COLUMNS = ("scenario_id", "line_id", "weather_id")
REQUIRED_WEATHER_IDS = ("Fall", "Summer", "Wind-N", "Wind-E", "Wind-S", "Wind-W")
SCORE_PREFIX = "IGREFire-rerun-v1"
OUTPUT_COLUMNS = (
    "scenario_id",
    "line_id",
    "weather_id",
    "manifest_sha256",
    "score",
    "rank",
    "eligibility",
    "selected",
    "selection_reason",
    "replacement_reason",
)


class ScenarioSelectionError(ValueError):
    """Raised when a frozen scenario manifest cannot support the selection."""


@dataclass(frozen=True)
class SelectionResult:
    manifest_sha256: str
    rows: list[dict[str, str]]

    @property
    def selected_count(self) -> int:
        return sum(row["selected"] == "true" for row in self.rows)


def _score(scenario_id: str, manifest_sha256: str) -> str:
    payload = f"{SCORE_PREFIX}|{scenario_id}|{manifest_sha256}".encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _read_manifest(path: Path) -> tuple[str, list[dict[str, str]]]:
    try:
        raw = path.read_bytes()
    except OSError as error:
        raise ScenarioSelectionError(f"cannot read manifest: {path}") from error
    manifest_sha256 = hashlib.sha256(raw).hexdigest()
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        raise ScenarioSelectionError("manifest must be UTF-8 encoded") from error

    reader = csv.DictReader(text.splitlines())
    missing = [column for column in REQUIRED_COLUMNS if column not in (reader.fieldnames or ())]
    if missing:
        raise ScenarioSelectionError(f"manifest missing required column(s): {', '.join(missing)}")

    records: list[dict[str, str]] = []
    seen_scenario_ids: set[str] = set()
    for row_number, row in enumerate(reader, start=2):
        record = {column: (row.get(column) or "").strip() for column in REQUIRED_COLUMNS}
        blank = [column for column, value in record.items() if not value]
        if blank:
            raise ScenarioSelectionError(f"row {row_number} has blank required field(s): {', '.join(blank)}")
        scenario_id = record["scenario_id"]
        if scenario_id in seen_scenario_ids:
            raise ScenarioSelectionError(f"duplicate scenario_id: {scenario_id}")
        seen_scenario_ids.add(scenario_id)
        if record["weather_id"] not in REQUIRED_WEATHER_IDS:
            raise ScenarioSelectionError(
                f"row {row_number} has unsupported weather_id: {record['weather_id']}"
            )
        records.append(record)
    if not records:
        raise ScenarioSelectionError("manifest contains no scenario rows")
    return manifest_sha256, records


def _validate_complete_strata(records: Iterable[dict[str, str]]) -> list[str]:
    weather_by_line: dict[str, set[str]] = {}
    for record in records:
        weather_by_line.setdefault(record["line_id"], set()).add(record["weather_id"])
    for line_id in sorted(weather_by_line):
        missing = [weather for weather in REQUIRED_WEATHER_IDS if weather not in weather_by_line[line_id]]
        if missing:
            raise ScenarioSelectionError(
                f"line_id {line_id} is missing required weather stratum(s): {', '.join(missing)}"
            )
    return sorted(weather_by_line)


def select_validation_scenarios(
    manifest_path: str | Path,
    *,
    expected_line_count: int | None = None,
) -> SelectionResult:
    """Return auditable candidate rows for the deterministic stratified selection.

    The first sorted line omits ``Fall``, the second omits ``Summer``, and so
    on cyclically. Every selected stratum uses its score-minimum candidate. One
    extra scenario is then selected from the omitted strata that belong to the
    underrepresented weather conditions: the one whose score-minimum candidate
    has the lowest score. With 41 lines this is exactly ``41 * 5 + 1 == 206``
    selections, with weather-condition counts differing by at most one.
    """
    manifest_sha256, records = _read_manifest(Path(manifest_path))
    line_ids = _validate_complete_strata(records)
    if expected_line_count is not None and len(line_ids) != expected_line_count:
        raise ScenarioSelectionError(
            f"manifest has {len(line_ids)} distinct line_id values; expected {expected_line_count}"
        )

    candidates: list[dict[str, str]] = []
    for record in records:
        candidate = dict(record)
        candidate["manifest_sha256"] = manifest_sha256
        candidate["score"] = _score(record["scenario_id"], manifest_sha256)
        candidates.append(candidate)

    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for candidate in candidates:
        grouped.setdefault((candidate["line_id"], candidate["weather_id"]), []).append(candidate)
    winners: dict[tuple[str, str], dict[str, str]] = {}
    for key, group in grouped.items():
        group.sort(key=lambda row: (row["score"], row["scenario_id"]))
        for rank, candidate in enumerate(group, start=1):
            candidate["rank"] = str(rank)
        winners[key] = group[0]

    omitted_weather_by_line = {
        line_id: REQUIRED_WEATHER_IDS[index % len(REQUIRED_WEATHER_IDS)]
        for index, line_id in enumerate(line_ids)
    }
    selected_keys = {
        (line_id, weather_id)
        for line_id in line_ids
        for weather_id in REQUIRED_WEATHER_IDS
        if weather_id != omitted_weather_by_line[line_id]
    }
    # The sixth scenario must come from an underrepresented condition.  This
    # preserves the protocol's final condition-count balance (difference <= 1)
    # while still resolving the choice by the lowest deterministic score.
    omitted_keys = [(line_id, omitted_weather_by_line[line_id]) for line_id in line_ids]
    omitted_count_by_weather = {
        weather_id: sum(key[1] == weather_id for key in omitted_keys)
        for weather_id in REQUIRED_WEATHER_IDS
    }
    maximum_omission_count = max(omitted_count_by_weather.values())
    balance_eligible_omitted_keys = [
        key for key in omitted_keys
        if omitted_count_by_weather[key[1]] == maximum_omission_count
    ]
    sixth_key = min(
        balance_eligible_omitted_keys,
        key=lambda key: (winners[key]["score"], winners[key]["scenario_id"]),
    )
    selected_keys.add(sixth_key)

    for candidate in candidates:
        key = (candidate["line_id"], candidate["weather_id"])
        is_winner = candidate["rank"] == "1"
        is_selected = is_winner and key in selected_keys
        candidate["eligibility"] = "eligible" if is_winner else "not-selected: non-minimum score"
        candidate["selected"] = "true" if is_selected else "false"
        if is_selected and key == sixth_key:
            candidate["selection_reason"] = "lowest-score sixth-condition selection"
            candidate["replacement_reason"] = "selected from the cyclically omitted weather stratum"
        elif is_selected:
            candidate["selection_reason"] = "five-condition cyclic stratified selection"
            candidate["replacement_reason"] = "selected: minimum score in line/weather stratum"
        elif is_winner:
            candidate["selection_reason"] = "not selected"
            candidate["replacement_reason"] = (
                "cyclically omitted weather stratum; not the lowest score among balance-eligible omitted strata"
            )
        else:
            winner = winners[key]
            candidate["selection_reason"] = "not selected"
            candidate["replacement_reason"] = (
                f"replaced by {winner['scenario_id']} (rank 1 minimum score in line/weather stratum)"
            )

    ordered_rows = sorted(
        candidates,
        key=lambda row: (
            row["line_id"],
            REQUIRED_WEATHER_IDS.index(row["weather_id"]),
            int(row["rank"]),
            row["scenario_id"],
        ),
    )
    return SelectionResult(manifest_sha256=manifest_sha256, rows=[
        {column: row[column] for column in OUTPUT_COLUMNS} for row in ordered_rows
    ])


def write_selection_csv(result: SelectionResult, output_path: str | Path) -> None:
    """Write all candidates atomically enough for a normal local workflow."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(result.rows)
