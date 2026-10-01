# Skill: pcb-cad

## Purpose

Schematics, PCB, enclosure CAD.

## When to invoke

hardware/schematics, pcb, cad, enclosure, bom.

## Inputs

Board name, revision.

## Workflow

1. Keep PLACEHOLDER in P0. 2. No proprietary datasheet dumps. 3. Revision in filename when real files appear.

## Outputs

Path to CAD or explicit skip.

## Validation

No fabricated-board claim.

## Forbidden shortcuts

Generating fake Gerbers and calling them manufactured.

## Relevant paths

hardware/
