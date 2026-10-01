"""Golden vectors for flood PHI rainfall-threshold baseline v0.1.0."""

from __future__ import annotations

import pytest

from hazards.flood.phi import (
    FORMULA_VERSION,
    MODE_UNCERTAINTY,
    T0_MM,
    T1_MM,
    compute_phi,
    phi_from_rainfall,
)

# Hand-computed: PHI = 0 for R<=10; 1 for R>=80; else (R-10)/70
PHI_VECTORS = [
    (0.0, 0.0),
    (10.0, 0.0),
    (12.0, 2.0 / 70.0),
    (45.0, 35.0 / 70.0),
    (72.0, 62.0 / 70.0),
    (80.0, 1.0),
    (100.0, 1.0),
]


@pytest.mark.parametrize(("rainfall_mm", "expected"), PHI_VECTORS)
def test_phi_golden_vectors(rainfall_mm: float, expected: float) -> None:
    assert phi_from_rainfall(rainfall_mm) == pytest.approx(expected)


def test_phi_rejects_negative_rainfall() -> None:
    with pytest.raises(ValueError, match="rainfall_mm"):
        phi_from_rainfall(-0.1)


def test_phi_mode_must_be_declared() -> None:
    with pytest.raises(ValueError, match="phi_mode"):
        compute_phi(
            rainfall_mm=45.0,
            phi_mode="GUESSED",
            spatial_unit_id="u",
            source_id="s",
            observed_at="2026-10-01T11:00:00Z",
            computed_at="2026-10-01T12:00:00Z",
            quality_flag="qc_pass",
            data_class="SIMULATED",
            run_id="run",
        )


def test_phi_does_not_use_exposure_or_vulnerability() -> None:
    record = compute_phi(
        rainfall_mm=45.0,
        phi_mode="NOWCAST",
        spatial_unit_id="u",
        source_id="s",
        observed_at="2026-10-01T11:00:00Z",
        computed_at="2026-10-01T12:00:00Z",
        quality_flag="qc_pass",
        data_class="SIMULATED",
        run_id="run",
    )
    assert record.formula_version == FORMULA_VERSION
    assert record.inputs["exposure_used"] is False
    assert record.inputs["vulnerability_used"] is False
    assert record.inputs["t0_mm"] == T0_MM
    assert record.inputs["t1_mm"] == T1_MM
    assert record.uncertainty == MODE_UNCERTAINTY["NOWCAST"]
    assert record.evidence == "IMPLEMENTED"


def test_same_rainfall_same_phi_regardless_of_caller_context() -> None:
    a = phi_from_rainfall(45.0)
    b = phi_from_rainfall(45.0)
    assert a == b == pytest.approx(0.5)
