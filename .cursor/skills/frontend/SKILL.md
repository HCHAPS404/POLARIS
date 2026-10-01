# Skill: frontend

## Purpose

Horizon / Vector / Forge web delivery.

## When to invoke

apps/horizon-web, vector-console, forge-studio.

## Inputs

Product surface name, user, HITL copy.

## Workflow

1. Check if package.json exists. 2. If not, stop (P0 README-only). 3. If implementing later, consume API contracts only.

## Outputs

UI slice or explicit skip.

## Validation

No fake IMPLEMENTED dashboard.

## Forbidden shortcuts

Generating a full Next app unasked.

## Relevant paths

apps/horizon-web/, apps/vector-console/, apps/forge-studio/
