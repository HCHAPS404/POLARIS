"""Integration tests for V1 flood API (SIMULATED fixtures)."""

from __future__ import annotations

import sys
from pathlib import Path

from fastapi.testclient import TestClient

API = Path(__file__).resolve().parents[2] / "platform" / "api"
sys.path.insert(0, str(API))

from main import app  # noqa: E402

client = TestClient(app)


def test_health_still_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["maturity"] == "V1-historical-replay"


def test_assessments_chain_and_draft_only() -> None:
    response = client.get("/v1/assessments")
    assert response.status_code == 200
    body = response.json()
    assert body["data_class"] == "SIMULATED"
    assert len(body["assessments"]) == 3
    for unit in body["assessments"]:
        assert unit["phi"]["formula_version"].startswith("flood.phi.")
        assert unit["gci"]["formula_version"] == "gci.v0.1.0"
        assert unit["operational_risk"]["formula_version"].startswith("risk.operational.")
        assert unit["phi"]["inputs"]["exposure_used"] is False
        assert unit["exposure"]["evidence"] == "PLACEHOLDER"
        assert unit["alert"]["status"] == "DRAFT"
        assert unit["alert"]["official"] is False
        assert unit["alert"]["human_in_the_loop"] is True
        assert "83%" not in str(unit["operational_risk"]["value"])


def test_post_run_refuses_live() -> None:
    response = client.post(
        "/v1/assessments/run",
        json={"seed": 42, "data_class": "LIVE"},
    )
    assert response.status_code == 400


def test_observation_endpoint() -> None:
    listing = client.get("/v1/observations")
    assert listing.status_code == 200
    obs_id = listing.json()["observations"][0]["observation_id"]
    one = client.get(f"/v1/observations/{obs_id}")
    assert one.status_code == 200
    assert one.json()["data_class"] == "SIMULATED"


def test_geojson_for_horizon() -> None:
    response = client.get("/v1/map/geojson")
    assert response.status_code == 200
    body = response.json()
    assert body["type"] == "FeatureCollection"
    assert body["data_class"] == "SIMULATED"
    assert len(body["features"]) == 3


def test_horizon_page_served() -> None:
    response = client.get("/horizon/")
    assert response.status_code == 200
    assert "SIMULATED" in response.text
    assert "DRAFT" in response.text
    assert "HISTORICAL_REPLAY" in response.text
