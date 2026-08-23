#!/usr/bin/env python3
import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "cask23-distillery-profile.schema.json"
DATA_DIR = ROOT / "data" / "distilleries"
RECON_PATH = ROOT / "reconciliation" / "pz-distillery-00-entity-reconciliation.json"
V11_OVERRIDE_PATH = ROOT / "governance" / "pz-distillery-v1.1-coverage-overrides.json"
V12_PROVENANCE_PATH = ROOT / "governance" / "pz-distillery-v1.2-expression-provenance.json"
SMOKE_POLICY_PATH = ROOT / "governance" / "pz-whisky-sensory-smoke-v1.1.json"
OUT_PATH = ROOT / "PROJECT_ZERO_DISTILLERY_MASTER.json"

ALIAS_TO_CANONICAL_SLUG = {
    "ardmore-distillery": "ardmore", "ardnahoe-distillery": "ardnahoe",
    "balblair-distillery": "balblair", "balcones-distilling": "balcones",
    "barton-1792-distillery": "barton-1792", "buffalo-trace-distillery": "buffalo-trace",
    "bunnahabhain-distillery": "bunnahabhain", "deanston-distillery": "deanston",
    "fettercairn-distillery": "fettercairn", "few-spirits-llc": "few-spirits",
    "filey-bay": "spirit-of-yorkshire", "four-roses-distillery": "four-roses",
    "glenglassaugh-distillery": "glenglassaugh", "heaven-hill-distillery": "heaven-hill",
    "kavalan-distillery": "kavalan", "macduff-distillery": "macduff",
    "milk-and-honey": "mh-distillery", "the-benriach": "benriach",
    "the-dalmore": "dalmore", "the-glendronach": "glendronach",
    "tomatin-distillery": "tomatin", "tullibardine-distillery": "tullibardine",
    "wire-works": "white-peak", "wolfburn-distillery": "wolfburn"
}

with SCHEMA_PATH.open(encoding="utf-8") as f: schema = json.load(f)
validator = Draft202012Validator(schema)
profiles, errors = [], []
for path in sorted(DATA_DIR.glob("dist-*.json")):
    with path.open(encoding="utf-8") as f: profile = json.load(f)
    for err in sorted(validator.iter_errors(profile), key=lambda e: list(e.path)):
        errors.append(f"{path.name}: {'/'.join(map(str, err.path)) or '<root>'}: {err.message}")
    profiles.append(profile)
if errors: raise SystemExit("Schema validation failed:\n" + "\n".join(errors))

ids = [p["distilleryId"] for p in profiles]; slugs = [p["slug"] for p in profiles]
if len(ids) != len(set(ids)): raise SystemExit("Duplicate distilleryId detected")
if len(slugs) != len(set(slugs)): raise SystemExit("Duplicate canonical slug detected")
if any(p["governanceStatus"] != "SOURCE_VERIFIED" for p in profiles): raise SystemExit("All profiles must be SOURCE_VERIFIED")
if any(not p.get("sources") for p in profiles): raise SystemExit("Every profile must contain source tracking")

with RECON_PATH.open(encoding="utf-8") as f: reconciliation = json.load(f)
with V11_OVERRIDE_PATH.open(encoding="utf-8") as f: v11 = json.load(f)
with V12_PROVENANCE_PATH.open(encoding="utf-8") as f: v12 = json.load(f)
with SMOKE_POLICY_PATH.open(encoding="utf-8") as f: smoke = json.load(f)

distillery_rows = [e for e in reconciliation["entities"] if e.get("entityType") == "DISTILLERY"]
profile_by_slug = {p["slug"]: p for p in profiles}
coverage, unresolved = [], []

def add_coverage(directory_slug, entity_name, target_slug, relationship, source):
    if any(r["directorySlug"] == directory_slug for r in coverage):
        raise SystemExit(f"Duplicate sourceEntityCoverage directorySlug: {directory_slug}")
    profile = profile_by_slug.get(target_slug)
    if not profile:
        unresolved.append({"directorySlug": directory_slug, "targetSlug": target_slug, "source": source}); return
    coverage.append({"directorySlug": directory_slug, "entityName": entity_name,
        "canonicalDistilleryId": profile["distilleryId"], "canonicalSlug": profile["slug"], "relationship": relationship})

