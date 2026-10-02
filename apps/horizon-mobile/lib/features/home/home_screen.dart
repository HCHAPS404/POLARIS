import 'package:flutter/material.dart';

import '../../core/app_scope.dart';
import '../../core/api/polaris_api.dart';
import '../../shared/widgets/api_error_banner.dart';
import '../../shared/widgets/data_class_chip.dart';
import '../../shared/widgets/disclaimer_banner.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  String _healthLine = '—';
  String _hazardLine = '—';
  String? _dataClass;
  String? _error;
  bool _loading = false;

  var _started = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_started) {
      _started = true;
      _refresh();
    }
  }

  Future<void> _refresh() async {
    final scope = AppScope.of(context);
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final health = await scope.api.fetchHealth();
      final assessments = await scope.api.fetchAssessments();
      setState(() {
        _healthLine = '${health['status']} · ${health['maturity']}';
        _hazardLine = PolarisApi.hazardStatusSummary(assessments);
        _dataClass = assessments['data_class'] as String?;
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        if (scope.api.cache.hasCachedPayload) {
          _hazardLine = 'Modo offline (stub): caché en memoria disponible';
        }
      });
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final scope = AppScope.of(context);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inicio'),
        actions: [
          IconButton(
            onPressed: _loading ? null : _refresh,
            icon: const Icon(Icons.refresh),
            tooltip: 'Actualizar',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          const DisclaimerBanner(),
          const SizedBox(height: 16),
          if (_dataClass != null) DataClassChip(dataClass: _dataClass!),
          const SizedBox(height: 12),
          Text('API: ${scope.config.apiBaseUrl}', style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: 12),
          _InfoTile(title: 'Health', value: _loading ? 'Cargando…' : _healthLine),
          _InfoTile(title: 'Estado de amenaza (V1)', value: _hazardLine),
          if (_error != null) ...[
            const SizedBox(height: 8),
            ApiErrorBanner(
              message: _error!,
              staleHint: scope.api.cache.hasCachedPayload
                  ? 'Mostrando última respuesta en caché (stub).'
                  : null,
            ),
          ],
        ],
      ),
    );
  }
}

class _InfoTile extends StatelessWidget {
  const _InfoTile({required this.title, required this.value});

  final String title;
  final String value;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      title: Text(title),
      subtitle: Text(value),
    );
  }
}
