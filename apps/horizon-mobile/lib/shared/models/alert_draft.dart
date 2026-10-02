/// DRAFT alert row from `GET /v1/alerts` or nested under assessments.
class AlertDraft {
  AlertDraft({
    required this.spatialUnitId,
    required this.level,
    required this.status,
    this.hazardId,
    this.operationalRiskValue,
  });

  factory AlertDraft.fromJson(Map<String, dynamic> json) {
    return AlertDraft(
      spatialUnitId: json['spatial_unit_id'] as String? ?? '—',
      level: json['level'] as String? ?? '—',
      status: json['status'] as String? ?? 'DRAFT',
      hazardId: json['hazard_id'] as String?,
      operationalRiskValue: (json['operational_risk_value'] as num?)?.toDouble(),
    );
  }

  final String spatialUnitId;
  final String level;
  final String status;
  final String? hazardId;
  final double? operationalRiskValue;
}
