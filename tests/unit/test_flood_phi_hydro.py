"""Golden vectors for flood PHI rainfall + hydro v0.2.0."""

from __future__ import annotations

import pytest

from hazards.flood.phi import (
    FORMULA_VERSION_RAIN_HYDRO,
    L0_M,
    L1_M,
    combine_rainfall_hydro_phi,
    compute_phi_with_hydro,
    phi_from_water_level,
)

HYDRO_VECTORS = [
    (0.0, 0.0),
    (L0_M, 0.0),
    (1.0, (1.0 - L0_M) / (L1_M - L0_M)),
    (L1_M, 1.0),
    (4.0, 1.0),
]


@pytest.mark.parametrize(("level_m", "expected"), HYDRO_VECTORS)
def test_phi_hydro_golden(level_m: float, expected: float) -> None:
    assert phi_from_water_level(level_m) == pytest.approx(expected)


def test_combine_is_max() -> None:
    assert combine_rainfall_hydro_phi(0.2, 0.7) == pytest.approx(0.7)


def test_compute_with_hydro_bumps_formula_version() -> None:
    record = compute_phi_with_hydro(
        rainfall_mm=12.0,
        water_level_m=2.0,
        phi_mode="NOWCAST",
        spatial_unit_id="u",
        source_id="iot/weather",
        observed_at="2026-10-01T11:00:00Z",
        computed_at="2026-10-01T12:00:00Z",
        quality_flag="qc_pass",
        data_class="SIMULATED",
        run_id="run",
        hydro_source_id="iot/hydro",
    )
    assert record.formula_version == FORMULA_VERSION_RAIN_HYDRO
    assert record.inputs["merge"] == "max"
    assert record.value >= record.inputs["phi_rainfall"]
