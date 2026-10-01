"""CAP DRAFT representation tests."""

from __future__ import annotations

from domains.alerting.cap_draft import draft_alert_to_cap_json, draft_alert_to_cap_xml
from domains.alerting.draft import build_draft_alert
from domains.provenance.index_record import IndexRecord


def _risk_and_phi() -> tuple[IndexRecord, IndexRecord]:
    phi = IndexRecord(
        index_family="PHI",
        hazard_id="flood",
        spatial_unit_id="co-bogota-demo-north",
        value=0.8,
        unit="dimensionless",
        evidence="IMPLEMENTED",
        formula_version="flood.phi.test",
        model_version="test",
        inputs={"exposure_used": False},
        source_ids=("src",),
        observed_at="2026-10-01T12:00:00Z",
        computed_at="2026-10-01T12:00:00Z",
        quality_flags=("qc_pass",),
        uncertainty=0.2,
        data_class="SIMULATED",
        run_id="run-cap-test",
    )
    risk = IndexRecord(
        index_family="operational_risk",
        hazard_id="flood",
        spatial_unit_id="co-bogota-demo-north",
        value=0.22,
        unit="dimensionless",
        evidence="IMPLEMENTED",
        formula_version="risk.operational.phi-ev-site.v0.1.0",
        model_version="test",
        inputs={},
        source_ids=("src",),
        observed_at="2026-10-01T12:00:00Z",
        computed_at="2026-10-01T12:00:00Z",
        quality_flags=("qc_pass",),
        uncertainty=0.2,
        data_class="SIMULATED",
        run_id="run-cap-test",
    )
    return risk, phi


def test_cap_json_has_disclaimer_and_not_official() -> None:
    risk, phi = _risk_and_phi()
    alert = build_draft_alert(risk=risk, phi=phi)
    cap = draft_alert_to_cap_json(alert)
    assert cap["status"] == "DRAFT"
    assert cap["official"] is False
    assert "not an official" in cap["headline"].lower() or "NOT" in cap["headline"]
    assert len(cap["disclaimer"]) >= 16


def test_cap_xml_is_test_status() -> None:
    risk, phi = _risk_and_phi()
    alert = build_draft_alert(risk=risk, phi=phi)
    xml = draft_alert_to_cap_xml(alert)
    assert "DRAFT/SIMULATION" in xml
    assert "<status>Test</status>" in xml
