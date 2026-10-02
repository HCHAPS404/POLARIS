#!/usr/bin/env bash
# Smoke test against local compose (or any API on :8000). Evidence: IMPLEMENTED dev harness.
set -euo pipefail

BASE="${POLARIS_SMOKE_BASE:-http://127.0.0.1:8000}"

echo "POLARIS smoke → $BASE"

health="$(curl -sf "$BASE/health")"
echo "$health" | grep -q '"status":"ok"'

curl -sf "$BASE/v1/map/geojson?fixture_id=flood-bogota-demo" | grep -q '"data_class":"SIMULATED"'

curl -sf "$BASE/v1/config/map" | grep -q '"evidence":"IMPLEMENTED"'

echo "smoke OK"
