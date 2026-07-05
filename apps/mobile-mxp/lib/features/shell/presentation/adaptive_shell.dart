import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

class AdaptiveShell extends StatelessWidget {
  final Widget child;

  const AdaptiveShell({super.key, required this.child});

  @override
  Widget build(BuildContext context) {
    // Determine layout based on screen width
    final isLargeScreen = MediaQuery.of(context).size.width >= 600;

    return Scaffold(
      body: isLargeScreen ? _buildNavRail(context) : child,
      bottomNavigationBar: isLargeScreen ? null : _buildBottomNav(context),
    );
  }

  Widget _buildNavRail(BuildContext context) {
    return Row(
      children: [
        NavigationRail(
          selectedIndex: _calculateSelectedIndex(context),
          onDestinationSelected: (index) => _onItemTapped(index, context),
          labelType: NavigationRailLabelType.all,
          destinations: const [
            NavigationRailDestination(
              icon: Icon(Icons.home_outlined),
              selectedIcon: Icon(Icons.home),
              label: Text('Home'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.track_changes_outlined),
              selectedIcon: Icon(Icons.track_changes),
              label: Text('Missions'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.auto_awesome_outlined),
              selectedIcon: Icon(Icons.auto_awesome),
              label: Text('AI'),
            ),
            NavigationRailDestination(
              icon: Icon(Icons.workspaces_outline),
              selectedIcon: Icon(Icons.workspaces),
              label: Text('Workspaces'),
            ),
          ],
        ),
        const VerticalDivider(thickness: 1, width: 1),
        Expanded(child: child),
      ],
    );
  }

  Widget _buildBottomNav(BuildContext context) {
    return NavigationBar(
      selectedIndex: _calculateSelectedIndex(context),
      onDestinationSelected: (index) => _onItemTapped(index, context),
      destinations: const [
        NavigationDestination(
          icon: Icon(Icons.home_outlined),
          selectedIcon: Icon(Icons.home),
          label: 'Home',
        ),
        NavigationDestination(
          icon: Icon(Icons.track_changes_outlined),
          selectedIcon: Icon(Icons.track_changes),
          label: 'Missions',
        ),
        NavigationDestination(
          icon: Icon(Icons.auto_awesome_outlined),
          selectedIcon: Icon(Icons.auto_awesome),
          label: 'AI',
        ),
        NavigationDestination(
          icon: Icon(Icons.workspaces_outline),
          selectedIcon: Icon(Icons.workspaces),
          label: 'Workspaces',
        ),
      ],
    );
  }

  static int _calculateSelectedIndex(BuildContext context) {
    final String location = GoRouterState.of(context).uri.path;
    if (location.startsWith('/missions')) return 1;
    if (location.startsWith('/ai')) return 2;
    if (location.startsWith('/workspaces')) return 3;
    return 0;
  }

  void _onItemTapped(int index, BuildContext context) {
    switch (index) {
      case 0:
        context.go('/');
        break;
      case 1:
        context.go('/missions');
        break;
      case 2:
        context.go('/ai');
        break;
      case 3:
        context.go('/workspaces');
        break;
    }
  }
}
