"""SIMULATED IoT fault injection flags."""

from __future__ import annotations

from pathlib import Path

from simulation.python.iot.pipeline import apply_fault_injection, run_iot_scenario_path

ROOT = Path(__file__).resolve().parents[2]


def test_apply_fault_gateway_down_sets_backhaul() -> None:
    scenario = {"fault_injection": "gateway_down", "communication": {}}
    out = apply_fault_injection(scenario)
    assert out["backhaul_down"] is True
    assert out["fault_injection"] == "gateway_down"


def test_apply_fault_packet_loss_sets_comm() -> None:
    out = apply_fault_injection({"fault_injection": "packet_loss"})
    assert out["communication"]["packet_loss"] == 0.5


def test_packet_loss_scenario_drops_a_packet() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "iot-bogota-fault-packet-loss.yaml"
    payload = run_iot_scenario_path(scenario, seed=0)
    assert payload["gateway"]["fault_injection"] == "packet_loss"
    assert payload["packets_tx"] == 1


def test_gateway_down_fault_matches_store_and_forward() -> None:
    scenario = ROOT / "simulation" / "scenarios" / "iot-bogota-fault-gateway-down.yaml"
    payload = run_iot_scenario_path(scenario, seed=42)
    assert payload["gateway"]["fault_injection"] == "gateway_down"
    assert payload["gateway"]["backhaul_down"] is True
    assert payload["gateway"]["held_packets"] == 2
