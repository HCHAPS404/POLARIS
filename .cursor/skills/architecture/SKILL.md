# Skill: architecture

## Purpose

Enforce modular monolith, hexagonal ports, bootstrap order, ADRs.

## When to invoke

Changing tree, layering, ADRs, or platform ports.

## Inputs

README_ARCHITECTURE.md, proposed change, current evidence states.

## Workflow

1. Diff against canonical tree. 2. Check bootstrap order. 3. File or update ADR if binding. 4. Update evidence headers.

## Outputs

Architecture note + ADR path or explicit 'no ADR needed'.

## Validation

Tree still matches README_ARCHITECTURE; no packages/sim revival.

## Forbidden shortcuts

Inventing microservices or a second engine tree.

## Relevant paths

README_ARCHITECTURE.md, docs/adr/, platform/ports/
