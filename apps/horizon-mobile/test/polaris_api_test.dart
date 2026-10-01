import 'package:flutter_test/flutter_test.dart';
import 'package:horizon_mobile/services/offline_cache_stub.dart';
import 'package:horizon_mobile/services/polaris_api.dart';

void main() {
  test('hazardStatusSummary counts DRAFT alerts', () {
    final body = {
      'data_class': 'SIMULATED',
      'assessments': [
        {
          'alert': {'status': 'DRAFT'},
        },
        {
          'alert': {'status': 'DRAFT'},
        },
      ],
    };
    final summary = PolarisApi.hazardStatusSummary(body);
    expect(summary, contains('2 unidades'));
    expect(summary, contains('2 alertas DRAFT'));
  });

  test('offline cache stub stores payloads', () {
    final cache = OfflineCacheStub();
    cache.rememberHealth('{"status":"ok"}');
    expect(cache.lastHealthJson, '{"status":"ok"}');
    cache.clear();
    expect(cache.hasCachedPayload, isFalse);
  });
}
