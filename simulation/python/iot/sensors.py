"""Deterministic sensor error models (SIMULATED).

Per README_SIMULATION_ENGINEERING / product sensor architecture:
  true value → response with documented bias, drift, noise, quantization.

Not unseeded randomness — all draws use a seeded RNG passed from the runner.
"""

from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class SensorModelParams:
    bias: float
    drift_per_hour: float
    noise_sigma: float
    quantize_step: float
    dropout_prob: float = 0.0


RAINFALL_PARAMS = SensorModelParams(
    bias=0.35,
    drift_per_hour=0.02,
    noise_sigma=0.8,
    quantize_step=0.2,
    dropout_prob=0.0,
)

WATER_LEVEL_PARAMS = SensorModelParams(
    bias=-0.015,
    drift_per_hour=0.001,
    noise_sigma=0.012,
    quantize_step=0.005,
    dropout_prob=0.0,
)


def _quantize(value: float, step: float) -> float:
    if step <= 0:
        return value
    return round(value / step) * step


def simulate_rainfall_mm(
    *,
    true_mm: float,
    rng: Random,
    elapsed_hours: float,
    params: SensorModelParams = RAINFALL_PARAMS,
) -> tuple[float, dict[str, float]]:
    """Pluviometer accumulation model (1-hour window truth injected as true_mm)."""
    if rng.random() < params.dropout_prob:
        raise RuntimeError("simulated sensor dropout (rainfall)")
    drift = params.drift_per_hour * elapsed_hours
    noise = rng.gauss(0.0, params.noise_sigma)
    raw = true_mm + params.bias + drift + noise
    measured = _quantize(max(0.0, raw), params.quantize_step)
    meta = {
        "true_mm": true_mm,
        "bias": params.bias,
        "drift": drift,
        "noise": noise,
        "quantize_step": params.quantize_step,
    }
    return measured, meta


def simulate_water_level_m(
    *,
    true_m: float,
    rng: Random,
    elapsed_hours: float,
    params: SensorModelParams = WATER_LEVEL_PARAMS,
) -> tuple[float, dict[str, float]]:
    """Ultrasonic level — true stage with slow drift and mm-scale noise."""
    if rng.random() < params.dropout_prob:
        raise RuntimeError("simulated sensor dropout (water_level)")
    drift = params.drift_per_hour * elapsed_hours
    noise = rng.gauss(0.0, params.noise_sigma)
    raw = true_m + params.bias + drift + noise
    measured = _quantize(max(0.0, raw), params.quantize_step)
    meta = {
        "true_m": true_m,
        "bias": params.bias,
        "drift": drift,
        "noise": noise,
        "quantize_step": params.quantize_step,
    }
    return measured, meta


def fspl_db(*, distance_m: float, frequency_mhz: float) -> float:
    """Re-export FSPL from `simulation.python.rf` for IoT comm models."""
    from simulation.python.rf.link_budget import free_space_path_loss_db

    return free_space_path_loss_db(distance_m=distance_m, frequency_mhz=frequency_mhz)


def link_rssi_dbm(*, tx_power_dbm: float, distance_m: float, frequency_mhz: float) -> float:
    from simulation.python.rf.link_budget import received_power_dbm

    return received_power_dbm(
        tx_power_dbm=tx_power_dbm,
        distance_m=distance_m,
        frequency_mhz=frequency_mhz,
    )
