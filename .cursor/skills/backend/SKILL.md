# Skill: backend

## Purpose

FastAPI platform API and application layer.

## When to invoke

platform/api, health, future REST/WebSocket.

## Inputs

OpenAPI/schema, desired route, evidence bar.

## Workflow

1. Confirm schema exists. 2. Implement against ports. 3. Test with TestClient. 4. Do not add domain physics in the router.

## Outputs

Route + pytest.

## Validation

ruff + pytest green; /health remains.

## Forbidden shortcuts

PHI computation inside a router in P0; platform/__init__.py.

## Relevant paths

platform/api/, schemas/, tests/unit/
