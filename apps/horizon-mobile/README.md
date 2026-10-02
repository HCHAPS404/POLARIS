# horizon-mobile

**Evidence:** IMPLEMENTED (minimal APK build in CI; **not** app-store ready)

Horizon Mobile — Flutter field shell (ADR-0003). Consumes the same POLARIS API as Horizon Web:

- `GET /health`
- `GET /v1/assessments` (hazard status summary, DRAFT alerts)
- Map via **WebView** → `/horizon/` on the API (SIMULATED / HISTORICAL_REPLAY only)

## Offline

`lib/services/offline_cache_stub.dart` — in-memory stub only; documents future `path_provider` persistence.

## Local dev (against docker compose or `make api`)

1. Start API on the host (port 8000):

   ```bash
   cp .env.example .env   # from repo root
   make up                # or: make api
   ```

2. Run the app:

   ```bash
   cd apps/horizon-mobile
   flutter pub get
   flutter test
   ```

   **Android emulator** (default API base `http://10.0.2.2:8000`):

   ```bash
   flutter run
   ```

   **Physical device** on the same LAN (replace with your machine IP):

   ```bash
   flutter run --dart-define=POLARIS_API_BASE=http://192.168.1.10:8000
   ```

   Optional Horizon path / fixture:

   ```bash
   flutter run --dart-define=POLARIS_HORIZON_PATH=/horizon/?fixture_id=flood-mocoa-2017-replay
   ```

## Disclaimer

Decision-support only. SIMULATED / HISTORICAL_REPLAY data. Human-in-the-loop for DRAFT alerts.
