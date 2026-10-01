# Security policy

**Evidence:** IMPLEMENTED (disclosure process). Runtime threat model is DESIGNED (`docs/security/`).

## Supported versions

Only `main` and the latest tag (when one exists) receive security fixes.

## Reporting

Email **helmut.chs@gmail.com** with:

- Description and impact
- Reproduction (no public 0-day dumps of operational alert channels)
- Whether personal or infrastructure data is involved

Do not file public GitHub issues for credentials or exploitable alerting flaws.

## Hard rules in this repo

- No secrets in git. Use `.env.example` with dummy values only.
- POLARIS is decision-support: do not add unauthenticated endpoints that publish HCI/alerts until auth exists (P4+).
- IoT payloads must eventually carry device identity; P0 has no live IoT.
