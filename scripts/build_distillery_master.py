#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "cask23-distillery-profile.schema.json"
DATA_DIR = ROOT / "data" / "distilleries"
RECON_PATH = ROOT / "reconciliation" / "pz-distillery-00-entity-reconciliation.json"
OUT_PATH = ROOT / "PROJECT_ZERO_DISTILLERY_MASTER.json"

# The approved 58 DISTILLERY directory rows collapse to 55 physical assets because
# three rows are duplicate naming aliases for the same hardware facilities.
ALIAS_TO_CANONICAL_SLUG = {
    "the-benriach": "benriach",
    "the-glendronach": "glendronach",
    "kavalan-distillery": "kavalan",
    "filey-bay": "spirit-of-yorkshire",
    "wire-works": "white-peak",
    "the-dalmore": "dalmore",
    "milk-and-honey": "milk-and-honey"
}

with SCHEMA_PATH.open(encoding="utf-8") as f:
    schema = json.load(f)
validator = Draft202012Validator(schema)

profiles = []
errors = []
for path in sorted(DATA_DIR.glob("dist-*.json")):
    with path.open(encoding="utf-8") as f:
        profile = json.load(f)
    validation_errors = sorted(validator.iter_errors(profile), key=lambda e: list(e.path))
    if validation_errors:
        for err in validation_errors:
            errors.append(f"{path.name}: {'/'.join(map(str, err.path)) or '<root>'}: {err.message}")
    profiles.append(profile)

if errors:
    raise SystemExit("Schema validation failed:\n" + "\n".join(errors))

ids = [p["distilleryId"] for p in profiles]
slugs = [p["slug"] for p in profiles]
if len(ids) != len(set(ids)):
    raise SystemExit("Duplicate distilleryId detected")
if len(slugs) != len(set(slugs)):
    raise SystemExit("Duplicate canonical slug detected")
if any(p["governanceStatus"] != "SOURCE_VERIFIED" for p in profiles):
    raise SystemExit("All canonical profiles must be SOURCE_VERIFIED before master assembly")
if any(not p.get("sources") for p in profiles):
    raise SystemExit("Every profile must contain at least one source URL")

with RECON_PATH.open(encoding="utf-8") as f:
    reconciliation = json.load(f)
distillery_rows = [e for e in reconciliation["entities"] if e.get("entityType") == "DISTILLERY"]

profile_by_slug = {p["slug"]: p for p in profiles}
coverage = []
unresolved = []
for entity in distillery_rows:
    directory_slug = entity["directorySlug"]
    target_slug = ALIAS_TO_CANONICAL_SLUG.get(directory_slug, directory_slug)
    # Facility-led mappings may carry an explicit canonical name but not the profile slug.
    if directory_slug == "filey-bay":
        target_slug = "spirit-of-yorkshire"
    elif directory_slug == "wire-works":
        target_slug = "white-peak"
    elif directory_slug == "the-dalmore":
        target_slug = "dalmore"
    elif directory_slug == "milk-and-honey":
        # Current canonical profile may use either human slug or short implementation slug.
        if "milk-and-honey" not in profile_by_slug and "mh" in profile_by_slug:
            target_slug = "mh"
    profile = profile_by_slug.get(target_slug)
    if profile is None:
        unresolved.append({"directorySlug": directory_slug, "targetSlug": target_slug})
    else:
        coverage.append({
            "directorySlug": directory_slug,
            "entityName": entity["entityName"],
            "canonicalDistilleryId": profile["distilleryId"],
            "canonicalSlug": profile["slug"]
        })

if unresolved:
    raise SystemExit("Unresolved approved DISTILLERY rows: " + json.dumps(unresolved, ensure_ascii=False))

expected_rows = 58
expected_canonical = 55
if len(distillery_rows) != expected_rows:
    raise SystemExit(f"Expected {expected_rows} approved DISTILLERY rows, found {len(distillery_rows)}")
if len(profiles) != expected_canonical:
    raise SystemExit(f"Expected {expected_canonical} canonical physical facilities after alias consolidation, found {len(profiles)}")
if len(coverage) != expected_rows:
    raise SystemExit(f"Expected coverage for {expected_rows} approved rows, found {len(coverage)}")

all_sources = [url for p in profiles for url in p.get("sources", [])]
unique_sources = sorted(set(all_sources))
tier_counts = {}
for p in profiles:
    tier_counts[p["evidenceTier"]] = tier_counts.get(p["evidenceTier"], 0) + 1

master = {
    "project": "PROJECT_ZERO_DISTILLERY_MASTER",
    "version": "1.0",
    "generatedDate": "2026-08-23",
    "governanceStatus": "FOUNDER_REVIEW",
    "metrics": {
        "approvedDistilleryEntityRowsCovered": len(coverage),
        "canonicalPhysicalFacilityProfiles": len(profiles),
        "aliasRowsCollapsed": len(coverage) - len(profiles),
        "schemaValidationPassed": True,
        "profileSourceReferences": len(all_sources),
        "uniqueSourceUrls": len(unique_sources),
        "evidenceTierCounts": tier_counts
    },
    "sourceEntityCoverage": coverage,
    "profiles": sorted(profiles, key=lambda p: p["officialName"].casefold())
}

with OUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(json.dumps(master["metrics"], indent=2))
print(f"Wrote {OUT_PATH}")
