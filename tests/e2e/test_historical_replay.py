"""HISTORICAL_REPLAY backtest: same V1 formulas, honest metrics, no LIVE."""

from __future__ import annotations

import json
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "platform"))
sys.path.insert(0, str(ROOT / "platform" / "api"))

from application.flood_assessment import run_flood_slice  # noqa: E402
from main import app  # noqa: E402

from adapters.storage.simulated_json import load_fixture  # noqa: E402
from domains.backtesting.metrics import score_units  # noqa: E402
from harness.backtesting.replay import run_backtest  # noqa: E402
from hazards.flood.phi import FORMULA_VERSION, phi_from_rainfall  # noqa: E402
from simulation.python.run import run  # noqa: E402

SCENARIO = ROOT / "simulation" / "scenarios" / "flood-mocoa-2017-replay.yaml"


def test_replay_seed_is_deterministic() -> None:
    a = run(SCENARIO, 42)
    b = run(SCENARIO, 42)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["data_class"] == "HISTORICAL_REPLAY"
    assert a["scenario_seed"] == 42


def test_replay_uses_same_phi_formula_as_v1() -> None:
    payload = run(SCENARIO, 42)
    by_id = {row["spatial_unit_id"]: row for row in payload["assessments"]}
    burst = by_id["co-mocoa-2017-acueducto-3h"]
    daily = by_id["co-mocoa-2017-acueducto-24h"]
    era5 = by_id["co-mocoa-2017-era5-1h"]
    assert burst["phi"]["formula_version"] == FORMULA_VERSION
    assert burst["phi"]["value"] == phi_from_rainfall(106.0) == 1.0
    assert daily["phi"]["value"] == phi_from_rainfall(129.3) == 1.0
    assert era5["phi"]["value"] == phi_from_rainfall(1.3) == 0.0
    assert burst["phi"]["inputs"]["accumulation"] == "3h"
    assert daily["phi"]["inputs"]["accumulation"] == "24h"
    assert era5["phi"]["inputs"]["accumulation"] == "1h"
    assert burst["gci"]["formula_version"] == "gci.v0.1.0"
    assert burst["operational_risk"]["formula_version"].startswith("risk.operational.")
    assert burst["alert"]["status"] == "DRAFT"


def test_event_time_is_not_ingest_time() -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d")
    payload = run(SCENARIO, 42)
    assert payload["as_of"].startswith("2017-04-01")
    assert now not in payload["as_of"]
    for unit in payload["assessments"]:
        observed = unit["observation"]["observed_at"]
        event_time = unit["observation"]["provenance"]["event_time"]
        assert observed == event_time
        assert observed.startswith("2017-")
        assert unit["phi"]["computed_at"] == payload["as_of"]
        assert unit["phi"]["observed_at"] == observed


def test_fixture_to_metrics_pipeline() -> None:
    fixture = load_fixture("flood-mocoa-2017-replay")
    domain = run_flood_slice(fixture, seed=42)
    report = run_backtest(SCENARIO, 42)
    assert report["evidence"] == "EXPERIMENTAL"
    assert report["evidence"] != "HISTORICALLY_VALIDATED"
    assert report["run_id"] == domain.run_id
    assert report["counts"]["hits"] == 2
    assert report["counts"]["misses"] == 1
    assert report["counts"]["false_alarms"] == 0
    assert report["far"] is None
    assert report["pod"] == pytest.approx(2 / 3)
    assert report["brier"] is None
    assert report["data_class"] == "HISTORICAL_REPLAY"
    client = TestClient(app)
    api = client.get("/v1/backtests/flood-mocoa-2017-replay", params={"seed": 42})
    assert api.status_code == 200
    body = api.json()
    assert body["counts"] == report["counts"]
    assert body["pod"] == report["pod"]


def test_backtest_refuses_historically_validated_flag() -> None:
    with pytest.raises(ValueError, match="HISTORICALLY_VALIDATED"):
        score_units(
            [
                {
                    "spatial_unit_id": "x",
                    "phi": 1.0,
                    "rainfall_mm": 80,
                    "observed_at": "2017-04-01T06:00:00Z",
                    "ground_truth_flooded": True,
                }
            ],
            scenario_id="x",
            seed=42,
            formula_version_phi=FORMULA_VERSION,
            limitations=(),
            historically_validated=True,
        )


def test_api_replay_fixture_and_refuses_live() -> None:
    client = TestClient(app)
    response = client.get(
        "/v1/assessments",
        params={"fixture_id": "flood-mocoa-2017-replay", "seed": 42},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["data_class"] == "HISTORICAL_REPLAY"
    live = client.post(
        "/v1/assessments/run",
        json={"seed": 42, "fixture_id": "flood-mocoa-2017-replay", "data_class": "LIVE"},
    )
    assert live.status_code == 400
    geo = client.get(
        "/v1/map/geojson",
        params={"fixture_id": "flood-mocoa-2017-replay"},
    )
    assert geo.status_code == 200
    assert geo.json()["data_class"] == "HISTORICAL_REPLAY"
    horizon = client.get("/horizon/")
    assert horizon.status_code == 200
    assert "HISTORICAL_REPLAY" in horizon.text
