"""Unit tests for in-memory observation repository."""

from __future__ import annotations

from adapters.storage.memory_repository import MemoryObservationRepository


def test_memory_repo_roundtrip() -> None:
    repo = MemoryObservationRepository()
    repo.clear()
    obs = [
        {
            "observation_id": "a",
            "observed_at": "t",
            "observed_property": "rainfall_mm",
            "value": 1.0,
        }
    ]
    assert repo.save_observations(run_id="run-1", observations=obs) == 1
    repo.save_assessment_snapshot(run_id="run-1", fixture_id="fx", snapshot={"ok": True})
    listed = repo.list_observations(run_id="run-1")
    assert listed[0]["observation_id"] == "a"
    assert repo.get_observation("a") is not None
    assert repo.get_assessment_snapshot("run-1") == {"ok": True}
