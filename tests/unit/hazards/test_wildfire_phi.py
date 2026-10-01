"""Unit tests for wildfire PHI baseline."""

from __future__ import annotations

from hazards.wildfire.phi import FORMULA_VERSION, compute_phi, phi_components


def test_phi_components_pm_detection_can_dominate() -> None:
    value, susceptibility, detection = phi_components(
        temperature_c=28.0,
        relative_humidity=0.40,
        wind_speed_ms=6.0,
        pm25_ugm3=120.0,
    )
    assert susceptibility > 0.2
    assert detection > susceptibility
    assert value == detection


def test_phi_without_pm_uses_susceptibility_only() -> None:
    value, susceptibility, detection = phi_components(
        temperature_c=24.0,
        relative_humidity=0.50,
        wind_speed_ms=3.0,
        pm25_ugm3=None,
    )
    assert detection == 0.0
    assert value == susceptibility


def test_compute_phi_record() -> None:
    record = compute_phi(
        temperature_c=31.0,
        relative_humidity=0.30,
        wind_speed_ms=9.0,
        pm25_ugm3=70.0,
        phi_mode="NOWCAST",
        spatial_unit_id="co-bogota-demo-center",
        source_id="test",
        observed_at="2026-10-01T14:00:00Z",
        computed_at="2026-10-01T14:05:00Z",
        quality_flag="qc_pass",
        data_class="SIMULATED",
        run_id="run-test",
    )
    assert record.formula_version == FORMULA_VERSION
    assert record.hazard_id == "wildfire"
    assert record.inputs["exposure_used"] is False
