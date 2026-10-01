# Skill: devops

## Purpose

Compose, GitHub Actions, Taskfile/Make.

## When to invoke

.github/workflows, infra, docker-compose, Makefile.

## Inputs

Job name, skip conditions.

## Workflow

1. Path-filter web/mobile. 2. No secrets. 3. Compose labelled non-production.

## Outputs

Workflow or compose change.

## Validation

CI Python green; skip jobs documented.

## Forbidden shortcuts

Deploying to production from P0.

## Relevant paths

.github/workflows/, infra/, docker-compose.yml
