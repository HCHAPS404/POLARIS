# horizon-mobile

**Evidence:** IMPLEMENTED (minimal APK build in CI; **not** app-store ready)

Horizon Mobile — Flutter field shell (ADR-0003). Consumes the same POLARIS API as Horizon Web:

- `GET /health`
- `GET /v1/assessments` (hazard status summary, DRAFT alerts)
- Map **placeholder** (WebView to `/horizon/` documented for a later slice)

## Offline

`lib/services/offline_cache_stub.dart` — in-memory stub only; documents future `path_provider` persistence.

## Local dev

```bash
cd apps/horizon-mobile
flutter pub get
flutter test
# API on host: make api  (default base http://10.0.2.2:8000 on Android emulator)
flutter run
```

## Disclaimer

Decision-support only. SIMULATED / HISTORICAL_REPLAY data. Human-in-the-loop for DRAFT alerts.
