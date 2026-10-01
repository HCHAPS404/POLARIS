# Skill: security

## Purpose

Secrets, HITL alerting ethics, disclosure.

## When to invoke

SECURITY.md, schemas/alerts, adapters/alerts.

## Inputs

Threat or disclosure item.

## Workflow

1. Scan for secrets. 2. Require disclaimer fields on alert schemas. 3. Follow SECURITY.md.

## Outputs

Policy or schema tweak.

## Validation

gitleaks/detect-secrets or workflow equivalent clean.

## Forbidden shortcuts

Public full exploit writeups against alerting channels.

## Relevant paths

SECURITY.md, schemas/alerts/, .github/workflows/security.yml
