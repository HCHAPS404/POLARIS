import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import 'core/api/polaris_api.dart';
import 'core/app_scope.dart';
import 'core/config/app_config.dart';
import 'core/theme/app_theme.dart';
import 'features/alerts/alerts_screen.dart';
import 'features/home/home_screen.dart';
import 'features/map/map_screen.dart';
import 'features/preparedness/preparedness_screen.dart';
import 'features/settings/settings_screen.dart';
import 'features/status/site_status_screen.dart';

class HorizonMobileApp extends StatefulWidget {
  const HorizonMobileApp({super.key});

  @override
  State<HorizonMobileApp> createState() => _HorizonMobileAppState();
}

class _HorizonMobileAppState extends State<HorizonMobileApp> {
  late AppConfig _config;
  late PolarisApi _api;
  late final GoRouter _router;

  @override
  void initState() {
    super.initState();
    _config = AppConfig.initial();
    _api = PolarisApi(baseUrl: _config.apiBaseUrl);
    _router = GoRouter(
      initialLocation: '/',
      routes: [
        StatefulShellRoute.indexedStack(
          builder: (context, state, navigationShell) {
            return _MainShell(navigationShell: navigationShell);
          },
          branches: [
            StatefulShellBranch(
              routes: [
                GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(path: '/map', builder: (_, __) => const MapScreen()),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(path: '/alerts', builder: (_, __) => const AlertsScreen()),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(path: '/status', builder: (_, __) => const SiteStatusScreen()),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(path: '/settings', builder: (_, __) => const SettingsScreen()),
              ],
            ),
            StatefulShellBranch(
              routes: [
                GoRoute(
                  path: '/preparedness',
                  builder: (_, __) => const PreparednessScreen(),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }

  void _updateConfig(AppConfig config) {
    if (config.apiBaseUrl != _config.apiBaseUrl) {
      _api.dispose();
      _api = PolarisApi(baseUrl: config.apiBaseUrl);
    }
    setState(() => _config = config);
  }

  @override
  void dispose() {
    _api.dispose();
    _router.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AppScope(
      config: _config,
      api: _api,
      updateConfig: _updateConfig,
      child: MaterialApp.router(
        title: 'POLARIS Horizon',
        theme: AppTheme.light(),
        routerConfig: _router,
      ),
    );
  }
}

class _MainShell extends StatelessWidget {
  const _MainShell({required this.navigationShell});

  final StatefulNavigationShell navigationShell;

  void _onTap(int index) {
    navigationShell.goBranch(index, initialLocation: index == navigationShell.currentIndex);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: navigationShell,
      bottomNavigationBar: NavigationBar(
        selectedIndex: navigationShell.currentIndex,
        onDestinationSelected: _onTap,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), label: 'Inicio'),
          NavigationDestination(icon: Icon(Icons.map_outlined), label: 'Mapa'),
          NavigationDestination(icon: Icon(Icons.notifications_outlined), label: 'Alertas'),
          NavigationDestination(icon: Icon(Icons.monitor_heart_outlined), label: 'Estado'),
          NavigationDestination(icon: Icon(Icons.settings_outlined), label: 'Ajustes'),
        ],
      ),
      floatingActionButton: navigationShell.currentIndex == 0
          ? null
          : FloatingActionButton.small(
              onPressed: () => context.go('/preparedness'),
              tooltip: 'Preparación (stub)',
              child: const Icon(Icons.checklist),
            ),
    );
  }
}
