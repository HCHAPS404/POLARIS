# Mobile offline cache policy

**Evidence:** DESIGNED (directory contract + in-memory stub)

Production mobile builds would persist under app documents:

```text
offline/
  manifest.json          # schema_version, data_class, ttl, provenance
  assessments.json       # last-good /v1/assessments body
  health.json            # last-good /health body
  alerts.json            # last-good /v1/alerts body
  map/                   # optional GeoJSON fragments (NOT IMPLEMENTED)
```

## Current implementation

- `offline_cache_stub.dart` — in-memory only for tests and demo
- No `path_provider` persistence in CI

## Badges (SIMULATED vs LIVE)

| `data_class` | UI badge | Policy |
|--------------|----------|--------|
| `SIMULATED` | SIM | Default fixtures; safe for demos |
| `HISTORICAL_REPLAY` | REPLAY | Mocoa 2017 replay; not HISTORICALLY_VALIDATED globally |
| `LIVE_INTEGRATED` | LIVE | Only when API returns it with provenance; never assumed offline |

Cached payloads **must** retain `data_class` and decision-support disclaimers. Stale cache shows an error hint — not fresh LIVE data.

## Alerts

DRAFT alerts may be cached for read-only review. **No auto-send** of operational notifications.
