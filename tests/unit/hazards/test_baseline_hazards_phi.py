"""Golden vectors for baseline hazard PHI plugins."""

from __future__ import annotations

import pytest

from hazards.cyclone.phi import phi_from_cyclone
from hazards.drought.phi import phi_from_drought
from hazards.earthquake.phi import compute_phi as eq_phi
from hazards.earthquake.phi import phi_from_pga
from hazards.erosion_subsidence.phi import phi_from_erosion
from hazards.flash_flood.phi import phi_from_rainfall_burst
from hazards.heat.phi import phi_from_heat
from hazards.smoke.phi import phi_from_smoke
from hazards.tsunami.phi import phi_from_tsunami
from hazards.volcano.phi import phi_from_volcano


def test_flash_flood_burst_golden() -> None:
    assert phi_from_rainfall_burst(25.0) == 0.0
    assert phi_from_rainfall_burst(42.5) == pytest.approx(0.5)
    assert phi_from_rainfall_burst(60.0) == 1.0


def test_drought_golden() -> None:
    assert phi_from_drought(precipitation_mm_30d=120.0, soil_moisture=0.35) == 0.0
    assert phi_from_drought(precipitation_mm_30d=20.0, soil_moisture=0.12) == pytest.approx(0.8)


def test_heat_golden() -> None:
    assert phi_from_heat(temperature_c=30.0, heat_index_c=None) == 0.0
    assert phi_from_heat(temperature_c=35.0, heat_index_c=36.5) == pytest.approx(0.5)


def test_cyclone_golden() -> None:
    assert phi_from_cyclone(wind_speed_ms=17.0, pressure_hpa=None) == 0.0
    assert phi_from_cyclone(wind_speed_ms=25.0, pressure_hpa=965.0) > 0.4


def test_smoke_golden() -> None:
    assert phi_from_smoke(pm25_ugm3=35.0, visibility_m=None) == 0.0
    assert phi_from_smoke(pm25_ugm3=142.5, visibility_m=8000.0) == pytest.approx(0.5)


def test_earthquake_refuses_forecast_mode() -> None:
    with pytest.raises(ValueError, match="earthquake phi_mode"):
        eq_phi(
            pga_g=0.1,
            phi_mode="FORECAST",
            spatial_unit_id="u",
            source_id="s",
            observed_at="2026-10-01T12:00:00Z",
            computed_at="2026-10-01T12:00:00Z",
            quality_flag="qc_pass",
            data_class="SIMULATED",
            run_id="run",
        )


def test_earthquake_pga_golden() -> None:
    assert phi_from_pga(0.02) == 0.0
    assert phi_from_pga(0.16) == pytest.approx(0.5)
    assert phi_from_pga(0.30) == 1.0


def test_tsunami_untriggered_zero() -> None:
    value, _ = phi_from_tsunami(event_triggered=False, wave_height_m=2.0, distance_km=10.0)
    assert value == 0.0


def test_tsunami_triggered_wave() -> None:
    value, _ = phi_from_tsunami(event_triggered=True, wave_height_m=1.65, distance_km=None)
    assert value == pytest.approx(0.5)


def test_volcano_golden() -> None:
    assert phi_from_volcano(so2_ton_per_day=500.0, ashfall_mm_h=None) == 0.0
    assert phi_from_volcano(so2_ton_per_day=2750.0, ashfall_mm_h=2.75) == pytest.approx(0.5)


def test_erosion_golden() -> None:
    v = phi_from_erosion(soil_cohesion_proxy=0.6, slope_deg=15.0, rainfall_mm=45.0)
    assert 0.0 < v < 1.0
