import 'dart:convert';

import 'package:http/http.dart' as http;

import '../../offline/offline_cache_stub.dart';

/// Minimal client for POLARIS V1 (SIMULATED fixtures via API).
class PolarisApi {
  PolarisApi({
    required this.baseUrl,
    http.Client? client,
    OfflineCacheStub? cache,
  })  : _client = client ?? http.Client(),
        cache = cache ?? OfflineCacheStub();

  final String baseUrl;
  final http.Client _client;
  final OfflineCacheStub cache;

  Uri _uri(String path) => Uri.parse('$baseUrl$path');

  Future<Map<String, dynamic>> fetchHealth({bool useCacheOnFailure = true}) async {
    try {
      final response = await _client.get(_uri('/health'));
      if (response.statusCode != 200) {
        throw PolarisApiException('health ${response.statusCode}');
      }
      cache.rememberHealth(response.body);
      return jsonDecode(response.body) as Map<String, dynamic>;
    } on Exception {
      if (useCacheOnFailure && cache.lastHealthJson != null) {
        return jsonDecode(cache.lastHealthJson!) as Map<String, dynamic>;
      }
      rethrow;
    }
  }

  Future<Map<String, dynamic>> fetchBootstrap({bool useCacheOnFailure = false}) async {
    final response = await _client.get(_uri('/v1/mobile/bootstrap'));
    if (response.statusCode != 200) {
      throw PolarisApiException('bootstrap ${response.statusCode}');
    }
    return jsonDecode(response.body) as Map<String, dynamic>;
  }

  Future<Map<String, dynamic>> fetchAssessments({bool useCacheOnFailure = true}) async {
    try {
      final response = await _client.get(_uri('/v1/assessments'));
      if (response.statusCode != 200) {
        throw PolarisApiException('assessments ${response.statusCode}');
      }
      cache.rememberAssessments(response.body);
      return jsonDecode(response.body) as Map<String, dynamic>;
    } on Exception {
      if (useCacheOnFailure && cache.lastAssessmentsJson != null) {
        return jsonDecode(cache.lastAssessmentsJson!) as Map<String, dynamic>;
      }
      rethrow;
    }
  }

  Future<Map<String, dynamic>> fetchAlerts({
    String fixtureId = 'flood-bogota-demo',
    bool useCacheOnFailure = true,
  }) async {
    try {
      final response = await _client.get(
        _uri('/v1/alerts?fixture_id=${Uri.encodeComponent(fixtureId)}'),
      );
      if (response.statusCode != 200) {
        throw PolarisApiException('alerts ${response.statusCode}');
      }
      cache.rememberAlerts(response.body);
      return jsonDecode(response.body) as Map<String, dynamic>;
    } on Exception {
      if (useCacheOnFailure && cache.lastAlertsJson != null) {
        return jsonDecode(cache.lastAlertsJson!) as Map<String, dynamic>;
      }
      rethrow;
    }
  }

  static String hazardStatusSummary(Map<String, dynamic> assessmentsBody) {
    final dataClass = assessmentsBody['data_class'] ?? 'UNKNOWN';
    final list = assessmentsBody['assessments'] as List<dynamic>? ?? [];
    if (list.isEmpty) {
      return 'Sin unidades ($dataClass)';
    }
    final draftCount = list.where((u) {
      final alert = (u as Map<String, dynamic>)['alert'] as Map<String, dynamic>?;
      return alert?['status'] == 'DRAFT';
    }).length;
    return '${list.length} unidades · $dataClass · $draftCount alertas DRAFT';
  }

  void dispose() => _client.close();
}

class PolarisApiException implements Exception {
  PolarisApiException(this.message);
  final String message;

  @override
  String toString() => 'PolarisApiException: $message';
}
