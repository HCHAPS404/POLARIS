# ADR-0003 — Flutter for Horizon Mobile

**Evidence:** DESIGNED. `apps/horizon-mobile` is README-only in P0.

## Status

Accepted — 2026-10-01

## Context

Field users need offline-capable capture and alert receipt. Notion listed Flutter **or** React Native as a future option, and Qt/PySide6 for the edge station. Web apps (Horizon, Vector, Forge) stay on the web stack.

## Decision

**Flutter** is the mobile client for `apps/horizon-mobile`. Qt/PySide remains a possible **edge/desktop** path under hardware/edge docs, not the phone app.

CI `mobile.yml` must **skip** until a `pubspec.yaml` exists so README-only P0 does not fail `main`.

## Alternatives

- React Native — rejected to keep one mobile toolchain
- PWA only — insufficient offline/sensor story for brigades
- Qt on mobile — rejected (team size, store packaging)

## Consequences

No Dart code in P0. Agents must not generate a full Flutter app unless a later phase asks. Nested `apps/horizon-mobile/AGENTS.md` binds mobile work.

## Validation

Directory + README + path-filtered workflow. Absence of `pubspec.yaml` is intentional.
