# ADR-0005 — Apache License 2.0

**Evidence:** IMPLEMENTED (`LICENSE`).

## Status

Accepted — 2026-10-01

## Context

POLARIS is open-source-first (Notion §1.4, §23.4) and will mix software, schemas, and later hardware artefacts. Contributors need an explicit grant, including patent peace, without copyleft that blocks institutional partners.

## Decision

License the repository under **Apache License 2.0**.

Hardware design files (KiCad, CAD) inherit Apache-2.0 unless a specific file states otherwise (e.g. third-party datasheets — those must not be copied if proprietary).

## Alternatives

- MIT — simpler, weaker patent grant; rejected for a cyber-physical system
- GPL-3.0 — copyleft may block government/NGO integration
- Proprietary — contradicts the competition and research stance

## Consequences

All contributions are Apache-2.0 unless a third-party notice applies. SBOM work remains P6.

## Validation

`LICENSE` at repo root; README and CONTRIBUTING reference this ADR.
