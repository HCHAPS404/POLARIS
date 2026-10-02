"""Fault-injection harness catalog."""

from __future__ import annotations

from harness.fault_injection.runner import run_all


def test_fault_injection_catalog_passes() -> None:
    payload = run_all()
    assert payload["passed"] is True
    assert len(payload["scenarios"]) >= 5
