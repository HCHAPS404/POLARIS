"""Golden vectors for GCI v0.1.0."""

from __future__ import annotations

import pytest

from domains.quality.gci import FORMULA_VERSION, QC_SCORE, completeness, gci_value


def test_completeness_full() -> None:
    present = ("rainfall_mm", "observed_at", "source_id", "data_class")
    assert completeness(present) == 1.0


def test_completeness_three_of_four() -> None:
    present = ("rainfall_mm", "observed_at", "source_id")
    assert completeness(present) == pytest.approx(0.75)


def test_gci_qc_pass_simulated_complete() -> None:
    # 1.00 * 1.00 * 0.65
    value = gci_value(
        quality_flag="qc_pass",
        data_class="SIMULATED",
        present=("rainfall_mm", "observed_at", "source_id", "data_class"),
    )
    assert value == pytest.approx(0.65)


def test_gci_raw_simulated_complete() -> None:
    # 0.70 * 1.00 * 0.65
    value = gci_value(
        quality_flag="raw",
        data_class="SIMULATED",
        present=("rainfall_mm", "observed_at", "source_id", "data_class"),
    )
    assert value == pytest.approx(0.455)


def test_gci_qc_fail() -> None:
    # 0.05 * 1.00 * 0.65
    value = gci_value(
        quality_flag="qc_fail",
        data_class="SIMULATED",
        present=("rainfall_mm", "observed_at", "source_id", "data_class"),
    )
    assert value == pytest.approx(0.0325)


def test_gci_incomplete() -> None:
    # 1.00 * 0.75 * 0.65
    value = gci_value(
        quality_flag="qc_pass",
        data_class="SIMULATED",
        present=("rainfall_mm", "observed_at", "source_id"),
    )
    assert value == pytest.approx(0.4875)


def test_gci_refuses_live_trust_weight() -> None:
    with pytest.raises(ValueError, match="data_class"):
        gci_value(
            quality_flag="qc_pass",
            data_class="LIVE",
            present=("rainfall_mm", "observed_at", "source_id", "data_class"),
        )


def test_gci_historical_replay_raw_complete() -> None:
    # 0.70 * 1.00 * 0.70
    value = gci_value(
        quality_flag="raw",
        data_class="HISTORICAL_REPLAY",
        present=("rainfall_mm", "observed_at", "source_id", "data_class"),
    )
    assert value == pytest.approx(0.49)


def test_gci_formula_version_is_explicit() -> None:
    assert FORMULA_VERSION == "gci.v0.1.0"
    assert QC_SCORE["qc_pass"] == 1.0
