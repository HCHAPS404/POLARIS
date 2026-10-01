# Bugbot / automated review

**Evidence:** IMPLEMENTED (policy). No third-party bot is wired in P0 beyond GitHub Actions.

## What automated review should flag

- Evidence mismatch (README says IMPLEMENTED, no test)
- Secrets, tokens, `.env`, private keys
- Scope creep vs `MASTER_CURSOR_PROMPT.md` (P1–P6 work in a P0 PR)
- Alert payloads without disclaimer or provenance fields
- New top-level trees that contradict `README_ARCHITECTURE.md` (`packages/`, `sim/`)
- Flutter/pnpm jobs failing because apps are README-only (should skip, not fail `main`)

## What it should not flag as errors

- Empty domain modules marked PLACEHOLDER
- Country YAML stubs labelled INTEGRATION (not PILOT)
- Compose files documented as DESIGNED / not production
