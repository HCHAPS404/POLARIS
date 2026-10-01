import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:horizon_mobile/main.dart';
import 'package:horizon_mobile/services/polaris_api.dart';

void main() {
  testWidgets('shows decision-support disclaimer', (tester) async {
    await tester.pumpWidget(
      MaterialApp(
        home: HorizonHomeScreen(api: PolarisApi(baseUrl: 'http://127.0.0.1:1')),
      ),
    );
    expect(find.textContaining('Solo apoyo a la decisión'), findsOneWidget);
    expect(find.textContaining('DRAFT'), findsOneWidget);
  });
}
