# PROJECT ZERO — LOVABLE DISTILLERY MASTER v1.2 DEPLOYMENT CONTRACT

**Status:** FOUNDER-APPROVED DEPLOYMENT INSTRUCTION  
**Canonical source:** `PROJECT_ZERO_DISTILLERY_MASTER.json` on `main`  
**Master version:** `1.2`  
**Canonical physical facilities:** `63`  
**Schema validation:** PASS  
**Open expression provenance queue:** `0`

## 0. Deployment objective

Deploy the complete Project Zero Distillery Master v1.2 package into the Lovable experience layer without inventing, duplicating or reclassifying distillery identities.

This is a **binding + presentation deployment**, not a new research pass. The GitHub governance repository is authoritative. Do not replace governed facility identities with brand labels, marketing names, independent bottlers, or inferred sources.

The deployment must preserve:

- all **63 canonical physical facility profiles** from `PROJECT_ZERO_DISTILLERY_MASTER.json`;
- all source-entity coverage already present in the v1.2 master;
- all exact v1.2 expression provenance decisions in `governance/pz-distillery-v1.2-expression-provenance.json`;
- the four v1.1 deterministic coverage overrides below;
- the six invalid Explore Distillery route suppressions below;
- the Cù Bòcan → Tomatin parent-facility rule below;
- the sensory smoke governance in `governance/pz-whisky-sensory-smoke-v1.1.json`.

Do not write back to Supabase canonical, C3 governance, staging, inventory, pricing, or unrelated whisky enrichment records as part of this deployment unless a later explicit Founder instruction authorises it.

---

## 1. Canonical facility package

Load the canonical distillery dataset from:

```text
PROJECT_ZERO_DISTILLERY_MASTER.json
```

Required master assertions before UI release:

```text
version == "1.2"
canonicalPhysicalFacilityProfiles == 63
approvedDistilleryEntityRowsCovered == 58
v11CoverageOverrideRows == 4
v12CoverageOverrideRows == 3
expressionProvenanceDecisions == 12
expressionFacilityBindings == 10
expressionBindingsTerminallyWithheld == 2
openExpressionProvenanceQueue == 0
schemaValidationPassed == true
suppressedNonFacilityExploreTargets == 6
```

If any assertion fails, stop the deployment and report the mismatch. Do not silently substitute a cached or older master.

---

## 2. Facility identity rule

Every Distillery card, Explore Distillery route and facility rack must resolve to a canonical physical facility record by `canonicalDistilleryId` / canonical `slug`.

**Never create a new physical-facility profile from a brand label alone.**

Allowed relationship types include governed aliases/brand-to-facility bindings and exact expression-level facility bindings. Independent bottlers and undisclosed-source brands remain separate from facility identity unless an exact governed expression binding exists.

---

## 3. Cù Bòcan — mandatory Tomatin parent-facility binding

Treat **Cù Bòcan / Cu Bocan** as the lightly peated/smoky range identity produced at **Tomatin Distillery**, not as a disconnected distillery entity.

Canonical destination:

```json
{
  "canonicalDistilleryId": "DIST-TOMATIN",
  "canonicalSlug": "tomatin",
  "officialName": "Tomatin Distillery"
}
```

Binding rule:

```text
IF whisky brand/range identity normalises to "Cù Bòcan" OR "Cu Bocan"
THEN parentDistilleryId = "DIST-TOMATIN"
AND parentDistillerySlug = "tomatin"
AND Explore Distillery route = canonical Tomatin Distillery page
AND include the expression in the Tomatin facility whisky rack when the expression itself is active/publishable
AND do NOT create a separate Cù Bòcan distillery profile
```

Preserve the range identity **Cù Bòcan** on the whisky/product presentation. Only the structural parent distillery is Tomatin.

The governed Tomatin facility profile already distinguishes the two production streams: core Tomatin spirit is unpeated, while a separate lightly peated production run is made for Cu Bocan. Do not apply Cù Bòcan peat/smoke characteristics to ordinary Tomatin expressions.

---

## 4. Four v1.1 deterministic coverage overrides

Apply these exact directory/entity bindings. No fuzzy matching.

