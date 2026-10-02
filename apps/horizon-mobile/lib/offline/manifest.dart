/// Offline manifest shape (DESIGNED — not persisted to disk in V1).
library;

class OfflineManifest {
  const OfflineManifest({
    required this.schemaVersion,
    required this.dataClass,
    required this.fetchedAtUtc,
  });

  static const schemaVersion = 'horizon.mobile.offline.v0.1.0';

  final String schemaVersion;
  final String dataClass;
  final String fetchedAtUtc;

  Map<String, Object?> toJson() => {
        'schema_version': schemaVersion,
        'data_class': dataClass,
        'fetched_at': fetchedAtUtc,
      };
}
