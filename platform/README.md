# Platform

**Evidence:** DESIGNED · health + V1 flood application/API IMPLEMENTED

Hexagonal core: `domain`, `application`, `ports`, `adapters`, `api`. Do not add `platform/__init__.py` (stdlib name clash). API lives in `platform/api`. Flood slice orchestration lives in `platform/application/flood_assessment.py`.
