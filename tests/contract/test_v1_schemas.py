"""Contract tests: API payloads match JSON Schema envelopes."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from fastapi.testclient import TestClient
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
API = ROOT / "platform" / "api"
sys.path.insert(0, str(API))

from main import app  # noqa: E402

client = TestClient(app)


def _schema(relative: str) -> dict:
    return json.loads((ROOT / "schemas" / relative).read_text(encoding="utf-8"))


def test_observation_schema() -> None:
    validator = Draft202012Validator(_schema("observation/observation.json"))
    payload = client.get("/v1/observations").json()["observations"][0]
    validator.validate(payload)


def test_alert_schema_draft_only() -> None:
    validator = Draft202012Validator(_schema("alerts/alert.json"))
    alerts = client.get("/v1/alerts").json()["alerts"]
    assert alerts
    for alert in alerts:
        validator.validate(alert)
        assert alert["status"] == "DRAFT"


def test_index_envelope_on_phi_and_gci() -> None:
    validator = Draft202012Validator(_schema("risk/index-envelope.json"))
    unit = client.get("/v1/assessments").json()["assessments"][0]
    validator.validate(unit["phi"])
    validator.validate(unit["gci"])
    validator.validate(unit["operational_risk"])


def test_assessment_schema() -> None:
    validator = Draft202012Validator(_schema("assessment/assessment.json"))
    unit = client.get("/v1/assessments/co-bogota-demo-center").json()
    validator.validate(unit)
