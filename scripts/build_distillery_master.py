#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "cask23-distillery-profile.schema.json"
DATA_DIR = ROOT / "data" / "distilleries"
RECON_PATH = ROOT / "reconciliation" / "pz-distillery-00-entity-reconciliation.json"
V11_OVERRIDE_PATH = ROOT / "governance" / "pz-distillery-v1.1-coverage-overrides.json"
SMOKE_POLICY_PATH = ROOT / "governance" / "pz-whisky-sensory-smoke-v1.1.json"
OUT_PATH = ROOT / "PROJECT_ZERO_DISTILLERY_MASTER.json"

# Exact, founder-approved directory-row -> canonical physical-facility slug bindings.
# These are deterministic aliases only; no fuzzy/name-similarity matching is permitted.
ALIAS_TO_CANONICAL_SLUG = {
    "ardmore-distillery": "ardmore",
    "ardnahoe-distillery": "ardnahoe",
    "balblair-distillery": "balblair",
    "balcones-distilling": "balcones",
    "barton-1792-distillery": "barton-1792",
    "buffalo-trace-distillery": "buffalo-trace",
    "bunnahabhain-distillery": "bunnahabhain",
    "deanston-distillery": "deanston",
    "fettercairn-distillery": "fettercairn",
    "few-spirits-llc": "few-spirits",
    "filey-bay": "spirit-of-yorkshire",
    "four-roses-distillery": "four-roses",
    "glenglassaugh-distillery": "glenglassaugh",
    "heaven-hill-distillery": "heaven-hill",
    "kavalan-distillery": "kavalan",
    "macduff-distillery": "macduff",
    "milk-and-honey": "mh-distillery",
    "the-benriach": "benriach",
    "the-dalmore": "dalmore",
    "the-glendronach": "glendronach",
    "tomatin-distillery": "tomatin",
    "tullibardine-distillery": "tullibardine",
    "wire-works": "white-peak",
    "wolfburn-distillery": "wolfburn"
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
with V11_OVERRIDE_PATH.open(encoding="utf-8") as f:
    v11_overrides = json.load(f)
with SMOKE_POLICY_PATH.open(encoding="utf-8") as f:
    smoke_policy = json.load(f)

distillery_rows = [e for e in reconciliation["entities"] if e.get("entityType") == "DISTILLERY"]
profile_by_slug = {p["slug"]: p for p in profiles}
coverage = []
unresolved = []

# Founder-approved PZ-DISTILLERY-00 DISTILLERY rows.
for entity in distillery_rows:
    directory_slug = entity["directorySlug"]
    target_slug = ALIAS_TO_CANONICAL_SLUG.get(directory_slug, directory_slug)
    profile = profile_by_slug.get(target_slug)
    if profile is None:
        unresolved.append({"directorySlug": directory_slug, "targetSlug": target_slug})
    else:
        coverage.append({
            "directorySlug": directory_slug,
            "entityName": entity["entityName"],
            "canonicalDistilleryId": profile["distilleryId"],
            "canonicalSlug": profile["slug"],
            "relationship": "PZ_DISTILLERY_00_APPROVED"
        })

# v1.1 exact deterministic coverage corrections. These may resolve legacy aliases or
# governed brand labels to one proven physical facility. No string similarity is allowed.
for override in v11_overrides.get("coverageOverrides", []):
    directory_slug = override["directorySlug"]
    target_slug = override["canonicalSlug"]
    if any(row["directorySlug"] == directory_slug for row in coverage):
        raise SystemExit(f"Duplicate sourceEntityCoverage directorySlug: {directory_slug}")
    profile = profile_by_slug.get(target_slug)
    if profile is None:
        unresolved.append({"directorySlug": directory_slug, "targetSlug": target_slug, "source": "v1.1 override"})
    else:
        coverage.append({
            "directorySlug": directory_slug,
            "entityName": directory_slug,
            "canonicalDistilleryId": profile["distilleryId"],
            "canonicalSlug": profile["slug"],
            "relationship": override["relationship"]
        })

if unresolved:
    raise SystemExit("Unresolved approved facility coverage rows: " + json.dumps(unresolved, ensure_ascii=False))

expected_distillery_rows = 58
expected_canonical = 58
expected_v11_overrides = 4
if len(distillery_rows) != expected_distillery_rows:
    raise SystemExit(f"Expected {expected_distillery_rows} approved DISTILLERY rows, found {len(distillery_rows)}")
if len(profiles) != expected_canonical:
    raise SystemExit(f"Expected {expected_canonical} canonical physical facilities in v1.1, found {len(profiles)}")
if len(v11_overrides.get("coverageOverrides", [])) != expected_v11_overrides:
    raise SystemExit(f"Expected {expected_v11_overrides} v1.1 coverage overrides")
if len(coverage) != expected_distillery_rows + expected_v11_overrides:
    raise SystemExit("Source entity coverage count mismatch")

all_sources = [url for p in profiles for url in p.get("sources", [])]
unique_sources = sorted(set(all_sources))
tier_counts = {}
for p in profiles:
    tier_counts[p["evidenceTier"]] = tier_counts.get(p["evidenceTier"], 0) + 1

master = {
    "project": "PROJECT_ZERO_DISTILLERY_MASTER",
    "version": "1.1",
    "generatedDate": "2026-08-23",
    "governanceStatus": "FOUNDER_REVIEW",
    "metrics": {
        "approvedDistilleryEntityRowsCovered": len(distillery_rows),
        "canonicalPhysicalFacilityProfiles": len(profiles),
        "v11AdditionalFacilityProfiles": 3,
        "coverageOverrideRows": expected_v11_overrides,
        "sourceEntityCoverageRows": len(coverage),
        "schemaValidationPassed": True,
        "profileSourceReferences": len(all_sources),
        "uniqueSourceUrls": len(unique_sources),
        "evidenceTierCounts": tier_counts,
        "suppressedNonFacilityExploreTargets": len(v11_overrides.get("suppressExploreDistillery", [])),
        "provenanceReviewQueueCount": len(v11_overrides.get("provenanceReviewQueue", []))
    },
    "sourceEntityCoverage": sorted(coverage, key=lambda r: r["directorySlug"]),
    "presentationGovernance": {
        "suppressExploreDistillery": v11_overrides.get("suppressExploreDistillery", []),
        "provenanceReviewQueue": v11_overrides.get("provenanceReviewQueue", [])
    },
    "sensoryGovernance": {
        "policyId": smoke_policy["policyId"],
        "version": smoke_policy["version"],
        "rules": smoke_policy["rules"],
        "derivedSmokeFromPeatLevel": smoke_policy["derivedSmokeFromPeatLevel"],
        "implementationNote": smoke_policy["implementationNote"]
    },
    "profiles": sorted(profiles, key=lambda p: p["officialName"].casefold())
}

with OUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2)
    f.write("\n")

print(json.dumps(master["metrics"], indent=2))
print(f"Wrote {OUT_PATH}")
