"""Operational risk = PHI × E_stub × V_stub; PHI stays independent of E/V."""

from __future__ import annotations

import pytest

from domains.exposure.stub import stub_exposure
from domains.risk.operational import FORMULA_VERSION, operational_risk_value
from domains.vulnerability.stub import stub_vulnerability
from hazards.flood.phi import phi_from_rainfall


def test_operational_risk_golden() -> None:
    # 0.5 * 0.70 * 0.55 = 0.1925 (center unit)
    assert operational_risk_value(0.5, 0.70, 0.55) == pytest.approx(0.1925)


def test_north_fixture_chain_numbers() -> None:
    phi = phi_from_rainfall(72.0)
    exposure = stub_exposure("co-bogota-demo-north").value
    vulnerability = stub_vulnerability("co-bogota-demo-north").value
    assert phi == pytest.approx(62.0 / 70.0)
    assert exposure == 0.40
    assert vulnerability == 0.50
    assert operational_risk_value(phi, exposure, vulnerability) == pytest.approx(
        (62.0 / 70.0) * 0.40 * 0.50
    )


def test_phi_unchanged_when_exposure_changes() -> None:
    rainfall = 45.0
    phi_a = phi_from_rainfall(rainfall)
    phi_b = phi_from_rainfall(rainfall)
    risk_low = operational_risk_value(phi_a, 0.1, 0.5)
    risk_high = operational_risk_value(phi_b, 0.9, 0.5)
    assert phi_a == phi_b
    assert risk_high > risk_low
    assert FORMULA_VERSION == "risk.operational.phi-ev-stub.v0.1.0"


def test_stubs_are_placeholder() -> None:
    assert stub_exposure("co-bogota-demo-center").evidence == "PLACEHOLDER"
    assert stub_vulnerability("co-bogota-demo-center").evidence == "PLACEHOLDER"
