import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../features/shell/presentation/adaptive_shell.dart';
import '../../features/home/presentation/home_screen.dart';
import '../../features/workspaces/presentation/workspaces_screen.dart';

final rootNavigatorKey = GlobalKey<NavigatorState>();
final shellNavigatorKey = GlobalKey<NavigatorState>();

final appRouterProvider = Provider<GoRouter>((ref) {
  return GoRouter(
    navigatorKey: rootNavigatorKey,
    initialLocation: '/',
    routes: [
      ShellRoute(
        navigatorKey: shellNavigatorKey,
        builder: (context, state, child) {
          return AdaptiveShell(child: child);
        },
        routes: [
          GoRoute(
            path: '/',
            builder: (context, state) => const HomeScreen(),
          ),
          GoRoute(
            path: '/missions',
            builder: (context, state) => const Center(child: Text('Mission Center')),
          ),
          GoRoute(
            path: '/decisions',
            builder: (context, state) => const Center(child: Text('Decision Center')),
          ),
          GoRoute(
            path: '/ai',
            builder: (context, state) => const Center(child: Text('AI Copilot')),
          ),
          GoRoute(
            path: '/workspaces',
            builder: (context, state) => const WorkspacesScreen(),
          ),
        ],
      ),
    ],
  );
});
