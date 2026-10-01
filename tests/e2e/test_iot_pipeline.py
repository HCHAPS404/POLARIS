"""E2E: SIMULATED IoT → gateway → V1 flood pipeline."""

from __future__ import annotations

from pathlib import Path

from simulation.python.iot.pipeline import golden_digest, run_iot_scenario_path

ROOT = Path(__file__).resolve().parents[2]

# Captured from seed=42, iot-bogota-demo.yaml — update only when models change intentionally.
GOLDEN_IOT_DIGEST = "54c92aa1dde75c91a893abd9da19b436"


def test_iot_pipeline_deterministic_golden() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "iot-bogota-demo.yaml"
    payload = run_iot_scenario_path(scenario, seed=42)
    assert payload["data_class"] == "SIMULATED"
    assert payload["observations"][0]["source_id"].startswith("iot/")
    assert all(o["data_class"] == "SIMULATED" for o in payload["observations"])
    digest = golden_digest(payload)
    assert digest == GOLDEN_IOT_DIGEST


def test_store_and_forward_preserves_event_time() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "iot-bogota-backhaul-down.yaml"
    payload = run_iot_scenario_path(scenario, seed=42)
    assert payload["gateway"]["backhaul_down"] is True
    assert payload["gateway"]["held_packets"] == 2
    for rec in payload["gateway_records"]:
        assert rec["event_time"] == "2026-10-01T12:00:00Z"
        assert rec["ingest_time"] == "2026-10-01T12:15:00Z"
        assert rec["store_and_forward"] is True


def test_flood_slice_draft_only_from_iot() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "iot-bogota-demo.yaml"
    payload = run_iot_scenario_path(scenario, seed=42)
    assessments = payload["flood_slice"]["assessments"]
    assert len(assessments) == 1
    assert assessments[0]["alert"]["status"] == "DRAFT"
    assert assessments[0]["phi"]["formula_version"] == "flood.phi.rainfall-hydro.v0.2.0"
    assert "water_level_m" in assessments[0]["phi"]["inputs"]
