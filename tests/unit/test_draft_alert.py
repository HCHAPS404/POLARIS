"""DRAFT-only alerts. Never OFFICIAL."""

from __future__ import annotations

from domains.alerting.draft import (
    FORMULA_VERSION,
    DraftAlert,
    build_draft_alert,
    draft_level,
)
from domains.common import ALERT_STATUS_DRAFT, DISCLAIMER
from domains.exposure.stub import stub_exposure
from domains.risk.operational import compute_operational_risk
from domains.vulnerability.stub import stub_vulnerability
from hazards.flood.phi import compute_phi


def test_level_bands() -> None:
    assert draft_level(0.0) == "info"
    assert draft_level(0.09) == "info"
    assert draft_level(0.10) == "watch"
    assert draft_level(0.29) == "watch"
    assert draft_level(0.30) == "warning"
    assert draft_level(0.54) == "warning"
    assert draft_level(0.55) == "proposed"


def test_serialised_alert_is_draft_with_hitl() -> None:
    phi = compute_phi(
        rainfall_mm=45.0,
        phi_mode="NOWCAST",
        spatial_unit_id="co-bogota-demo-center",
        source_id="sim-gauge-center-001",
        observed_at="2026-10-01T11:00:00Z",
        computed_at="2026-10-01T12:00:00Z",
        quality_flag="qc_pass",
        data_class="SIMULATED",
        run_id="run-test",
    )
    risk = compute_operational_risk(
        phi=phi,
        exposure=stub_exposure("co-bogota-demo-center"),
        vulnerability=stub_vulnerability("co-bogota-demo-center"),
        computed_at="2026-10-01T12:00:00Z",
    )
    alert = build_draft_alert(risk=risk, phi=phi)
    payload = alert.to_dict()
    assert payload["status"] == ALERT_STATUS_DRAFT
    assert payload["official"] is False
    assert payload["cap"] is None
    assert payload["human_in_the_loop"] is True
    assert payload["formula_version"] == FORMULA_VERSION
    assert "official warning" in payload["disclaimer"].lower()
    assert payload["status"] != "OFFICIAL"
    assert DISCLAIMER in payload["disclaimer"]


def test_refuse_non_draft_serialisation() -> None:
    alert = DraftAlert(
        alert_id="x",
        status="OFFICIAL",
        level="warning",
        hazard_id="flood",
        spatial_unit_id="u",
        human_in_the_loop=True,
        formula_version=FORMULA_VERSION,
        model_version=FORMULA_VERSION,
        evidence="IMPLEMENTED",
        disclaimer=DISCLAIMER,
        provenance={},
        operational_risk_value=0.2,
    )
    try:
        alert.to_dict()
        raise AssertionError("OFFICIAL alerts must not serialise")
    except RuntimeError as exc:
        assert "non-DRAFT" in str(exc)
