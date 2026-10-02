"""Backtesting experiments API + Bogotá 2018 replay."""

from __future__ import annotations

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_experiments_catalog_lists_downloads() -> None:
    res = client.get("/v1/backtesting/experiments")
    assert res.status_code == 200
    body = res.json()
    assert body["evidence"] == "EXPERIMENTAL"
    ids = {e["id"] for e in body["experiments"]}
    assert "flood-mocoa-2017-replay" in ids
    assert "flood-bogota-2018-april-replay" in ids


def test_bogota_2018_backtest_runs() -> None:
    res = client.get("/v1/backtests/flood-bogota-2018-april-replay", params={"seed": 42})
    assert res.status_code == 200
    body = res.json()
    assert body["scenario_id"] == "flood-bogota-2018-april-replay"
