# ADR-0002 — NATS as internal event bus

**Evidence:** DESIGNED (compose skeleton only). No publishers/subscribers in P0.

## Status

Accepted — 2026-10-01

## Context

Need to separate: (1) batch ETL, (2) near-real-time observations, (3) internal domain events, (4) IoT telemetry. Notion mentioned Redis Streams **or** NATS plus MQTT for sensors.

## Decision

- **NATS** (and later JetStream if persistence is required) is the **internal** event bus for domain events (observation accepted, index computed, alert proposed).
- **MQTT** remains the **device** telemetry channel (Mosquitto in dev).
- Airflow or cron-like jobs (future) own batch; they must not be sold as real-time.

Event payloads follow `schemas/` envelopes (`event_id`, `occurred_at`, `source`, `provenance`).

## Alternatives

- Redis Streams as the only bus — viable, but NATS matches fan-out and subject naming for many hazard types
- Kafka — rejected for P0–P4 ops weight
- Everything through FastAPI request/response — rejected (couples workers to HTTP)

## Consequences

Compose includes NATS as a **dev skeleton**, not production clustering. Domain code depends on a port, not a NATS client.

## Validation

`docker-compose.yml` / `infra/compose` declare a NATS service. No production HA config is claimed.
