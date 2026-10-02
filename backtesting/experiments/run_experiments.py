"""Run catalogued backtesting experiments (EXPERIMENTAL)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.backtesting.monte_carlo import run_monte_carlo  # noqa: E402
from harness.backtesting.replay import run_backtest  # noqa: E402

CATALOG = Path(__file__).parent / "catalog.yaml"
REPORTS = ROOT / "backtesting" / "reports"


def load_catalog() -> list[dict[str, Any]]:
    raw = yaml.safe_load(CATALOG.read_text(encoding="utf-8"))
    return list(raw.get("experiments") or [])


def run_experiment(experiment_id: str, *, seed: int, mc_draws: int) -> dict[str, Any]:
    entry = next((e for e in load_catalog() if e["id"] == experiment_id), None)
    if entry is None:
        raise KeyError(f"unknown experiment {experiment_id!r}")
    scenario = ROOT / str(entry["scenario"])
    backtest = run_backtest(scenario, seed)
    monte_carlo = run_monte_carlo(scenario, seed=seed, draws=mc_draws)
    return {
        "experiment_id": experiment_id,
        "title": entry.get("title"),
        "evidence": entry.get("evidence", "EXPERIMENTAL"),
        "seed": seed,
        "backtest": backtest,
        "monte_carlo": monte_carlo,
    }


def run_all(*, seed: int, mc_draws: int) -> dict[str, Any]:
    results = [run_experiment(e["id"], seed=seed, mc_draws=mc_draws) for e in load_catalog()]
    return {"evidence": "EXPERIMENTAL", "seed": seed, "experiments": results}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS backtesting experiments")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--mc-draws", type=int, default=100)
    parser.add_argument("--output", type=Path, default=REPORTS / "experiments-latest.json")
    args = parser.parse_args(argv)
    payload = run_all(seed=args.seed, mc_draws=args.mc_draws)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"written": str(args.output), "count": len(payload["experiments"])}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
