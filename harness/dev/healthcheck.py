#!/usr/bin/env python3
"""Runnable P0 health check — not docs-only.

Uses FastAPI TestClient so it does not require a listening port.
"""

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
    response = client.get("/health")
    payload = response.json()
    print(json.dumps(payload, indent=2))
    if response.status_code != 200 or payload.get("status") != "ok":
        print("health check failed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
