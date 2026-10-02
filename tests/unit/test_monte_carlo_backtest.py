"""Monte Carlo backtest harness."""

from __future__ import annotations

from pathlib import Path

from harness.backtesting.monte_carlo import run_monte_carlo

ROOT = Path(__file__).resolve().parents[2]
Mocoa = ROOT / "simulation" / "scenarios" / "flood-mocoa-2017-replay.yaml"


def test_monte_carlo_seeded_report() -> None:
    report = run_monte_carlo(Mocoa, seed=42, draws=50)
    assert report["harness"] == "monte_carlo"
    assert report["draws"] == 50
    assert report["unit_distributions"]
    again = run_monte_carlo(Mocoa, seed=42, draws=50)
    assert again["unit_distributions"] == report["unit_distributions"]
