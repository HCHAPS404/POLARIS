"""Minimal link-budget primitives (SIMULATED).

Free-space path loss (FSPL) in dB — Friis-style log-distance form for distance in
metres and frequency in MHz:

    FSPL(dB) = 20 log10(d) + 20 log10(f) - 27.55

Evidence: IMPLEMENTED (unit-tested). Not terrain, foliage, or multipath.
"""

from __future__ import annotations

import math


def free_space_path_loss_db(*, distance_m: float, frequency_mhz: float) -> float:
    """Return FSPL in dB; 0 dB when distance <= 0 (degenerate link)."""
    if distance_m <= 0:
        return 0.0
    if frequency_mhz <= 0:
        raise ValueError("frequency_mhz must be positive")
    return 20.0 * math.log10(distance_m) + 20.0 * math.log10(frequency_mhz) - 27.55


def log_distance_path_loss_db(
    *,
    distance_m: float,
    frequency_mhz: float,
    path_loss_exponent: float = 2.7,
    reference_distance_m: float = 1.0,
) -> float:
    """Log-distance path loss relative to FSPL at reference_distance_m.

    PL(d) = FSPL(d0) + 10 * n * log10(d / d0)  for d > d0; at d <= d0 uses FSPL(d).
    """
    if distance_m <= 0:
        return 0.0
    if frequency_mhz <= 0:
        raise ValueError("frequency_mhz must be positive")
    if reference_distance_m <= 0:
        raise ValueError("reference_distance_m must be positive")
    if path_loss_exponent < 2.0:
        raise ValueError("path_loss_exponent must be >= 2.0 for outdoor models")
    d0 = reference_distance_m
    fspl_d0 = free_space_path_loss_db(distance_m=d0, frequency_mhz=frequency_mhz)
    if distance_m <= d0:
        return free_space_path_loss_db(distance_m=distance_m, frequency_mhz=frequency_mhz)
    return fspl_d0 + 10.0 * path_loss_exponent * math.log10(distance_m / d0)


def received_power_dbm(
    *,
    tx_power_dbm: float,
    distance_m: float,
    frequency_mhz: float,
    cable_and_connector_loss_db: float = 0.0,
    antenna_gain_dbi: float = 0.0,
) -> float:
    """Simple received power: Tx + Gtx + Grx - FSPL - fixed losses (SIMULATED)."""
    fspl = free_space_path_loss_db(distance_m=distance_m, frequency_mhz=frequency_mhz)
    return tx_power_dbm + antenna_gain_dbi - fspl - cable_and_connector_loss_db
