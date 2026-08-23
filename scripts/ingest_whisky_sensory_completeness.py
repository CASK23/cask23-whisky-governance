#!/usr/bin/env python3
"""Project Zero sensory completeness manifest ingestion scaffold.

Purpose:
- Accept the forthcoming Lovable 262-BeverageId diagnostic manifest.
- Validate identity uniqueness and classification vocabulary.
- Preserve raw source data unchanged.
- Produce a deterministic research queue for Project Zero sensory enrichment.

Governance:
- BeverageId is the only expression identity key.
- No fuzzy/name-similarity joins.
- No flavour inference from icon taxonomy.
- Data chooses the icon; the icon never generates the data.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_RECORDS = 262
ALLOWED_STATES = {
    "RENDERED",
    "AVAILABLE_NOT_RENDERED",
    "ABSENT",
    "WITHHELD_CONFLICT",
}

AUDIT_FIELDS = {
    "descriptors",
    "tastingNote",
    "flavourProfile",
    "maturation",
    "technical",
    "distilleryCountry",
    "region",
    "style",
    "age",
    "abv",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def extract_records(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for key in ("records", "beverages", "items", "manifest"):
            value = payload.get(key)
            if isinstance(value, list):
                return value
    fail("Unable to locate sensory completeness record array")


def validate_record(record: dict[str, Any], index: int) -> None:
    beverage_id = record.get("beverageId") or record.get("beverage_id")
    if not isinstance(beverage_id, str) or not beverage_id.strip():
        fail(f"Record {index}: missing beverageId")

    completeness = record.get("completeness") or record.get("fields")
    if completeness is None:
        return
    if not isinstance(completeness, dict):
        fail(f"Record {index}: completeness/fields must be an object")

    for field_name, state in completeness.items():
        if field_name not in AUDIT_FIELDS:
            continue
        if isinstance(state, dict):
            state = state.get("state")
        if state is not None and state not in ALLOWED_STATES:
            fail(f"Record {index}: invalid state {state!r} for {field_name}")


def build_research_queue(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    queue: list[dict[str, Any]] = []
    for record in records:
        completeness = record.get("completeness") or record.get("fields") or {}
        missing: list[str] = []
        for field_name in ("descriptors", "tastingNote", "flavourProfile"):
            state = completeness.get(field_name)
            if isinstance(state, dict):
                state = state.get("state")
            if state in {"ABSENT", "WITHHELD_CONFLICT"}:
                missing.append(field_name)
        if missing:
            queue.append(
                {
                    "beverageId": record.get("beverageId") or record.get("beverage_id"),
                    "stagingId": record.get("stagingId"),
                    "systemSlug": record.get("systemSlug"),
                    "displayName": record.get("displayName"),
                    "researchRequiredFor": missing,
                    "governanceState": "UNVERIFIED_RESEARCH_QUEUE",
                }
            )
    return queue


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Raw Lovable sensory completeness JSON")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("sensory"),
        help="Destination directory for preserved manifest and deterministic research queue",
    )
    args = parser.parse_args()

    payload = load_json(args.input)
    records = extract_records(payload)

    if len(records) != EXPECTED_RECORDS:
        fail(f"Expected {EXPECTED_RECORDS} records, found {len(records)}")

    seen: set[str] = set()
    for index, record in enumerate(records, start=1):
        if not isinstance(record, dict):
            fail(f"Record {index}: expected object")
        validate_record(record, index)
        beverage_id = record.get("beverageId") or record.get("beverage_id")
        if beverage_id in seen:
            fail(f"Duplicate beverageId: {beverage_id}")
        seen.add(beverage_id)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = args.output_dir / "lovable-262-sensory-completeness.raw.json"
    with raw_path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    queue = build_research_queue(records)
    queue_path = args.output_dir / "PROJECT_ZERO_SENSORY_RESEARCH_QUEUE.json"
    queue_payload = {
        "project": "PROJECT_ZERO_SENSORY_RESEARCH_QUEUE",
        "status": "UNVERIFIED_RESEARCH_QUEUE",
        "sourceRecordCount": len(records),
        "identityKey": "beverageId",
        "governanceRule": "Data chooses the icon; the icon never generates the data.",
        "researchHierarchy": [
            "PRODUCER_OFFICIAL",
            "IMPORTER_OR_DISTRIBUTOR_OFFICIAL",
            "ESTABLISHED_INDUSTRY_SPECIALIST",
            "ABSENCE",
        ],
        "records": queue,
    }
    with queue_path.open("w", encoding="utf-8") as handle:
        json.dump(queue_payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(
        json.dumps(
            {
                "validatedRecords": len(records),
                "uniqueBeverageIds": len(seen),
                "researchQueueRecords": len(queue),
                "rawManifest": str(raw_path),
                "researchQueue": str(queue_path),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
