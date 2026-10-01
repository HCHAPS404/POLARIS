# ADR-0001 — Modular monolith with hexagonal and clean boundaries

**Evidence:** DESIGNED (runtime still a single FastAPI process) · tree IMPLEMENTED.

## Status

Accepted — 2026-10-01

## Context

Notion describes many services (API, workers, MQTT, GIS, Qt, mobile, firmware). A three-person team cannot operate a microservice mesh before the first index exists. A previous gap analysis inferred `packages/` + `sim/`; Helmut’s canonical scaffold is `apps/`, `platform/`, `domains/`, `hazards/`, `simulation/`.

## Decision

Ship a **modular monolith**:

- One deployable API (`platform/api`)
- Bounded contexts as packages (`domains/*`, `hazards/*`)
- Hexagonal ports in `platform/ports`, adapters in `platform/adapters` and `adapters/`
- Delivery apps remain separate folders but consume the API; they are not a second backend

MVP freeze: decision-support, human-in-the-loop, **one hazard** as the first vertical after P0, graphs conceptually central but not implemented until P5.

## Alternatives

- Microservices from day one — rejected (ops cost)
- `packages/indices` + `sim/` tree — rejected (not canonical)
- Modular monolith without ports — rejected (domain would couple to FastAPI/NATS)

## Consequences

Extract a service only when a context has its own scale or failure domain. Agents must not add new top-level engine trees.

## Validation

Canonical paths exist and are described in `README_ARCHITECTURE.md`. `GET /health` is the only API behaviour marked IMPLEMENTED.
