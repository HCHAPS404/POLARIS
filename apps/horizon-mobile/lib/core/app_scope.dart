import 'package:flutter/material.dart';

import 'api/polaris_api.dart';
import 'config/app_config.dart';

/// Session-scoped config + API client for feature screens.
class AppScope extends InheritedWidget {
  const AppScope({
    super.key,
    required this.config,
    required this.api,
    required this.updateConfig,
    required super.child,
  });

  final AppConfig config;
  final PolarisApi api;
  final void Function(AppConfig config) updateConfig;

  static AppScope of(BuildContext context) {
    final scope = context.dependOnInheritedWidgetOfExactType<AppScope>();
    assert(scope != null, 'AppScope not found');
    return scope!;
  }

  @override
  bool updateShouldNotify(AppScope oldWidget) =>
      oldWidget.config != config || oldWidget.api != api;
}
