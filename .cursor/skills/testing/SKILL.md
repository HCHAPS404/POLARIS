# Skill: testing

## Purpose

Pytest, C++ tests, harnesses.

## When to invoke

tests/**, harness/**

## Inputs

Behaviour to protect, evidence state.

## Workflow

1. Unit tests for what exists. 2. Do not fail CI on missing Flutter/pnpm. 3. Harness/dev must execute.

## Outputs

Tests + make targets.

## Validation

pytest collection green.

## Forbidden shortcuts

Snapshot tests of unpublished live alerts.

## Relevant paths

tests/, harness/dev/
