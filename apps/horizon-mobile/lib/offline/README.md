# Mobile offline package structure

**Evidence:** DESIGNED (directory contract; in-memory stub in `lib/services/offline_cache_stub.dart`)

Production mobile builds would persist under app documents:

```text
offline/
  manifest.json          # schema_version, data_class, ttl, provenance
  assessments.json       # last-good /v1/assessments body
  health.json            # last-good /health body
  map/                   # optional vector tiles or geojson fragments (NOT IMPLEMENTED)
```

## Current implementation

- `OfflineCacheStub` — in-memory only for tests and demo
- No `path_provider` persistence in CI

## Policy

All cached payloads must retain `data_class` and decision-support disclaimers. No auto-send of alerts.
