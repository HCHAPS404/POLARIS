"""Unit tests for GET /health (IMPLEMENTED)."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

API = Path(__file__).resolve().parents[2] / "platform" / "api"
sys.path.insert(0, str(API))

from main import app  # noqa: E402


def test_health_ok() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "polaris"
    assert body["evidence"] == "IMPLEMENTED"
