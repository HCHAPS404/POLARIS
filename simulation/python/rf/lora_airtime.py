"""LoRa airtime helper (SIMULATED, Semtech-style approximation).

Evidence: IMPLEMENTED for planning estimates. Not a bit-exact modem model.
"""

from __future__ import annotations

import math


def lora_symbol_time_s(*, bandwidth_hz: float, spreading_factor: int) -> float:
    if bandwidth_hz <= 0:
        raise ValueError("bandwidth_hz must be positive")
    if not 7 <= spreading_factor <= 12:
        raise ValueError("spreading_factor must be in [7, 12]")
    return (2**spreading_factor) / bandwidth_hz


def lora_payload_airtime_ms(
    *,
    payload_bytes: int,
    spreading_factor: int,
    bandwidth_hz: float = 125_000,
    coding_rate: str = "4/5",
    preamble_symbols: int = 8,
    header_explicit: bool = True,
    low_data_rate_optimize: bool = False,
) -> float:
    """Return estimated over-the-air time in milliseconds."""
    if payload_bytes < 0:
        raise ValueError("payload_bytes must be >= 0")
    cr_den = {"4/5": 5, "4/6": 6, "4/7": 7, "4/8": 8}.get(coding_rate)
    if cr_den is None:
        raise ValueError(f"unsupported coding_rate {coding_rate!r}")
    t_sym = lora_symbol_time_s(bandwidth_hz=bandwidth_hz, spreading_factor=spreading_factor)
    de = 1 if (low_data_rate_optimize and spreading_factor >= 11) else 0
    h = 0 if header_explicit else 1
    cr = cr_den - 4
    payload_symbols = 8 + max(
        math.ceil(
            (8 * payload_bytes - 4 * spreading_factor + 28 + 16 - 20 * h)
            / (4 * (spreading_factor - 2 * de))
        )
        * (cr + 4),
        0,
    )
    total_symbols = preamble_symbols + 4.25 + payload_symbols
    return total_symbols * t_sym * 1000.0
