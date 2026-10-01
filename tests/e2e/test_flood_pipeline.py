"""E2E-ish: SIMULATED fixture file → orchestrator → API JSON."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "platform" / "api"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(API))
sys.path.insert(0, str(ROOT / "platform"))

from application.flood_assessment import run_flood_slice  # noqa: E402
from main import app  # noqa: E402

from adapters.storage.simulated_json import load_simulated_fixture  # noqa: E402

FIXTURE = ROOT / "data" / "synthetic" / "flood-bogota-demo.simulated.json"


def test_fixture_file_to_api_json() -> None:
    raw = json.loads(FIXTURE.read_text(encoding="utf-8"))
    assert raw["data_class"] == "SIMULATED"
    loaded = load_simulated_fixture("flood-bogota-demo")
    domain = run_flood_slice(loaded, seed=42)

    client = TestClient(app)
    api = client.get("/v1/assessments", params={"seed": 42}).json()

    assert api["run_id"] == domain.run_id
    assert api["data_class"] == "SIMULATED"
    assert len(api["assessments"]) == len(domain.units) == 3

    by_id = {row["spatial_unit_id"]: row for row in api["assessments"]}
    north = by_id["co-bogota-demo-north"]
    assert north["observation"]["value"] == 72.0
    assert north["phi"]["value"] == domain.units[0].phi.value
    assert north["alert"]["status"] == "DRAFT"
    assert north["gci"]["provenance"]["formula_version"] == "gci.v0.1.0"
    assert set(north["phi"]["provenance"].keys()) >= {
        "run_id",
        "formula_version",
        "model_version",
        "inputs",
        "source_ids",
        "observed_at",
        "computed_at",
        "quality_flags",
        "uncertainty",
        "data_class",
    }


def test_same_seed_same_payload() -> None:
    client = TestClient(app)
    a = client.get("/v1/assessments", params={"seed": 42}).json()
    b = client.post("/v1/assessments/run", json={"seed": 42}).json()
    assert a["run_id"] == b["run_id"]
    assert a["assessments"][0]["alert"]["alert_id"] == b["assessments"][0]["alert"]["alert_id"]
    assert a["assessments"][0]["phi"]["value"] == b["assessments"][0]["phi"]["value"]
