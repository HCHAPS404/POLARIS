# Horizon Mobile — local test guide

**Evidence:** IMPLEMENTED (manual steps for emulator + APK debug build)

Decision-support only. Data is `SIMULATED` or `HISTORICAL_REPLAY`. Alerts are `DRAFT`.

## Prerequisites

- Flutter SDK 3.24+ (matches CI)
- Android SDK + emulator **or** physical device on the same LAN as the API
- POLARIS API running on port **8000** (see [local-deployment.md](./local-deployment.md))

## 1. Start the API

From repo root:

```bash
cp .env.example .env
docker compose up --build
# or: make up
curl -s http://localhost:8000/health | jq .
```

Optional checkout for the pre-local bundle tag:

```bash
git fetch --tags
git checkout v1.1.0-pre-local   # when tagged on remote
```

## 2. Android emulator networking

The emulator maps the host loopback to **`10.0.2.2`**. Default app config:

`http://10.0.2.2:8000`

No change needed if the API listens on host port 8000.

## 3. Physical device

Use your machine's LAN IP:

```bash
cd apps/horizon-mobile
flutter run --dart-define=POLARIS_API_BASE=http://192.168.1.10:8000
```

You can also set the base URL in **Settings** inside the app (session only).

## 4. Run tests and app

```bash
cd apps/horizon-mobile
flutter pub get
flutter analyze
flutter test
flutter run
```

Optional Horizon fixture path:

```bash
flutter run --dart-define=POLARIS_HORIZON_PATH=/horizon/?fixture_id=flood-mocoa-2017-replay
```

## 5. Build debug APK

```bash
flutter build apk --debug
```

Artifact: `build/app/outputs/flutter-apk/app-debug.apk`

## 6. What to verify

| Screen | Expect |
|--------|--------|
| Home | Disclaimer, health line from `/health`, hazard summary from `/v1/assessments` |
| Map | WebView loads `/horizon/` on the API host |
| Alerts | List stub from assessments/alerts contract |
| Site status | Bootstrap + storage backend from health |
| Settings | API base URL field (default `10.0.2.2:8000` on emulator) |

If the API is down, screens show an error banner; cached in-memory payloads may show an **offline (stub)** hint.

## CI parity

GitHub workflow `.github/workflows/mobile.yml` runs `flutter analyze`, `flutter test`, and `flutter build apk --debug` on changes under `apps/horizon-mobile/`.
