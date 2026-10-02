import 'alert_draft.dart';

/// Minimal mirror of OpenAPI assessment unit (V1 flood slice).
class AssessmentSummary {
  AssessmentSummary({
    required this.spatialUnitId,
    required this.dataClass,
    this.gci,
    this.phi,
    this.operationalRisk,
    this.alert,
  });

  factory AssessmentSummary.fromJson(Map<String, dynamic> json, {String? dataClass}) {
    return AssessmentSummary(
      spatialUnitId: json['spatial_unit_id'] as String? ?? '—',
      dataClass: dataClass ?? json['data_class'] as String? ?? 'UNKNOWN',
      gci: _metric(json['gci']),
      phi: _metric(json['phi']),
      operationalRisk: _metric(json['operational_risk']),
      alert: json['alert'] != null
          ? AlertDraft.fromJson(json['alert'] as Map<String, dynamic>)
          : null,
    );
  }

  static double? _metric(Map<String, dynamic>? block) {
    if (block == null) return null;
    final value = block['value'];
    if (value is num) return value.toDouble();
    return null;
  }

  final String spatialUnitId;
  final String dataClass;
  final double? gci;
  final double? phi;
  final double? operationalRisk;
  final AlertDraft? alert;
}
