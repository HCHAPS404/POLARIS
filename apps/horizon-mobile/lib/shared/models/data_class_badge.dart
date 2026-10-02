/// Mirrors API `data_class` on assessment/observation payloads.
enum DataClassBadge {
  simulated('SIMULATED'),
  historicalReplay('HISTORICAL_REPLAY'),
  liveIntegrated('LIVE_INTEGRATED'),
  unknown('UNKNOWN');

  const DataClassBadge(this.apiValue);
  final String apiValue;

  static DataClassBadge parse(String? raw) {
    return DataClassBadge.values.firstWhere(
      (v) => v.apiValue == raw,
      orElse: () => DataClassBadge.unknown,
    );
  }

  String get shortLabel {
    switch (this) {
      case DataClassBadge.simulated:
        return 'SIM';
      case DataClassBadge.historicalReplay:
        return 'REPLAY';
      case DataClassBadge.liveIntegrated:
        return 'LIVE';
      case DataClassBadge.unknown:
        return '?';
    }
  }
}
