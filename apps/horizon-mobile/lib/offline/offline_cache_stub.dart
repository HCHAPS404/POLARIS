/// In-memory offline cache stub (tests + demo). See [README.md](README.md).
class OfflineCacheStub {
  String? lastHealthJson;
  String? lastAssessmentsJson;
  String? lastAlertsJson;

  bool get hasCachedPayload =>
      lastHealthJson != null ||
      lastAssessmentsJson != null ||
      lastAlertsJson != null;

  void rememberHealth(String body) => lastHealthJson = body;

  void rememberAssessments(String body) => lastAssessmentsJson = body;

  void rememberAlerts(String body) => lastAlertsJson = body;

  void clear() {
    lastHealthJson = null;
    lastAssessmentsJson = null;
    lastAlertsJson = null;
  }
}
