import 'package:flutter/material.dart';

import '../../shared/widgets/disclaimer_banner.dart';

/// Stub for future preparedness checklists (not wired to API).
class PreparednessScreen extends StatelessWidget {
  const PreparednessScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Preparación')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: const [
          DisclaimerBanner(),
          SizedBox(height: 16),
          Text('PLACEHOLDER: listas de preparación por amenaza y sitio.'),
          SizedBox(height: 8),
          Text('Evidence: NOT IMPLEMENTED — navegación stub para arquitectura limpia.'),
        ],
      ),
    );
  }
}