for e in distillery_rows:
    d = e["directorySlug"]
    add_coverage(d, e["entityName"], ALIAS_TO_CANONICAL_SLUG.get(d, d), "PZ_DISTILLERY_00_APPROVED", "v1.0")
for o in v11.get("coverageOverrides", []):
    add_coverage(o["directorySlug"], o["directorySlug"], o["canonicalSlug"], o["relationship"], "v1.1")
for o in v12.get("coverageOverrides", []):
    add_coverage(o["directorySlug"], o["directorySlug"], o["canonicalSlug"], o["relationship"], "v1.2")
if unresolved: raise SystemExit("Unresolved facility coverage rows: " + json.dumps(unresolved, ensure_ascii=False))

expected_distillery_rows, expected_profiles, expected_v11, expected_v12 = 58, 63, 4, 3
if len(distillery_rows) != expected_distillery_rows: raise SystemExit(f"Expected 58 approved DISTILLERY rows, found {len(distillery_rows)}")
if len(profiles) != expected_profiles: raise SystemExit(f"Expected 63 canonical facilities in v1.2, found {len(profiles)}")
if len(v11.get("coverageOverrides", [])) != expected_v11: raise SystemExit("Expected 4 v1.1 coverage overrides")
if len(v12.get("coverageOverrides", [])) != expected_v12: raise SystemExit("Expected 3 v1.2 coverage overrides")
if len(v12.get("expressionFacilityBindings", [])) != 12: raise SystemExit("Expected 12 v1.2 expression provenance decisions")

expr = v12["expressionFacilityBindings"]
expr_ids = [x["beverageId"] for x in expr]
if len(expr_ids) != len(set(expr_ids)): raise SystemExit("Duplicate BeverageId in v1.2 expression provenance")
bound = [x for x in expr if x["status"] == "BOUND"]
withheld = [x for x in expr if x["status"] != "BOUND"]
for x in bound:
    if x.get("canonicalSlug") not in profile_by_slug: raise SystemExit(f"Expression binding targets missing profile: {x['beverageId']}")
if len(bound) != 10 or len(withheld) != 2: raise SystemExit("Expected 10 bound and 2 terminally withheld expression decisions")

all_sources = [u for p in profiles for u in p.get("sources", [])]
tier_counts = {}
for p in profiles: tier_counts[p["evidenceTier"]] = tier_counts.get(p["evidenceTier"], 0) + 1

master = {
  "project": "PROJECT_ZERO_DISTILLERY_MASTER", "version": "1.2", "generatedDate": "2026-08-23",
  "governanceStatus": "FOUNDER_REVIEW",
  "metrics": {
    "approvedDistilleryEntityRowsCovered": len(distillery_rows), "canonicalPhysicalFacilityProfiles": len(profiles),
    "v11AdditionalFacilityProfiles": 3, "v12AdditionalFacilityProfiles": 5,
    "v11CoverageOverrideRows": expected_v11, "v12CoverageOverrideRows": expected_v12,
    "sourceEntityCoverageRows": len(coverage), "expressionProvenanceDecisions": len(expr),
    "expressionFacilityBindings": len(bound), "expressionBindingsTerminallyWithheld": len(withheld),
    "openExpressionProvenanceQueue": 0, "schemaValidationPassed": True,
    "profileSourceReferences": len(all_sources), "uniqueSourceUrls": len(set(all_sources)), "evidenceTierCounts": tier_counts,
    "suppressedNonFacilityExploreTargets": len(v11.get("suppressExploreDistillery", []))
  },
  "sourceEntityCoverage": sorted(coverage, key=lambda r: r["directorySlug"]),
  "expressionProvenance": expr,
  "terminalWithheldExpressions": v12.get("terminalWithheldExpressions", []),
  "presentationGovernance": {"suppressExploreDistillery": v11.get("suppressExploreDistillery", []), "provenanceReviewQueue": []},
  "sensoryGovernance": {"policyId": smoke["policyId"], "version": smoke["version"], "rules": smoke["rules"],
      "derivedSmokeFromPeatLevel": smoke["derivedSmokeFromPeatLevel"], "implementationNote": smoke["implementationNote"]},
  "profiles": sorted(profiles, key=lambda p: p["officialName"].casefold())
}
with OUT_PATH.open("w", encoding="utf-8") as f:
    json.dump(master, f, ensure_ascii=False, indent=2); f.write("\n")
print(json.dumps(master["metrics"], indent=2)); print(f"Wrote {OUT_PATH}")
