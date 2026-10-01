"""Unit tests for landslide PHI baseline."""

from __future__ import annotations

from hazards.landslide.phi import FORMULA_VERSION, compute_phi, phi_components


def test_phi_components_max_merge() -> None:
    value, susceptibility, rain_norm, _ = phi_components(
        slope_deg=32.0,
        soil_moisture=0.62,
        rainfall_mm=48.0,
    )
    assert susceptibility > 0.5
    assert rain_norm > 0.5
    assert value == max(susceptibility, rain_norm)


def test_compute_phi_record() -> None:
    record = compute_phi(
        slope_deg=18.0,
        soil_moisture=0.48,
        rainfall_mm=22.0,
        phi_mode="DETECTION",
        spatial_unit_id="co-slope-demo-lower",
        source_id="test",
        observed_at="2026-10-01T13:00:00Z",
        computed_at="2026-10-01T14:00:00Z",
        quality_flag="qc_pass",
        data_class="SIMULATED",
        run_id="run-test",
    )
    assert record.formula_version == FORMULA_VERSION
    assert record.hazard_id == "landslide"
    assert record.inputs["exposure_used"] is False
