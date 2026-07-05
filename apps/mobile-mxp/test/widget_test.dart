import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'package:mobile_mxp/main.dart';

void main() {
  testWidgets('App loads home screen', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const ProviderScope(child: MobileMXPApp()));
    
    // Wait for the async riverpod providers to resolve (delayed missions loading)
    await tester.pumpAndSettle();

    // Verify that our app bar title is present
    expect(find.text('Mission Control'), findsWidgets);
  });
}
