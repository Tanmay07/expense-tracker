import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../services/api/bff_client.dart';
import '../../../shared/widgets/workspace_card.dart';

class WorkspacesScreen extends ConsumerWidget {
  const WorkspacesScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final workspacesAsync = ref.watch(workspacesProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Workspaces', style: TextStyle(fontWeight: FontWeight.bold)),
      ),
      body: workspacesAsync.when(
        data: (workspaces) {
          final screenWidth = MediaQuery.of(context).size.width;
          int crossAxisCount = 2;
          if (screenWidth >= 1200) {
            crossAxisCount = 6;
          } else if (screenWidth >= 800) {
            crossAxisCount = 4;
          } else if (screenWidth >= 600) {
            crossAxisCount = 3;
          }

          return GridView.builder(
            padding: const EdgeInsets.all(16.0),
            gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: crossAxisCount,
              crossAxisSpacing: 16,
              mainAxisSpacing: 16,
              childAspectRatio: 1.1,
            ),
            itemCount: workspaces.length,
            itemBuilder: (context, index) {
              final ws = workspaces[index];
              return WorkspaceCard(
                title: ws['name'] as String,
                icon: _getIconForString(ws['icon'] as String),
                onTap: () {
                  // In a real app we'd navigate to the detailed workspace route.
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(content: Text('Opening ${ws['name']} workspace...')),
                  );
                },
              );
            },
          );
        },
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, st) => Center(child: Text('Error loading workspaces: $e', style: TextStyle(color: theme.colorScheme.error))),
      ),
    );
  }

  IconData _getIconForString(String iconName) {
    switch (iconName) {
      case 'receipt':
        return Icons.receipt_long;
      case 'trending_up':
        return Icons.trending_up;
      case 'flag':
        return Icons.flag;
      default:
        return Icons.workspaces;
    }
  }
}
