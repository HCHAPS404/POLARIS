"""Abstract LoRa-ish packet transport (SIMULATED)."""

from __future__ import annotations

import json
from dataclasses import dataclass
from random import Random
from typing import Any

from simulation.python.iot.sensors import link_rssi_dbm


@dataclass(frozen=True)
class IoTPacket:
    node_id: str
    device_type: str
    event_time: str
    payload: dict[str, Any]
    rssi_dbm: float
    latency_ms: int


def _should_drop(rng: Random, packet_loss: float) -> bool:
    if packet_loss <= 0:
        return False
    return rng.random() < packet_loss


def transmit(
    *,
    node_id: str,
    device_type: str,
    event_time: str,
    payload: dict[str, Any],
    comm: dict[str, Any],
    rng: Random,
) -> IoTPacket | None:
    """TX side — may drop packet when packet_loss > 0."""
    if _should_drop(rng, float(comm.get("packet_loss") or 0)):
        return None
    rssi = link_rssi_dbm(
        tx_power_dbm=float(comm.get("tx_power_dbm") or 14),
        distance_m=float(comm.get("distance_m") or 1000),
        frequency_mhz=float(comm.get("frequency_mhz") or 868.0),
    )
    latency = int(comm.get("latency_ms") or 100)
    return IoTPacket(
        node_id=node_id,
        device_type=device_type,
        event_time=event_time,
        payload=dict(payload),
        rssi_dbm=round(rssi, 2),
        latency_ms=latency,
    )


def packet_bytes(packet: IoTPacket) -> bytes:
    body = {
        "node_id": packet.node_id,
        "device_type": packet.device_type,
        "event_time": packet.event_time,
        "payload": packet.payload,
        "rssi_dbm": packet.rssi_dbm,
    }
    return json.dumps(body, sort_keys=True, separators=(",", ":")).encode("utf-8")
