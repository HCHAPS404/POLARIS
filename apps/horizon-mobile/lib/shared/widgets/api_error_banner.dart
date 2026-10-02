import 'package:flutter/material.dart';

class ApiErrorBanner extends StatelessWidget {
  const ApiErrorBanner({super.key, required this.message, this.staleHint});

  final String message;
  final String? staleHint;

  @override
  Widget build(BuildContext context) {
    return Material(
      color: Theme.of(context).colorScheme.errorContainer,
      borderRadius: BorderRadius.circular(8),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Error de API o datos obsoletos',
              style: Theme.of(context).textTheme.titleSmall,
            ),
            const SizedBox(height: 4),
            Text(message, style: TextStyle(color: Theme.of(context).colorScheme.error)),
            if (staleHint != null) ...[
              const SizedBox(height: 4),
              Text(staleHint!, style: Theme.of(context).textTheme.bodySmall),
            ],
          ],
        ),
      ),
    );
  }
}