```json
[
  {
    "directorySlug": "glenscotia",
    "canonicalSlug": "glen-scotia",
    "relationship": "LEGACY_ALIAS_TO_CANONICAL_FACILITY"
  },
  {
    "directorySlug": "amrut",
    "canonicalSlug": "amrut",
    "relationship": "BRAND_LABEL_RESOLVES_TO_SINGLE_PHYSICAL_FACILITY"
  },
  {
    "directorySlug": "indri",
    "canonicalSlug": "piccadily-indri",
    "relationship": "BRAND_LABEL_RESOLVES_TO_SINGLE_PHYSICAL_FACILITY"
  },
  {
    "directorySlug": "paul-john",
    "canonicalSlug": "john-distilleries-goa",
    "relationship": "BRAND_LABEL_RESOLVES_TO_SINGLE_PHYSICAL_FACILITY"
  }
]
```

These four rules remain active alongside, not instead of, the v1.2 coverage overrides already present in the master.

---

## 5. v1.2 coverage + expression provenance

Consume `governance/pz-distillery-v1.2-expression-provenance.json` exactly.

The three v1.2 brand-level coverage overrides are:

```text
old-pulteney -> pulteney
hudson -> tuthilltown
evan-williams -> heaven-hill
```

Also apply all 12 expression adjudications from that file. Ten expressions are exact facility bindings. Two are terminally withheld and **must not** be forced onto a facility rack:

```text
WhistlePig Old World 12 Y 43%
  -> WITHHELD_SOURCE_TRANSITION_AMBIGUITY

Uncle Nearest 100 Proof 50%
  -> WITHHELD_BOTTLING_ERA_AMBIGUITY
```

A terminally withheld result is a completed governance decision, not an unresolved queue item.

For Uncle Nearest, the customer may explore Nearest Green as the brand-associated physical home if the UX distinguishes that relationship, but the withheld BeverageId itself must not be presented as proven to have been distilled there.

---

## 6. Six invalid Explore Distillery link suppressions

The following entities must **not** receive a generic Explore Distillery route from their brand/entity identity:

```json
[
  {
    "directorySlug": "douglas-laing-s",
    "entityType": "INDEPENDENT_BOTTLER",
    "policy": "NO_DISTILLERY_ROUTE"
  },
  {
    "directorySlug": "signatory-vintage",
    "entityType": "INDEPENDENT_BOTTLER",
    "policy": "NO_DISTILLERY_ROUTE"
  },
  {
    "directorySlug": "mossburn",
    "entityType": "INDEPENDENT_BOTTLER",
    "policy": "NO_DISTILLERY_ROUTE"
  },
  {
    "directorySlug": "that-boutique-y-whisky-co",
    "entityType": "INDEPENDENT_BOTTLER",
    "policy": "NO_DISTILLERY_ROUTE"
  },
  {
    "directorySlug": "gleann-mor",
    "entityType": "INDEPENDENT_BOTTLER",
    "policy": "NO_DISTILLERY_ROUTE"
  },
  {
    "directorySlug": "smokehead",
    "entityType": "UNDISCLOSED_DISTILLERY",
    "policy": "NO_DISTILLERY_ROUTE"
  }
]
```

UX requirement:

```text
NO_DISTILLERY_ROUTE => hide/omit generic Explore Distillery CTA.
```

Do not render a disabled or misleading link. If a specific expression under an independent bottler has a separate exact governed physical-facility binding, that expression may link to that physical facility through the expression binding only.

Smokehead remains undisclosed Islay single malt. Do not infer or expose a distillery.

---

## 7. Sensory smoke-meter governance — locked layout fix

Consume:

```text
governance/pz-whisky-sensory-smoke-v1.1.json
```

Required rendering precedence:

```text
1. explicit governed/panel-approved sensory smoke value
2. allowed peat-level derivation for peated records only
3. absence
```

Required derivation contract:

```json
{
  "Unpeated": null,
  "Lightly peated": 2,
  "Moderately peated": 3,
  "Heavily peated": 5
}
```

### Critical unpeated presentation rule

For a whisky that is **Unpeated** and has **no explicit governed sensory smoke value**:

```text
DO NOT render Smoke = 1
DO NOT render Smoke = 0
DO NOT render an empty Smoke gauge
DO NOT reserve a blank Smoke-axis slot
OMIT the Smoke dimension from the customer-facing sensory meter/layout
REFLOW the remaining dimensions cleanly so no visual gap is left
```

For unknown/absent peat with no explicit sensory smoke value, also omit the Smoke dimension.

