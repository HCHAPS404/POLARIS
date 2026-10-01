import 'package:flutter/material.dart';

import 'services/polaris_api.dart';

/// Default for Android emulator → host machine API (`make api`).
const kDefaultApiBase = String.fromEnvironment(
  'POLARIS_API_BASE',
  defaultValue: 'http://10.0.2.2:8000',
);

void main() {
  runApp(const HorizonMobileApp());
}

class HorizonMobileApp extends StatelessWidget {
  const HorizonMobileApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'POLARIS Horizon',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0B3D5C)),
        useMaterial3: true,
      ),
      home: HorizonHomeScreen(api: PolarisApi(baseUrl: kDefaultApiBase)),
    );
  }
}

class HorizonHomeScreen extends StatefulWidget {
  const HorizonHomeScreen({super.key, required this.api});

  final PolarisApi api;

  @override
  State<HorizonHomeScreen> createState() => _HorizonHomeScreenState();
}

class _HorizonHomeScreenState extends State<HorizonHomeScreen> {
  String _healthLine = '—';
  String _hazardLine = '—';
  String? _error;
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _refresh();
  }

  Future<void> _refresh() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final health = await widget.api.fetchHealth();
      final assessments = await widget.api.fetchAssessments();
      setState(() {
        _healthLine = '${health['status']} · ${health['maturity']}';
        _hazardLine = PolarisApi.hazardStatusSummary(assessments);
      });
    } catch (e) {
      setState(() {
        _error = e.toString();
        if (widget.api.cache.hasCachedPayload) {
          _hazardLine = 'Modo offline (stub): caché en memoria disponible';
        }
      });
    } finally {
      setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    widget.api.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Horizon Mobile'),
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
          const _DisclaimerBanner(),
          const SizedBox(height: 16),
          Text('API: $kDefaultApiBase', style: Theme.of(context).textTheme.bodySmall),
          const SizedBox(height: 12),
          _InfoTile(title: 'Health', value: _healthLine),
          _InfoTile(title: 'Estado de amenaza (V1)', value: _hazardLine),
          if (_error != null) ...[
            const SizedBox(height: 8),
            Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ],
          const SizedBox(height: 24),
          Text('Mapa', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          const _MapPlaceholder(),
        ],
      ),
    );
  }
}

class _DisclaimerBanner extends StatelessWidget {
  const _DisclaimerBanner();

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Theme.of(context).colorScheme.errorContainer,
      borderRadius: BorderRadius.circular(8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Text(
          'Solo apoyo a la decisión. Datos SIMULATED/REPLAY. Alertas DRAFT con humano en el loop. '
          'POLARIS no es un servicio oficial de alerta.',
          style: Theme.of(context).textTheme.bodyMedium,
        ),
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

/// Placeholder until WebView to `/horizon/` is wired for production builds.
class _MapPlaceholder extends StatelessWidget {
  const _MapPlaceholder();

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 220,
      alignment: Alignment.center,
      decoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(8),
        color: Theme.of(context).colorScheme.surfaceContainerHighest,
      ),
      child: const Padding(
        padding: EdgeInsets.all(16),
        child: Text(
          'Placeholder de mapa.\n'
          'En producción: WebView → /horizon/ (MapLibre SIMULATED).\n'
          'Caché offline: stub en lib/services/offline_cache_stub.dart',
          textAlign: TextAlign.center,
        ),
      ),
    );
  }
}
