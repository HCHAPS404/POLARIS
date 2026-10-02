/// Offline manifest shape (DESIGNED — not persisted to disk in V1).
library;

class OfflineManifest {
  static const schemaVersion = 'horizon.mobile.offline.v0.1.0';

  const OfflineManifest({
    required this.dataClass,
    required this.fetchedAtUtc,
  });

  final String dataClass;
  final String fetchedAtUtc;

  Map<String, Object?> toJson() => {
        'schema_version': schemaVersion,
        'data_class': dataClass,
        'fetched_at': fetchedAtUtc,
      };
}
