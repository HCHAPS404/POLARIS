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
    assert body["maturity"] == "v1.0.0-response-quest"
    assert body["storage_backend"] in ("memory", "postgis")


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
        assert unit["exposure"]["evidence"] == "EXPERIMENTAL"
        assert unit["operational_risk"]["formula_version"] == "risk.operational.phi-ev-site.v0.1.0"
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


def test_map_client_config_defaults_local_background() -> None:
    response = client.get("/v1/config/map")
    assert response.status_code == 200
    body = response.json()
    assert body["evidence"] == "IMPLEMENTED"
    assert body["tiles_enabled"] is False
    assert body["tile_url_template"] is None


def test_demo_latest_meta() -> None:
    response = client.get("/v1/meta/demo-latest")
    assert response.status_code == 200
    body = response.json()
    assert body["evidence"] in ("IMPLEMENTED", "PLACEHOLDER")
    assert "output_dir" in body


def test_iot_ingest_endpoint() -> None:
    response = client.post("/v1/ingest/iot", json={"seed": 42, "scenario_id": "iot-bogota-demo"})
    assert response.status_code == 200
    body = response.json()
    assert body["data_class"] == "SIMULATED"
    assert body["flood_slice"]["assessments"][0]["alert"]["status"] == "DRAFT"
    assert any(o["source_id"].startswith("iot/") for o in body["observations"])


def test_landslide_fixture_via_api() -> None:
    response = client.get(
        "/v1/assessments",
        params={"fixture_id": "landslide-co-slope-demo", "seed": 42},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["hazard_id"] == "landslide"
    assert len(body["assessments"]) == 2


def test_hazards_catalog() -> None:
    response = client.get("/v1/hazards")
    assert response.status_code == 200
    body = response.json()
    ids = {h["hazard_id"] for h in body["hazards"]}
    assert "earthquake" in ids
    assert "heat" in ids
    assert all(h["evidence"] == "IMPLEMENTED" for h in body["hazards"])


def test_heat_fixture_hazard_id_param() -> None:
    ok = client.get(
        "/v1/assessments",
        params={"fixture_id": "heat-co-demo", "hazard_id": "heat"},
    )
    assert ok.status_code == 200
    assert ok.json()["hazard_id"] == "heat"
    bad = client.get(
        "/v1/assessments",
        params={"fixture_id": "heat-co-demo", "hazard_id": "flood"},
    )
    assert bad.status_code == 400


def test_alerts_cap_format() -> None:
    response = client.get("/v1/alerts", params={"format": "cap"})
    assert response.status_code == 200
    body = response.json()
    cap0 = body["cap_alerts"][0]["cap"]
    assert cap0["status"] == "DRAFT"
    assert cap0["official"] is False
    assert "disclaimer" in cap0


def test_horizon_page_served() -> None:
    response = client.get("/horizon/")
    assert response.status_code == 200
    assert "SIMULATED" in response.text
    assert "DRAFT" in response.text
    assert "HISTORICAL_REPLAY" in response.text


def test_compound_chi_endpoint() -> None:
    response = client.get("/v1/compound/chi", params={"site_id": "co-bogota-demo"})
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["formula_version"].startswith("compound.chi.")
    assert body["summary"]["units_active"] >= 1
    north = next(u for u in body["units"] if u["spatial_unit_id"] == "co-bogota-demo-north")
    assert north["chi"]["index_family"] == "CHI"


def test_vector_console_served() -> None:
    response = client.get("/vector/")
    assert response.status_code == 200
    assert "Vector" in response.text
    assert "DRAFT" in response.text


def test_forge_studio_served() -> None:
    response = client.get("/forge/")
    assert response.status_code == 200
    assert "Forge" in response.text
    assert "sim-flood" in response.text
