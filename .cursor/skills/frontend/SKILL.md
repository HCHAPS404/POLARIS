# Skill: frontend

## Purpose

Horizon / Vector / Forge web delivery.

## When to invoke

apps/horizon-web, vector-console, forge-studio.

## Inputs

Product surface name, user, HITL copy.

## Workflow

1. Check if a real UI exists (`index.html` or `package.json`). 2. Consume API contracts only. 3. Horizon V1 is the static MapLibre page.

## Outputs

UI slice or explicit skip.

## Validation

No fake IMPLEMENTED dashboard.

## Forbidden shortcuts

Generating a full Next app unasked.

## Relevant paths

apps/horizon-web/, apps/vector-console/, apps/forge-studio/
