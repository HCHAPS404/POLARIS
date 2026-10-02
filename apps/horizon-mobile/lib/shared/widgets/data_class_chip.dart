import 'package:flutter/material.dart';

import '../models/data_class_badge.dart';

class DataClassChip extends StatelessWidget {
  const DataClassChip({super.key, required this.dataClass});

  final String dataClass;

  @override
  Widget build(BuildContext context) {
    final badge = DataClassBadge.parse(dataClass);
    final color = switch (badge) {
      DataClassBadge.liveIntegrated => Colors.green.shade800,
      DataClassBadge.historicalReplay => Colors.deepPurple,
      DataClassBadge.simulated => Colors.blueGrey,
      DataClassBadge.unknown => Colors.grey,
    };
    return Chip(
      label: Text(badge.shortLabel),
      backgroundColor: color.withOpacity(0.15),
      side: BorderSide(color: color),
      visualDensity: VisualDensity.compact,
    );
  }
}
