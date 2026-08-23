# Cask 23 Whisky Governance

This repository is the controlled source of truth for Project Zero whisky-governance research outputs.

## Repository structure

- `schema/` — locked JSON schemas for governed profile records.
- `reconciliation/` — entity-reconciliation maps and source-freeze audits.
- `profiles/` — one governed distillery profile per file, added only after reconciliation.
- `evidence/` — optional structured evidence manifests supporting profile records.

## Governance lifecycle

`UNVERIFIED` → `SOURCE_VERIFIED` → `FOUNDER_REVIEW` → `FOUNDER_APPROVED`

Research branches are opened per controlled batch. Nothing becomes `FOUNDER_APPROVED` until Founder review and merge.

## Entity types

- `DISTILLERY`
- `INDEPENDENT_BOTTLER`
- `BRAND/PRODUCER`
- `UNDISCLOSED_DISTILLERY`
- `REVIEW_REQUIRED`

## Research rule

Primary/official sources are preferred for technical production facts. Established specialist sources may corroborate gaps. Missing facts remain absent; no field is populated by inference merely for completeness.

## Implementation boundary

Lovable is a rendering/implementation consumer of approved deterministic JSON packages. It is not the authority for research, identity resolution, or governance decisions.
