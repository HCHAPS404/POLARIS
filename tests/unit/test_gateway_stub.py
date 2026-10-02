"""Gateway firmware stub store-and-forward behaviour."""

from __future__ import annotations

from firmware.gateway.gateway_stub import GatewayState, GatewayStub


def test_gateway_buffer_and_flush() -> None:
    gw = GatewayStub(max_packets=4)
    assert gw.ingest_lora(b"a")
    assert gw.ingest_lora(b"b")
    gw.tick(backhaul_up=True)  # BOOT -> BUFFER
    gw.tick(backhaul_up=True)  # BUFFER -> FORWARD
    gw.tick(backhaul_up=True)  # FORWARD -> FLUSH
    gw.tick(backhaul_up=True)  # FLUSH -> BUFFER, clears
    assert gw.forwarded == 2
    assert gw.buffer == []


def test_gateway_hold_when_backhaul_down() -> None:
    gw = GatewayStub()
    gw.ingest_lora(b"x")
    gw.tick(backhaul_up=True)
    gw.tick(backhaul_up=True)
    gw.tick(backhaul_up=False)
    assert gw.state == GatewayState.HOLD
    assert gw.held == 1
