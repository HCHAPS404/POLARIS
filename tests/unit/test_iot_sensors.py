"""Unit tests for SIMULATED IoT sensor and comm models."""

from __future__ import annotations

from random import Random

from simulation.python.iot.comm import transmit
from simulation.python.iot.sensors import fspl_db, simulate_rainfall_mm, simulate_water_level_m


def test_rainfall_model_is_seeded_deterministic() -> None:
    a, _ = simulate_rainfall_mm(true_mm=50.0, rng=Random(42), elapsed_hours=1.0)
    b, _ = simulate_rainfall_mm(true_mm=50.0, rng=Random(42), elapsed_hours=1.0)
    assert a == b
    assert a > 0


def test_fspl_increases_with_distance() -> None:
    near = fspl_db(distance_m=100, frequency_mhz=868)
    far = fspl_db(distance_m=2000, frequency_mhz=868)
    assert far > near


def test_packet_loss_can_drop() -> None:
    comm = {
        "distance_m": 500,
        "frequency_mhz": 868,
        "tx_power_dbm": 14,
        "latency_ms": 50,
        "packet_loss": 1.0,
    }
    pkt = transmit(
        node_id="iot/weather-node-001",
        device_type="weather-node",
        event_time="2026-10-01T12:00:00Z",
        payload={"observed_property": "rainfall_mm", "value": 1.0, "unit": "mm"},
        comm=comm,
        rng=Random(1),
    )
    assert pkt is None


def test_water_level_bias_documented() -> None:
    _, meta = simulate_water_level_m(true_m=2.0, rng=Random(7), elapsed_hours=2.0)
    assert "bias" in meta
    assert meta["bias"] < 0
