"""RF log-distance and LoRa airtime helpers."""

from __future__ import annotations

from simulation.python.rf.link_budget import free_space_path_loss_db, log_distance_path_loss_db
from simulation.python.rf.lora_airtime import lora_payload_airtime_ms


def test_log_distance_exceeds_fspl_at_km() -> None:
    fspl = free_space_path_loss_db(distance_m=2000.0, frequency_mhz=868.0)
    logd = log_distance_path_loss_db(
        distance_m=2000.0, frequency_mhz=868.0, path_loss_exponent=3.2
    )
    assert logd > fspl


def test_lora_airtime_increases_with_sf() -> None:
    low = lora_payload_airtime_ms(payload_bytes=20, spreading_factor=7)
    high = lora_payload_airtime_ms(payload_bytes=20, spreading_factor=12)
    assert high > low
