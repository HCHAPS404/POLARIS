/// Compile-time defaults for local POLARIS API (Android emulator → host).
class AppConfig {
  const AppConfig({
    required this.apiBaseUrl,
    required this.horizonPath,
  });

  /// Default for Android emulator → host machine API (`make api` / docker compose).
  static const defaultApiBase = String.fromEnvironment(
    'POLARIS_API_BASE',
    defaultValue: 'http://10.0.2.2:8000',
  );

  /// WebView loads Horizon static mount; override for device → LAN IP.
  static const defaultHorizonPath = String.fromEnvironment(
    'POLARIS_HORIZON_PATH',
    defaultValue: '/horizon/?fixture_id=flood-bogota-demo',
  );

  factory AppConfig.initial() => const AppConfig(
        apiBaseUrl: defaultApiBase,
        horizonPath: defaultHorizonPath,
      );

  final String apiBaseUrl;
  final String horizonPath;

  AppConfig copyWith({String? apiBaseUrl, String? horizonPath}) {
    return AppConfig(
      apiBaseUrl: apiBaseUrl ?? this.apiBaseUrl,
      horizonPath: horizonPath ?? this.horizonPath,
    );
  }

  String horizonUrl(String baseOverride) {
    final base = baseOverride.replaceAll(RegExp(r'/+$'), '');
    final path =
        horizonPath.startsWith('/') ? horizonPath : '/$horizonPath';
    return '$base$path';
  }
}
