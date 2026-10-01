/// Offline cache **stub** (DESIGNED → minimal IMPLEMENTED in-memory only).
///
/// Production would persist last-good assessments + map GeoJSON under
/// `path_provider` with TTL and provenance. This stub documents the contract
/// without claiming full offline GIS.
library;

class OfflineCacheStub {
  OfflineCacheStub();

  String? _lastHealthJson;
  String? _lastAssessmentsJson;

  void rememberHealth(String body) => _lastHealthJson = body;

  void rememberAssessments(String body) => _lastAssessmentsJson = body;

  String? get lastHealthJson => _lastHealthJson;

  String? get lastAssessmentsJson => _lastAssessmentsJson;

  bool get hasCachedPayload => _lastHealthJson != null || _lastAssessmentsJson != null;

  void clear() {
    _lastHealthJson = null;
    _lastAssessmentsJson = null;
  }
}
