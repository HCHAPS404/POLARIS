#!/usr/bin/env python3
"""API slice for IEEE demo — uses TestClient (no listening server)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "platform" / "api"
if str(API) not in sys.path:
    sys.path.insert(0, str(API))

from fastapi.testclient import TestClient  # noqa: E402
from main import app  # noqa: E402


def main() -> int:
    client = TestClient(app)
    health = client.get("/health")
    assessments = client.get("/v1/assessments")
    map_geo = client.get("/v1/map/geojson")
    forge = client.get("/forge/")
    print("GET /health", health.status_code, json.dumps(health.json(), indent=2))
    print(
        "GET /v1/assessments",
        assessments.status_code,
        f"units={len(assessments.json().get('assessments', []))}",
    )
    print("GET /v1/map/geojson", map_geo.status_code, map_geo.json().get("type"))
    print("GET /forge/", forge.status_code, "bytes=", len(forge.text))
    ok = all(
        r.status_code == 200
        for r in (health, assessments, map_geo, forge)
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
