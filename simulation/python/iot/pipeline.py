"""Virtual weather + hydro nodes → comm → gateway → V1 flood assessment."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from random import Random
from typing import Any
from uuid import NAMESPACE_URL, uuid5

import yaml

from simulation.python.iot.catalog import resolve_device_catalog
from simulation.python.iot.comm import transmit
from simulation.python.iot.gateway import GatewaySim
from simulation.python.iot.sensors import simulate_rainfall_mm, simulate_water_level_m

ROOT = Path(__file__).resolve().parents[3]
PLATFORM = ROOT / "platform"
for path in (str(ROOT), str(PLATFORM)):
    if path not in sys.path:
        sys.path.insert(0, path)

from application.flood_assessment import run_flood_slice, run_id_for  # noqa: E402
from application.persistence import persist_flood_slice  # noqa: E402

from domains.common import DATA_CLASS_SIMULATED, DISCLAIMER  # noqa: E402

ALLOWED_FAULT_INJECTIONS = frozenset({"packet_loss", "gateway_down"})


def apply_fault_injection(scenario: dict[str, Any]) -> dict[str, Any]:
    """Apply SIMULATED fault flags (mutates scenario copy semantics via returned dict)."""
    fault = scenario.get("fault_injection")
    if fault is None:
        return scenario
    if fault not in ALLOWED_FAULT_INJECTIONS:
        raise ValueError(
            f"fault_injection must be one of {sorted(ALLOWED_FAULT_INJECTIONS)}; got {fault!r}"
        )
    updated = dict(scenario)
    if fault == "gateway_down":
        updated["backhaul_down"] = True
    elif fault == "packet_loss":
        comm = dict(updated.get("communication") or {})
        comm["packet_loss"] = float(comm.get("packet_loss") or 0.5)
        updated["communication"] = comm
    updated["fault_injection"] = fault
    return updated


def load_scenario(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("scenario must be a mapping")
    if payload.get("data_class") != DATA_CLASS_SIMULATED:
        raise ValueError("IoT scenario must be data_class=SIMULATED")
    return apply_fault_injection(payload)


def _observation_id(seed: int, node_id: str, prop: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"polaris:iot:{seed}:{node_id}:{prop}"))


def gateway_records_to_observations(
    scenario: dict[str, Any],
    records: list,
    *,
    seed: int,
    devices: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    site_id = str(scenario["site_id"])
    country = str(scenario["country_iso"])
    spatial = str(scenario["spatial_unit_id"])
    phi_mode = str(scenario.get("phi_mode") or "NOWCAST")
    geometry = scenario.get("geometry") or {"type": "Point", "coordinates": [0.0, 0.0]}
    cal_weather = devices["weather"].get("calibration_version", "cal.weather.v0.1.0")
    cal_hydro = devices["hydro"].get("calibration_version", "cal.hydro.v0.1.0")

    observations: list[dict[str, Any]] = []
    for rec in records:
        payload = rec.payload
        prop = str(payload.get("observed_property"))
        if prop == "rainfall_mm":
            source_id = "iot/weather-node-001"
            calibration = cal_weather
        elif prop == "water_level_m":
            source_id = "iot/hydro-node-001"
            calibration = cal_hydro
        else:
            continue
        observations.append(
            {
                "observation_id": _observation_id(seed, rec.node_id, prop),
                "observed_at": rec.event_time,
                "observed_property": prop,
                "value": float(payload["value"]),
                "unit": payload["unit"],
                "quality_flag": "qc_pass",
                "source_id": source_id,
                "source": "polaris.simulation.iot",
                "data_class": DATA_CLASS_SIMULATED,
                "spatial_unit_id": spatial,
                "site_id": site_id,
                "country_iso": country,
                "phi_mode": phi_mode if prop == "rainfall_mm" else "DETECTION",
                "geometry": geometry,
                "provenance": {
                    "generator": "simulation.python.iot",
                    "event_time": rec.event_time,
                    "ingest_time": rec.ingest_time,
                    "gateway_id": "iot/gateway-pi5-001",
                    "node_id": rec.node_id,
                    "rssi_dbm": rec.rssi_dbm,
                    "store_and_forward": rec.store_and_forward,
                    "calibration_version": calibration,
                    "sensor_model": payload.get("sensor_model", {}),
                },
            }
        )
    return observations


def run_iot_scenario(scenario: dict[str, Any], *, seed: int = 42) -> dict[str, Any]:
    devices = resolve_device_catalog(scenario)
    rng = Random(seed)
    truth = scenario.get("truth") or {}
    event_time = str(scenario["as_of"])
    comm = scenario.get("communication") or {}
    elapsed_hours = 1.0

    rain_mm, rain_model = simulate_rainfall_mm(
        true_mm=float(truth.get("rainfall_mm", 0)),
        rng=rng,
        elapsed_hours=elapsed_hours,
    )
    level_m, level_model = simulate_water_level_m(
        true_m=float(truth.get("water_level_m", 0)),
        rng=rng,
        elapsed_hours=elapsed_hours,
    )

    weather_pkt = transmit(
        node_id="iot/weather-node-001",
        device_type="weather-node",
        event_time=event_time,
        payload={
            "observed_property": "rainfall_mm",
            "value": rain_mm,
            "unit": "mm",
            "sensor_model": rain_model,
            "calibration_version": devices["weather"].get("calibration_version"),
        },
        comm=comm,
        rng=rng,
    )
    hydro_pkt = transmit(
        node_id="iot/hydro-node-001",
        device_type="hydro-node",
        event_time=event_time,
        payload={
            "observed_property": "water_level_m",
            "value": level_m,
            "unit": "m",
            "sensor_model": level_model,
            "calibration_version": devices["hydro"].get("calibration_version"),
        },
        comm=comm,
        rng=rng,
    )

    gw = GatewaySim()
    for pkt in (weather_pkt, hydro_pkt):
        if pkt is not None:
            gw.receive(pkt)

    backhaul_down = bool(scenario.get("backhaul_down"))
    gateway_meta: dict[str, Any] = {"backhaul_down": backhaul_down}
    if scenario.get("fault_injection"):
        gateway_meta["fault_injection"] = str(scenario["fault_injection"])
    if backhaul_down:
        held = gw.hold_due_to_backhaul()
        gateway_meta["held_packets"] = held
        recovery_time = event_time.replace("12:00:00", "12:15:00")
        records = gw.flush_store(ingest_time=recovery_time)
        gateway_meta["recovery_ingest_time"] = recovery_time
    else:
        records = gw.forward_immediate(ingest_time=event_time)

    observations = gateway_records_to_observations(scenario, records, seed=seed, devices=devices)
    fixture_id = str(scenario.get("scenario_id") or "iot-bogota-demo")
    fixture = {
        "fixture_id": fixture_id,
        "data_class": DATA_CLASS_SIMULATED,
        "hazard_id": scenario.get("hazard_id", "flood"),
        "site_id": scenario["site_id"],
        "country_iso": scenario["country_iso"],
        "as_of": event_time,
        "disclaimer": DISCLAIMER,
        "observations": observations,
    }

    slice_result = run_flood_slice(fixture, seed=seed)
    run_id = run_id_for(fixture_id, seed)
    storage = persist_flood_slice(
        run_id=run_id,
        fixture_id=fixture_id,
        observations=observations,
        snapshot=slice_result.to_dict(),
    )

    return {
        "scenario_id": fixture_id,
        "seed": seed,
        "run_id": run_id,
        "data_class": DATA_CLASS_SIMULATED,
        "disclaimer": DISCLAIMER,
        "evidence": {
            "device_catalog": "IMPLEMENTED (SIMULATED)",
            "sensor_models": "IMPLEMENTED (SIMULATED)",
            "comm_model": "IMPLEMENTED (SIMULATED)",
            "gateway_sim": "IMPLEMENTED (SIMULATED)",
            "firmware_stubs": "PLACEHOLDER",
            "live_iot": "NOT_IMPLEMENTED",
        },
        "gateway": gateway_meta,
        "packets_tx": sum(1 for p in (weather_pkt, hydro_pkt) if p is not None),
        "gateway_records": [
            {
                "event_time": r.event_time,
                "ingest_time": r.ingest_time,
                "node_id": r.node_id,
                "store_and_forward": r.store_and_forward,
            }
            for r in records
        ],
        "observations": observations,
        "flood_slice": slice_result.to_dict(),
        "storage": storage,
    }


def run_iot_scenario_path(path: Path, *, seed: int = 42) -> dict[str, Any]:
    return run_iot_scenario(load_scenario(path), seed=seed)


def golden_digest(payload: dict[str, Any]) -> str:
    """Stable hash for pytest — excludes run_id timing noise."""
    slim = {
        "scenario_id": payload["scenario_id"],
        "seed": payload["seed"],
        "observations": payload["observations"],
        "assessments": payload["flood_slice"]["assessments"],
        "gateway_records": payload["gateway_records"],
    }
    return uuid5(NAMESPACE_URL, json.dumps(slim, sort_keys=True)).hex
