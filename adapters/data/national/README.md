# adapters/data/national

**Evidence:** IMPLEMENTED

Shared **catalog ingest** factory (`catalog_ingest.py`) plus country YAML under `configs/data/catalog/`. No API keys in git.

- Static metadata: country profile + catalog YAML (`SIMULATED` class on ingest envelope when no live HTTP source).
- Live metadata: keyless public JSON endpoints where configured (`LIVE_INTEGRATED`, stale on failure).
- Precipitation nowcast proxy: delegated to `adapters.data.global_feeds.open_meteo_precip` per site binding in catalog.

Not national pilots. Not official alert fan-out.
