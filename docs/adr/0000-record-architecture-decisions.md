# ADR-0000 — Record architecture decisions

**Evidence:** IMPLEMENTED (process).

## Status

Accepted — 2026-10-01

## Context

POLARIS is a three-person IEEE Response Quest 2026 effort. Architecture currently lives in Notion and chat. Agents will otherwise invent conflicting trees (`packages/sim` vs the canonical modular monolith).

## Decision

Architecture Decision Records live in `docs/adr/`, numbered `NNNN-kebab-title.md`, with sections Status, Context, Decision, Alternatives, Consequences, Validation.

## Alternatives

- Wiki-only decisions — rejected (not in git)
- ADRs inside Notion — rejected as source of truth (Notion remains product notes)

## Consequences

Every stack or product-surface choice that binds implementers (monolith vs services, NATS, Flutter, C++ kernel, license) gets an ADR before mass implementation.

## Validation

This directory exists; ADR-0001–0005 are filed with the P0 foundation PR.
