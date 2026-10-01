"""Resolve ObservationRepository: PostGIS when configured, else in-memory."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import TYPE_CHECKING

from adapters.storage.memory_repository import MemoryObservationRepository
from adapters.storage.postgis_repository import PostgisObservationRepository

if TYPE_CHECKING:
    from platform.ports.persistence import ObservationRepository

_MEMORY = MemoryObservationRepository()


@lru_cache(maxsize=1)
def _postgis_singleton() -> PostgisObservationRepository | None:
    if os.environ.get("POLARIS_USE_MEMORY_REPO", "").lower() in ("1", "true", "yes"):
        return None
    repo = PostgisObservationRepository.from_env(create_tables=False)
    if repo is None:
        return None
    if not repo.is_available():
        return None
    return repo


def get_observation_repository() -> ObservationRepository:
    pg = _postgis_singleton()
    if pg is not None:
        return pg
    return _MEMORY


def reset_repository_cache() -> None:
    _postgis_singleton.cache_clear()


def memory_repository_for_tests() -> MemoryObservationRepository:
    """Explicit in-memory repo (tests)."""
    return _MEMORY
