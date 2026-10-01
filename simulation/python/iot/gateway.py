"""Raspberry Pi 5 logical gateway — RX buffer, event_time preservation, store-and-forward."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from simulation.python.iot.comm import IoTPacket


@dataclass(frozen=True)
class GatewayRecord:
    event_time: str
    ingest_time: str
    node_id: str
    device_type: str
    payload: dict[str, Any]
    rssi_dbm: float
    store_and_forward: bool


@dataclass
class GatewaySim:
    """BUFFER state machine stub aligned to firmware/gateway contract."""

    gateway_id: str = "iot/gateway-pi5-001"
    _rx: list[IoTPacket] = field(default_factory=list)
    _store: list[IoTPacket] = field(default_factory=list)
    _delivered: list[GatewayRecord] = field(default_factory=list)

    def receive(self, packet: IoTPacket) -> None:
        self._rx.append(packet)

    def hold_due_to_backhaul(self) -> int:
        """Persist RX into store when backhaul is down."""
        self._store.extend(self._rx)
        held = len(self._rx)
        self._rx.clear()
        return held

    def flush_store(self, *, ingest_time: str) -> list[GatewayRecord]:
        """Deliver stored packets after backhaul recovery."""
        return self._emit(self._store, ingest_time=ingest_time, store_and_forward=True)

    def forward_immediate(self, *, ingest_time: str) -> list[GatewayRecord]:
        """Deliver RX directly when backhaul is up."""
        return self._emit(self._rx, ingest_time=ingest_time, store_and_forward=False)

    def _emit(
        self,
        packets: list[IoTPacket],
        *,
        ingest_time: str,
        store_and_forward: bool,
    ) -> list[GatewayRecord]:
        out: list[GatewayRecord] = []
        for pkt in packets:
            rec = GatewayRecord(
                event_time=pkt.event_time,
                ingest_time=ingest_time,
                node_id=pkt.node_id,
                device_type=pkt.device_type,
                payload=dict(pkt.payload),
                rssi_dbm=pkt.rssi_dbm,
                store_and_forward=store_and_forward,
            )
            out.append(rec)
            self._delivered.append(rec)
        if packets is self._store:
            self._store.clear()
        elif packets is self._rx:
            self._rx.clear()
        return out

    def all_records(self) -> list[GatewayRecord]:
        return list(self._delivered)

    @property
    def store_depth(self) -> int:
        return len(self._store)
