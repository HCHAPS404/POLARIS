import 'package:flutter/material.dart';

import '../../core/app_scope.dart';
import '../../core/config/app_config.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late TextEditingController _apiController;
  late TextEditingController _horizonController;

  var _started = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_started) return;
    _started = true;
    final config = AppScope.of(context).config;
    _apiController = TextEditingController(text: config.apiBaseUrl);
    _horizonController = TextEditingController(text: config.horizonPath);
  }

  @override
  void dispose() {
    _apiController.dispose();
    _horizonController.dispose();
    super.dispose();
  }

  void _apply() {
    final scope = AppScope.of(context);
    scope.updateConfig(
      scope.config.copyWith(
        apiBaseUrl: _apiController.text.trim(),
        horizonPath: _horizonController.text.trim(),
      ),
    );
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Configuración aplicada (sesión). Reinicia navegación si cambió la API.')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Ajustes')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            'Emulador Android: use ${AppConfig.defaultApiBase} para alcanzar el host en el puerto 8000.',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _apiController,
            decoration: const InputDecoration(
              labelText: 'API base URL',
              hintText: 'http://10.0.2.2:8000',
            ),
            keyboardType: TextInputType.url,
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _horizonController,
            decoration: const InputDecoration(
              labelText: 'Horizon path',
              hintText: '/horizon/?fixture_id=flood-bogota-demo',
            ),
          ),
          const SizedBox(height: 16),
          FilledButton(onPressed: _apply, child: const Text('Aplicar')),
        ],
      ),
    );
  }
}
