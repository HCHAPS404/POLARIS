# Skill: rf-telecom

## Purpose

LoRa/MQTT/LTE communications design.

## When to invoke

configs/communications, hardware/antenna, adapters/communications.

## Inputs

Band, protocol, country regulation note.

## Workflow

1. Mark DESIGNED. 2. Do not claim homologation. 3. MQTT is device telemetry; NATS is internal bus.

## Outputs

YAML stub or doc note.

## Validation

No illegal-transmitter instructions.

## Forbidden shortcuts

Hardcoding TX power as certified.

## Relevant paths

configs/communications/, adapters/communications/, docs/telecom/
