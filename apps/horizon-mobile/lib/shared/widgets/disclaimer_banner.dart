import 'package:flutter/material.dart';

class DisclaimerBanner extends StatelessWidget {
  const DisclaimerBanner({super.key});

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
