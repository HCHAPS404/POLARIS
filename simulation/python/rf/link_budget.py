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
