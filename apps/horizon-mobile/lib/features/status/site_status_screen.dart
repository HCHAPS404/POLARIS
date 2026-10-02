import 'package:flutter/material.dart';

import '../../core/app_scope.dart';
import '../../shared/widgets/api_error_banner.dart';

class SiteStatusScreen extends StatefulWidget {
  const SiteStatusScreen({super.key});

  @override
  State<SiteStatusScreen> createState() => _SiteStatusScreenState();
}

class _SiteStatusScreenState extends State<SiteStatusScreen> {
  Map<String, dynamic>? _health;
  Map<String, dynamic>? _bootstrap;
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
      final health = await api.fetchHealth();
      Map<String, dynamic>? bootstrap;
      try {
        bootstrap = await api.fetchBootstrap();
      } on Exception {
        bootstrap = null;
      }
      setState(() {
        _health = health;
        _bootstrap = bootstrap;
      });
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
        title: const Text('Estado del sitio'),
        actions: [
          IconButton(onPressed: _loading ? null : _load, icon: const Icon(Icons.refresh)),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          if (_loading) const LinearProgressIndicator(),
          if (_error != null) ApiErrorBanner(message: _error!),
          if (_health != null) ...[
            Text('Servicio: ${_health!['service']}'),
            Text('Maturity: ${_health!['maturity']}'),
            Text('Storage: ${_health!['storage_backend']}'),
            Text('UTC: ${_health!['utc']}'),
          ],
          if (_bootstrap != null) ...[
            const SizedBox(height: 16),
            Text('Bootstrap', style: Theme.of(context).textTheme.titleMedium),
            Text('Horizon: ${_bootstrap!['horizon_url']}'),
            Text('Fixtures: ${(_bootstrap!['fixtures'] as List).join(", ")}'),
          ],
        ],
      ),
    );
  }
}
