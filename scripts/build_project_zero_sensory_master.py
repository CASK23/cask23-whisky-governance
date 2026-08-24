#!/usr/bin/env python3
"""Build PROJECT_ZERO_SENSORY_MASTER.json from the frozen Lovable manifest + reviewed progress ledgers.

Hard rules:
- Canonical identity comes only from the 262-item manifest (beverageId + officialName).
- No name recovery, fuzzy matching, slug matching, or cross-expression donation.
- Existing governed descriptors/tasting notes are preserved verbatim.
- Research fills missing fields only.
- A research row with a BeverageId absent from the manifest is a hard failure unless it is covered by an explicit reviewed ledger-correction row.
- Descriptor-family mappings must be explicitly present either in a reviewed expression ledger or, for pre-existing governed descriptors only, in the reviewed governed baseline descriptor-family map; no family inference.
- Withholds remain explicit and never become synthetic sensory content.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EXPECTED_RECORDS = 262
ALLOWED_FAMILIES = {
    "orchard-fruit", "citrus", "dried-fruit", "tropical", "sweet",
    "chocolate-coffee", "spice", "nutty", "oak", "floral-herbal",
    "maritime", "smoke-peat",
}


def evidence_rank(tier: str | None) -> int:
    """Rank competing research only; governed baseline fields are never replaced."""
    t = (tier or "").upper()
    if t.startswith("TIER_A_PHYSICAL"):
        return 100
    if t.startswith("TIER_1_OFFICIAL"):
        return 90
    if "OFFICIAL" in t and t.startswith("TIER_2"):
        return 80
    if t.startswith("TIER_2_ESTABLISHED"):
        return 70
    if t.startswith("GOVERNED_EXISTING"):
        return 60
    if t.startswith("WITHHELD"):
        return 10
    return 40


def load(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def fail(msg: str) -> None:
    raise SystemExit(msg)


def validate_family_map(descriptors: list[str], family_map: dict[str, str], context: str) -> None:
    for descriptor in descriptors:
        if descriptor not in family_map:
            fail(f"{context}: descriptor lacks explicit family mapping: {descriptor!r}")
        family = family_map[descriptor]
        if family not in ALLOWED_FAMILIES:
            fail(f"{context}: invalid family {family!r} for {descriptor!r}")


def load_baseline_family_map(path: Path) -> dict[str, str]:
    if not path.exists():
        fail(f"Governed baseline descriptor-family map not found: {path}")
    payload = load(path)
    if not isinstance(payload, dict):
        fail(f"{path}: expected object")
    declared = payload.get("allowedFamilies")
    if not isinstance(declared, list) or set(declared) != ALLOWED_FAMILIES or len(declared) != len(ALLOWED_FAMILIES):
        fail(f"{path}: allowedFamilies must declare exactly the 12 governed visual families")
    mapping = payload.get("descriptorFamilies")
    if not isinstance(mapping, dict):
        fail(f"{path}: descriptorFamilies must be an object")
    for descriptor, family in mapping.items():
        if not isinstance(descriptor, str) or not descriptor:
            fail(f"{path}: malformed descriptor key")
        if family not in ALLOWED_FAMILIES:
            fail(f"{path}: invalid family {family!r} for {descriptor!r}")
    return mapping


def load_explicit_corrections(progress_dir: Path) -> dict[tuple[str, str], str]:
    path = progress_dir / "ledger-corrections.json"
    if not path.exists():
        return {}
    payload = load(path)
    rows = payload.get("corrections") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        fail(f"{path}: corrections must be an array")
    corrections: dict[tuple[str, str], str] = {}
    for row in rows:
        ledger = row.get("ledger")
        bad = row.get("incorrectBeverageId")
        good = row.get("canonicalBeverageId")
        if not all(isinstance(v, str) and v for v in (ledger, bad, good)):
            fail(f"{path}: malformed correction row")
        corrections[(ledger, bad)] = good
    return corrections


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("manifest", type=Path, help="Verbatim Lovable 262-item completeness manifest")
    ap.add_argument("--progress-dir", type=Path, default=Path("data/sensory-research"))
    ap.add_argument(
        "--baseline-family-map",
        type=Path,
        default=Path("schema/governed-descriptor-family-map.json"),
        help="Reviewed explicit visual-family mappings for descriptors already present in the governed manifest",
    )
    ap.add_argument("--output", type=Path, default=Path("PROJECT_ZERO_SENSORY_MASTER.json"))
    args = ap.parse_args()

    manifest = load(args.manifest)
    if not isinstance(manifest, list) or len(manifest) != EXPECTED_RECORDS:
        fail(f"Manifest must contain exactly {EXPECTED_RECORDS} records")

    canonical: dict[str, dict[str, Any]] = {}
    for idx, row in enumerate(manifest, 1):
        if not isinstance(row, dict):
            fail(f"Manifest row {idx} is not an object")
        bid = row.get("beverageId")
        name = row.get("officialName")
        if not isinstance(bid, str) or not bid:
            fail(f"Manifest row {idx} missing beverageId")
        if bid in canonical:
            fail(f"Duplicate manifest beverageId: {bid}")
        if not isinstance(name, str) or not name:
            fail(f"Manifest row {idx} missing officialName")
        canonical[bid] = row

    baseline_family_map = load_baseline_family_map(args.baseline_family_map)
    explicit_corrections = load_explicit_corrections(args.progress_dir)
    research: dict[str, list[dict[str, Any]]] = {bid: [] for bid in canonical}
    # Only execution ledgers participate in assembly. Human-readable correction
    # artefacts such as progress-002-correction.json are governance records, not
    # research ledgers; the machine-readable correction lives in ledger-corrections.json.
    ledger_paths = sorted(
        p for p in args.progress_dir.glob("progress-*.json")
        if "-correction" not in p.stem
    )
    if not ledger_paths:
        fail(f"No progress ledgers found under {args.progress_dir}")

    corrections_applied: list[dict[str, str]] = []
    for path in ledger_paths:
        payload = load(path)
        records = payload.get("records") if isinstance(payload, dict) else None
        if not isinstance(records, list):
            fail(f"{path}: missing records array")
        for original_row in records:
            row = dict(original_row)
            bid = row.get("beverageId")
            if bid not in canonical:
                corrected = explicit_corrections.get((path.name, bid))
                if not corrected:
                    fail(f"{path}: research BeverageId not in canonical manifest and has no explicit correction: {bid}")
                if corrected not in canonical:
                    fail(f"{path}: correction target is not in canonical manifest: {corrected}")
                corrections_applied.append({"ledger": path.name, "from": bid, "to": corrected})
                bid = corrected
                row["beverageId"] = corrected
                row["governanceCorrectionApplied"] = True
            research[bid].append({**row, "_ledger": str(path)})

    output_records: list[dict[str, Any]] = []
    descriptor_coverage = 0
    narrative_coverage = 0
    explicit_withholds = 0
    research_filled_descriptors = 0
    research_filled_narratives = 0
    baseline_taxonomy_mappings_used = 0

    for bid in sorted(canonical):
        base = canonical[bid]
        existing_desc = list(base.get("currentDescriptors") or [])
        existing_note = base.get("currentTastingNote")
        candidates = research[bid]
        ranked = sorted(candidates, key=lambda r: evidence_rank(r.get("evidenceTier")), reverse=True)

        chosen_desc = existing_desc
        desc_source = "GOVERNED_EXISTING" if existing_desc else None
        family_map: dict[str, str] = {}

        if existing_desc:
            mapping_candidate = next(
                (r for r in ranked if all(d in (r.get("descriptorFamilies") or {}) for d in existing_desc)),
                None,
            )
            if mapping_candidate:
                fm = mapping_candidate.get("descriptorFamilies") or {}
                family_map = {d: fm[d] for d in existing_desc}
            else:
                missing = [d for d in existing_desc if d not in baseline_family_map]
                if missing:
                    fail(f"{bid}: governed existing descriptors lack reviewed taxonomy mappings: {missing}")
                family_map = {d: baseline_family_map[d] for d in existing_desc}
                baseline_taxonomy_mappings_used += 1
        else:
            desc_candidate = next((r for r in ranked if r.get("verifiedDescriptors")), None)
            if desc_candidate:
                chosen_desc = list(desc_candidate["verifiedDescriptors"])
                family_map = dict(desc_candidate.get("descriptorFamilies") or {})
                validate_family_map(chosen_desc, family_map, f"{bid} researched descriptors")
                desc_source = desc_candidate.get("evidenceTier")
                research_filled_descriptors += 1

        if chosen_desc:
            validate_family_map(chosen_desc, family_map, f"{bid} final descriptors")
            descriptor_coverage += 1

        chosen_note = existing_note
        note_source = "GOVERNED_EXISTING" if existing_note else None
        if not chosen_note:
            note_candidate = next((r for r in ranked if r.get("cask23TastingNarrative")), None)
            if note_candidate:
                chosen_note = note_candidate["cask23TastingNarrative"]
                note_source = note_candidate.get("evidenceTier")
                research_filled_narratives += 1

        if chosen_note:
            narrative_coverage += 1

        withhold_rows = [r for r in ranked if str(r.get("evidenceTier", "")).startswith("WITHHELD")]
        unresolved = not chosen_desc and not chosen_note
        if unresolved and withhold_rows:
            explicit_withholds += 1

        sources: list[str] = []
        for r in ranked:
            for src in r.get("sources") or []:
                if src not in sources:
                    sources.append(src)

        output_records.append({
            "beverageId": bid,
            "officialName": base["officialName"],
            "descriptors": chosen_desc,
            "descriptorFamilies": family_map,
            "tastingNarrative": chosen_note,
            "descriptorEvidence": desc_source,
            "narrativeEvidence": note_source,
            "governanceStatus": "WITHHELD" if unresolved and withhold_rows else ("ENRICHED" if chosen_desc or chosen_note else "ABSENT_UNRESOLVED"),
            "withholdReasons": [r.get("evidenceTier") for r in withhold_rows],
            "sources": sources,
        })

    payload = {
        "project": "PROJECT_ZERO_SENSORY_MASTER",
        "version": "1.0-candidate",
        "recordCount": len(output_records),
        "identityKey": "beverageId",
        "governanceRule": "Data chooses the icon; the icon never generates the data.",
        "metrics": {
            "descriptorCoverage": descriptor_coverage,
            "tastingNarrativeCoverage": narrative_coverage,
            "researchFilledDescriptorRecords": research_filled_descriptors,
            "researchFilledNarrativeRecords": research_filled_narratives,
            "explicitWithholds": explicit_withholds,
            "ledgerCount": len(ledger_paths),
            "explicitLedgerCorrectionsApplied": len(corrections_applied),
            "baselineTaxonomyMappingsUsed": baseline_taxonomy_mappings_used,
        },
        "ledgerCorrectionsApplied": corrections_applied,
        "records": output_records,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(json.dumps(payload["metrics"] | {"recordCount": len(output_records)}, indent=2))


if __name__ == "__main__":
    main()
