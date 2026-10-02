/// Stub for future `GET /v1/observations` list rows (not wired in UI yet).
class ObservationSummary {
  ObservationSummary({
    required this.observationId,
    required this.siteId,
    required this.dataClass,
    this.variable,
  });

  factory ObservationSummary.fromJson(Map<String, dynamic> json) {
    return ObservationSummary(
      observationId: json['observation_id'] as String? ?? '—',
      siteId: json['site_id'] as String? ?? '—',
      dataClass: json['data_class'] as String? ?? 'UNKNOWN',
      variable: json['variable'] as String?,
    );
  }

  final String observationId;
  final String siteId;
  final String dataClass;
  final String? variable;
}
