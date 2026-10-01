# Agents — horizon-mobile

**Evidence:** IMPLEMENTED (nested agent notes)

- Flutter is the chosen stack (ADR-0003).
- Do not generate a full app in P0. No `pubspec.yaml` until a real slice is requested.
- CI must skip, not fail, while this folder is README-only.
- Offline + HITL disclaimers are mandatory when UI appears.
