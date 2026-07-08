import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'core/router/app_router.dart';

import 'package:client_extension_framework/client_extension_framework.dart';
import 'extensions/mock_auth_extension.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Create a global Riverpod container
  final container = ProviderContainer();

  // Fetch the Extension Framework
  final framework = container.read(extensionFrameworkProvider);

  // Register plugins statically
  framework.registerExtension(MockAuthExtension());

  // Boot the framework (Topological sorting, sandbox initialization)
  await framework.boot();

  runApp(UncontrolledProviderScope(
    container: container,
    child: const MobileMXPApp(),
  ));
}

class MobileMXPApp extends ConsumerWidget {
  const MobileMXPApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final router = ref.watch(appRouterProvider);

    return MaterialApp.router(
      title: 'PFOS Mobile MXP',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.light,
        ),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      themeMode: ThemeMode.system,
      routerConfig: router,
    );
  }
}
