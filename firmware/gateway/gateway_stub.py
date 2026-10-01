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
            self.state = GatewayState.BUFFER
        return self.state
