# Skill: hazard-model

## Purpose

Per-phenomenon plugins.

## When to invoke

hazards/*, domains/hazards, compound.

## Inputs

Hazard id, evidence papers (optional).

## Workflow

1. Run scaffold generator. 2. Fill interface only. 3. No PHI math in P0.

## Outputs

Plugin files + test.

## Validation

pytest on placeholder; provenance.json present.

## Forbidden shortcuts

Copying uncited 'AI flood models' as IMPLEMENTED.

## Relevant paths

hazards/, generators/hazard/, configs/hazards/
