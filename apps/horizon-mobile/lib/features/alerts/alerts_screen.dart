import 'package:flutter/material.dart';

import '../../core/app_scope.dart';
import '../../shared/models/alert_draft.dart';
import '../../shared/widgets/api_error_banner.dart';
import '../../shared/widgets/disclaimer_banner.dart';

class AlertsScreen extends StatefulWidget {
  const AlertsScreen({super.key});

  @override
  State<AlertsScreen> createState() => _AlertsScreenState();
}

class _AlertsScreenState extends State<AlertsScreen> {
  List<AlertDraft> _alerts = [];
  String? _error;
  bool _loading = false;

  var _started = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_started) {
      _started = true;
      _load();
    }
  }

  Future<void> _load() async {
    final api = AppScope.of(context).api;
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final body = await api.fetchAlerts();
      final list = (body['alerts'] as List<dynamic>? ?? [])
          .map((e) => AlertDraft.fromJson(e as Map<String, dynamic>))
          .toList();
      setState(() => _alerts = list);
    } catch (e) {
      setState(() => _error = e.toString());
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Alertas DRAFT'),
        actions: [
          IconButton(onPressed: _loading ? null : _load, icon: const Icon(Icons.refresh)),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const DisclaimerBanner(),
          const SizedBox(height: 12),
          if (_loading) const LinearProgressIndicator(),
          if (_error != null) ApiErrorBanner(message: _error!),
          if (!_loading && _alerts.isEmpty)
            const Text('Sin filas de alerta para el fixture por defecto.'),
          ..._alerts.map(
            (a) => Card(
              child: ListTile(
                title: Text('${a.level} · ${a.spatialUnitId}'),
                subtitle: Text('${a.status} · riesgo ${a.operationalRiskValue ?? "—"}'),
              ),
            ),
          ),
        ],
      ),
    );
  }
}
