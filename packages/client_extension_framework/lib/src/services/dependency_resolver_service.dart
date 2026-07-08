import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:pub_semver/pub_semver.dart';
import '../sdk/base_extension.dart';

final dependencyResolverServiceProvider = Provider<DependencyResolverService>((ref) {
  return DependencyResolverService();
});

class DependencyResolverService {
  /// Resolves the plugin dependency graph and returns a topologically sorted list of plugins.
  /// Throws an exception if dependencies are unmet or a cycle is detected.
  List<BaseExtension> resolveDependencies(List<BaseExtension> plugins) {
    final availablePlugins = {
      for (var plugin in plugins) plugin.metadata.id: plugin
    };

    final Map<String, List<String>> graph = {};
    final Map<String, int> inDegree = {};

    // Initialize graph
    for (var plugin in plugins) {
      graph[plugin.metadata.id] = [];
      inDegree[plugin.metadata.id] = 0;
    }

    // Build graph and check versions
    for (var plugin in plugins) {
      for (var depString in plugin.metadata.dependencies) {
        // Simple parsing: "plugin_id@^1.0.0"
        final parts = depString.split('@');
        final depId = parts[0];
        final versionConstraint = parts.length > 1 ? VersionConstraint.parse(parts[1]) : VersionConstraint.any;

        if (!availablePlugins.containsKey(depId)) {
          throw Exception('Unmet dependency: ${plugin.metadata.id} requires $depId');
        }

        final targetPlugin = availablePlugins[depId]!;
        final targetVersion = Version.parse(targetPlugin.metadata.version);

        if (!versionConstraint.allows(targetVersion)) {
          throw Exception('Version mismatch: ${plugin.metadata.id} requires $depId@$versionConstraint but found ${targetPlugin.metadata.version}');
        }

        graph[depId]!.add(plugin.metadata.id);
        inDegree[plugin.metadata.id] = inDegree[plugin.metadata.id]! + 1;
      }
    }

    // Kahn's Algorithm for Topological Sort
    final queue = <String>[];
    for (var pluginId in inDegree.keys) {
      if (inDegree[pluginId] == 0) {
        queue.add(pluginId);
      }
    }

    final sortedPlugins = <BaseExtension>[];
    while (queue.isNotEmpty) {
      final currentId = queue.removeAt(0);
      sortedPlugins.add(availablePlugins[currentId]!);

      for (var neighbor in graph[currentId]!) {
        inDegree[neighbor] = inDegree[neighbor]! - 1;
        if (inDegree[neighbor] == 0) {
          queue.add(neighbor);
        }
      }
    }

    if (sortedPlugins.length != plugins.length) {
      throw Exception('Circular dependency detected in plugins graph');
    }

    return sortedPlugins;
  }
}
