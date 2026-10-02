import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

import '../../core/app_scope.dart';
import '../../shared/widgets/disclaimer_banner.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  WebViewController? _controller;
  var _started = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_started) return;
    _started = true;
    final scope = AppScope.of(context);
    final url = scope.config.horizonUrl(scope.config.apiBaseUrl);
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(Uri.parse(url));
  }

  @override
  Widget build(BuildContext context) {
    final scope = AppScope.of(context);
    final url = scope.config.horizonUrl(scope.config.apiBaseUrl);
    return Scaffold(
      appBar: AppBar(title: const Text('Mapa')),
      body: Column(
        children: [
          const Padding(
            padding: EdgeInsets.all(12),
            child: DisclaimerBanner(),
          ),
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 12),
            child: Text('Horizon WebView: $url', style: Theme.of(context).textTheme.bodySmall),
          ),
          const SizedBox(height: 8),
          Expanded(
            child: _controller == null
                ? const Center(child: CircularProgressIndicator())
                : WebViewWidget(controller: _controller!),
          ),
        ],
      ),
    );
  }
}
