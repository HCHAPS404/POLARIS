"""RF link-budget FSPL (SIMULATED)."""

from __future__ import annotations

import pytest

from simulation.python.rf.link_budget import free_space_path_loss_db, received_power_dbm


def test_fspl_known_distance_868mhz() -> None:
    # 1 km @ 868 MHz — Friis log form (MHz, metres): 20log10(d)+20log10(f)-27.55
    fspl = free_space_path_loss_db(distance_m=1000.0, frequency_mhz=868.0)
    assert fspl == pytest.approx(91.22, abs=0.05)


def test_fspl_increases_with_distance() -> None:
    near = free_space_path_loss_db(distance_m=100.0, frequency_mhz=868.0)
    far = free_space_path_loss_db(distance_m=2000.0, frequency_mhz=868.0)
    assert far > near


def test_fspl_zero_distance_is_degenerate() -> None:
    assert free_space_path_loss_db(distance_m=0.0, frequency_mhz=868.0) == 0.0


def test_received_power_matches_tx_minus_fspl() -> None:
    d_m = 500.0
    f_mhz = 868.0
    tx = 14.0
    fspl = free_space_path_loss_db(distance_m=d_m, frequency_mhz=f_mhz)
    rx = received_power_dbm(tx_power_dbm=tx, distance_m=d_m, frequency_mhz=f_mhz)
    assert rx == pytest.approx(tx - fspl, abs=1e-9)


def test_invalid_frequency_raises() -> None:
    with pytest.raises(ValueError, match="frequency"):
        free_space_path_loss_db(distance_m=10.0, frequency_mhz=0.0)
