"""
POLARIS gateway firmware stub — Raspberry Pi 5 reference (SIMULATED / PLACEHOLDER).

State machine: BOOT → BUFFER → FORWARD → (hold on backhaul down) → FLUSH.

Production would run packet forwarder + MQTT/HTTP ingest; Digital Testbed uses
simulation.python.iot.gateway.GatewaySim.
"""

from __future__ import annotations

from enum import Enum, auto


class GatewayState(Enum):
    BOOT = auto()
    BUFFER = auto()
    FORWARD = auto()
    HOLD = auto()
    FLUSH = auto()


class GatewayStub:
    state: GatewayState = GatewayState.BOOT
    buffer: list[bytes]
    max_packets: int = 256
    forwarded: int = 0
    held: int = 0

    def __init__(self, *, max_packets: int = 256) -> None:
        self.buffer = []
        self.max_packets = max_packets
        self.forwarded = 0
        self.held = 0
        self.state = GatewayState.BOOT

    def ingest_lora(self, payload: bytes) -> bool:
        """Accept one uplink frame into the store-and-forward buffer."""
        if len(self.buffer) >= self.max_packets:
            return False
        self.buffer.append(payload)
        return True

    def tick(self, *, backhaul_up: bool) -> GatewayState:
        if self.state == GatewayState.BOOT:
            self.state = GatewayState.BUFFER
        elif self.state == GatewayState.BUFFER:
            self.state = GatewayState.FORWARD
        elif self.state == GatewayState.FORWARD:
            self.state = GatewayState.FLUSH if backhaul_up else GatewayState.HOLD
        elif self.state == GatewayState.HOLD and backhaul_up:
            self.state = GatewayState.FLUSH
        elif self.state == GatewayState.FLUSH:
            flushed = len(self.buffer)
            if flushed:
                self.forwarded += flushed
                self.buffer.clear()
            self.state = GatewayState.BUFFER
        if self.state == GatewayState.HOLD:
            self.held = len(self.buffer)
        return self.state
