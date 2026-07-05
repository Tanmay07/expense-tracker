
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:mobile_mxp/main.dart';

void main() {
  testWidgets('App loads home screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const ProviderScope(child: MobileMXPApp()));
    await tester.pumpAndSettle();

    // Verify that the home screen is displayed.
    expect(find.text('Mission Control'), findsOneWidget);
    expect(find.text('Welcome to MXP'), findsOneWidget);
  });
}
