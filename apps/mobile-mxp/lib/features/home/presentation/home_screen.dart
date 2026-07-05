import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../services/api/bff_client.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final missionsAsync = ref.watch(missionsProvider);
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mission Control', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(icon: const Icon(Icons.notifications_outlined), onPressed: () {}),
          IconButton(icon: const Icon(Icons.person_outline), onPressed: () {}),
        ],
      ),
      body: RefreshIndicator(
        onRefresh: () => ref.refresh(missionsProvider.future),
        child: ListView(
          padding: const EdgeInsets.all(16.0),
          children: [
            _buildContextGreeting(theme),
            const SizedBox(height: 24),
            _buildQuickActions(theme),
            const SizedBox(height: 24),
            Text('Active Missions', style: theme.textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
            const SizedBox(height: 12),
            missionsAsync.when(
              data: (missions) => Column(
                children: missions.map((m) => _buildMissionCard(m, theme)).toList(),
              ),
              loading: () => const Center(child: CircularProgressIndicator()),
              error: (e, st) => Text('Error loading missions: $e', style: TextStyle(color: theme.colorScheme.error)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildContextGreeting(ThemeData theme) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Good afternoon, Tanmay', style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.w600)),
        const SizedBox(height: 4),
        Text('You have 2 high priority items requiring attention.', style: theme.textTheme.bodyMedium?.copyWith(color: theme.colorScheme.onSurfaceVariant)),
      ],
    );
  }

  Widget _buildQuickActions(ThemeData theme) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        _buildActionBtn(Icons.document_scanner, 'Scan Receipt', theme),
        _buildActionBtn(Icons.auto_awesome, 'Ask AI', theme),
        _buildActionBtn(Icons.add_card, 'Add Expense', theme),
        _buildActionBtn(Icons.insights, 'Analyze', theme),
      ],
    );
  }

  Widget _buildActionBtn(IconData icon, String label, ThemeData theme) {
    return Column(
      children: [
        CircleAvatar(
          radius: 28,
          backgroundColor: theme.colorScheme.primaryContainer,
          child: Icon(icon, color: theme.colorScheme.onPrimaryContainer),
        ),
        const SizedBox(height: 8),
        Text(label, style: theme.textTheme.labelMedium),
      ],
    );
  }

  Widget _buildMissionCard(MissionModel mission, ThemeData theme) {
    final isHigh = mission.priority == 'HIGH';
    return Card(
      elevation: 0,
      color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
      margin: const EdgeInsets.only(bottom: 12),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(color: isHigh ? theme.colorScheme.error : Colors.transparent, width: 1),
      ),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: isHigh ? theme.colorScheme.errorContainer : theme.colorScheme.secondaryContainer,
          child: Icon(
            isHigh ? Icons.warning_amber_rounded : Icons.check_circle_outline,
            color: isHigh ? theme.colorScheme.onErrorContainer : theme.colorScheme.onSecondaryContainer,
          ),
        ),
        title: Text(mission.title, style: const TextStyle(fontWeight: FontWeight.w600)),
        subtitle: Text(mission.type),
        trailing: const Icon(Icons.arrow_forward_ios, size: 16),
        onTap: () {},
      ),
    );
  }
}
