"""Seeded Monte Carlo harness over HISTORICAL_REPLAY PHI (EXPERIMENTAL)."""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PLATFORM = ROOT / "platform"
if str(PLATFORM) not in sys.path:
    sys.path.insert(0, str(PLATFORM))

from adapters.storage.simulated_json import load_fixture  # noqa: E402
from domains.common import DATA_CLASS_HISTORICAL_REPLAY, DATA_CLASS_LIVE  # noqa: E402
from harness.backtesting.replay import load_ground_truth, run_backtest  # noqa: E402
from hazards.flood.phi import FORMULA_VERSION, compute_phi  # noqa: E402


def _perturb_rainfall(base_mm: float, rng: random.Random, sigma_fraction: float) -> float:
    sigma = max(base_mm * sigma_fraction, 0.5)
    return max(0.0, rng.gauss(base_mm, sigma))


def run_monte_carlo(
    scenario_path: Path,
    *,
    seed: int,
    draws: int,
    rainfall_sigma_fraction: float = 0.08,
) -> dict[str, Any]:
    if draws < 1:
        raise ValueError("draws must be >= 1")
    baseline = run_backtest(scenario_path, seed)
    scenario = yaml.safe_load(scenario_path.read_text(encoding="utf-8"))
    if scenario.get("data_class") == DATA_CLASS_LIVE:
        raise ValueError("refusing LIVE scenario")
    if scenario.get("data_class") != DATA_CLASS_HISTORICAL_REPLAY:
        raise ValueError("monte carlo harness requires HISTORICAL_REPLAY")
    fixture = load_fixture(str(scenario["scenario_id"]))
    truth = load_ground_truth(ROOT / str(scenario["ground_truth"]))
    rng = random.Random(seed)
    unit_stats: dict[str, dict[str, Any]] = {}
    for draw in range(draws):
        draw_rng = random.Random(rng.randint(0, 2**31 - 1))
        for obs in fixture.get("observations", []):
            if obs.get("observed_property") != "rainfall_mm":
                continue
            unit_id = str(obs["spatial_unit_id"])
            rain = _perturb_rainfall(
                float(obs["value"]), draw_rng, rainfall_sigma_fraction
            )
            phi = compute_phi(
                rainfall_mm=rain,
                phi_mode=str(obs.get("phi_mode") or "DETECTION"),
                spatial_unit_id=unit_id,
                observed_at=str(obs["observed_at"]),
                run_id=f"mc-{seed}-{draw}",
                computed_at=str(obs["observed_at"]),
                source_id=str(obs.get("source_id") or "mc"),
                quality_flag=str(obs.get("quality_flag") or "qc_pass"),
                data_class=str(obs.get("data_class") or DATA_CLASS_HISTORICAL_REPLAY),
                accumulation=str(obs.get("provenance", {}).get("accumulation") or "1h"),
            )
            stats = unit_stats.setdefault(
                unit_id,
                {"phi_samples": [], "rainfall_samples": [], "ground_truth_flooded": None},
            )
            stats["phi_samples"].append(phi.value)
            stats["rainfall_samples"].append(rain)
            if stats["ground_truth_flooded"] is None:
                gt_row = next(
                    (u for u in truth["units"] if u["spatial_unit_id"] == unit_id), None
                )
                if gt_row:
                    stats["ground_truth_flooded"] = bool(gt_row["ground_truth_flooded"])
                else:
                    stats["ground_truth_flooded"] = None

    summaries = []
    for unit_id, stats in sorted(unit_stats.items()):
        samples = stats["phi_samples"]
        summaries.append(
            {
                "spatial_unit_id": unit_id,
                "ground_truth_flooded": stats["ground_truth_flooded"],
                "phi_mean": sum(samples) / len(samples),
                "phi_p05": sorted(samples)[max(0, int(0.05 * len(samples)) - 1)],
                "phi_p50": sorted(samples)[len(samples) // 2],
                "phi_p95": sorted(samples)[min(len(samples) - 1, int(0.95 * len(samples)))],
                "rainfall_mm_mean": sum(stats["rainfall_samples"]) / len(stats["rainfall_samples"]),
            }
        )

    return {
        "evidence": "EXPERIMENTAL",
        "harness": "monte_carlo",
        "scenario_id": baseline["scenario_id"],
        "seed": seed,
        "draws": draws,
        "rainfall_sigma_fraction": rainfall_sigma_fraction,
        "formula_version_phi": FORMULA_VERSION,
        "baseline_backtest": {
            "pod": baseline.get("pod"),
            "far": baseline.get("far"),
            "counts": baseline.get("counts"),
        },
        "unit_distributions": summaries,
        "limitations": list(truth.get("limitations") or ()),
        "disclaimer": baseline.get("disclaimer"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="POLARIS Monte Carlo backtest (EXPERIMENTAL)")
    parser.add_argument(
        "--scenario",
        type=Path,
        default=ROOT / "simulation" / "scenarios" / "flood-mocoa-2017-replay.yaml",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--draws", type=int, default=200)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args(argv)
    payload = run_monte_carlo(args.scenario, seed=args.seed, draws=args.draws)
    text = json.dumps(payload, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