This is non-destructive. Continue to display textual peat facts such as `Unpeated` where appropriate. Never overwrite an explicit governed sensory smoke value.

For peated records without a separately governed smoke dimension, the allowed derived values remain:

```text
Lightly peated -> Smoke 2
Moderately peated -> Smoke 3
Heavily peated -> Smoke 5
```

Cù Bòcan must therefore keep its own governed/lightly peated product facts and may use the peated derivation path where no higher-precedence explicit smoke value exists. Its Tomatin parent binding must not cause core unpeated Tomatin expressions to inherit Cù Bòcan smoke.

---

## 8. Distillery page/rack behaviour

For every canonical facility page:

1. Render facility identity from the canonical profile only.
2. Render Water, Malt, Fermentation, Stills, Maturation and other governed production fields only when present in that facility profile.
3. Populate the whisky rack only from exact structural bindings or approved coverage rules.
4. Never populate a rack by name similarity.
5. Never make a withheld expression appear facility-proven.
6. Preserve whisky brand/range identity on product cards even when the parent facility differs from the brand name.
7. Cù Bòcan expressions must appear structurally under Tomatin while retaining Cù Bòcan as the displayed range/brand.

---

## 9. Data safety / anti-regression rules

Do not:

- create a 64th facility for Cù Bòcan;
- create facility pages for Douglas Laing's, Signatory Vintage, Mossburn, That Boutique-y Whisky Co., Gleann Mòr or Smokehead;
- collapse independent bottler identity into a distillery identity;
- infer Smokehead's source distillery;
- convert either terminally withheld v1.2 expression into a facility binding;
- derive customer-facing Smoke from `Unpeated`;
- leave a dead/blank smoke-meter axis after omission;
- overwrite explicit governed smoke values;
- apply Cù Bòcan peat/smoke characteristics globally to Tomatin;
- use fuzzy string matching to create new governance relationships;
- mutate unrelated inventory, price, availability or checkout data.

---

## 10. Acceptance tests — must all pass before lifting the hold

```text
[ ] Master version displayed/loaded = 1.2
[ ] Canonical facility count = 63 exactly
[ ] No duplicate canonical distilleryId
[ ] No duplicate canonical facility slug
[ ] Cù Bòcan resolves to DIST-TOMATIN / tomatin
[ ] No standalone Cù Bòcan distillery page exists
[ ] Core Tomatin remains unpeated unless expression evidence says otherwise
[ ] All 4 v1.1 coverage overrides resolve exactly
[ ] All 3 v1.2 coverage overrides resolve exactly
[ ] All 12 v1.2 expression decisions are honoured
[ ] 10 v1.2 expressions are facility-bound
[ ] 2 v1.2 expressions remain terminally withheld
[ ] Open provenance queue = 0
[ ] All 6 NO_DISTILLERY_ROUTE entities have no generic Explore Distillery CTA
[ ] Smokehead has no inferred physical distillery route
[ ] Unpeated + no explicit smoke => Smoke dimension absent
[ ] Unpeated smoke omission leaves no empty layout gap
[ ] Explicit governed smoke values still render
[ ] Peated fallback derivation remains 2 / 3 / 5 only
[ ] Textual peat facts remain intact
[ ] No unrelated Supabase/inventory/pricing writes performed
```

If any acceptance test fails, keep the Lovable hold in place and report the exact failing assertion before making further changes.

---

## 11. Completion report required from Lovable

Return one concise implementation report containing:

```text
A. master version loaded
B. canonical facility count
C. Cù Bòcan -> Tomatin binding result
D. 4 v1.1 override results
E. 3 v1.2 override results
F. v1.2 expression binding count + withheld count
G. 6 suppression results
H. smoke-meter regression test results
I. confirmation that no 64th/duplicate facility was created
J. confirmation that no unrelated production writes occurred
K. list of files/components changed
L. any remaining blocker
```

Do not mark deployment complete until every acceptance test above is green.

---

## Founder intent

The Distillery experience is a physical-production map, not a brand-directory shortcut. Brand identities may route to a facility only through governed deterministic rules. Cù Bòcan is a distinct smoky/peated Tomatin range identity, but its physical distilling parent is Tomatin Distillery. Where provenance is uncertain, withhold rather than guess. Where smoke is absent, do not manufacture a customer-facing smoke score.