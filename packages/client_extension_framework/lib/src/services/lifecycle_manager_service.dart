import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/foundation.dart';
import '../sdk/base_extension.dart';

final lifecycleManagerServiceProvider = Provider<LifecycleManagerService>((ref) {
  return LifecycleManagerService();
});

class LifecycleManagerService {
  /// Initializes a topologically sorted list of extensions safely.
  /// If one fails, it logs the error but allows others to continue.
  Future<void> initializeExtensions(List<BaseExtension> extensions) async {
    for (final ext in extensions) {
      try {
        debugPrint('Initializing extension: ${ext.metadata.id} (${ext.metadata.version})');
        await ext.onInitialize();
      } catch (e, stackTrace) {
        debugPrint('Failed to initialize extension ${ext.metadata.id}: $e');
        debugPrint(stackTrace.toString());
        // We log and continue so a bad extension doesn't kill the entire system
      }
    }
  }

  /// Enables a specific extension.
  Future<void> enableExtension(BaseExtension extension) async {
    try {
      debugPrint('Enabling extension: ${extension.metadata.id}');
      await extension.onEnable();
    } catch (e, stackTrace) {
      debugPrint('Failed to enable extension ${extension.metadata.id}: $e');
      debugPrint(stackTrace.toString());
      rethrow;
    }
  }

  /// Disables a specific extension safely.
  Future<void> disableExtension(BaseExtension extension) async {
    try {
      debugPrint('Disabling extension: ${extension.metadata.id}');
      await extension.onDisable();
    } catch (e, stackTrace) {
      debugPrint('Failed to disable extension ${extension.metadata.id}: $e');
      debugPrint(stackTrace.toString());
    }
  }

  /// Runs health checks on all provided extensions.
  /// Returns a map of Extension ID to Health Status boolean.
  Future<Map<String, bool>> checkHealth(List<BaseExtension> extensions) async {
    final healthReport = <String, bool>{};
    for (final ext in extensions) {
      try {
        final isHealthy = await ext.onHealthCheck();
        healthReport[ext.metadata.id] = isHealthy;
      } catch (e) {
        debugPrint('Health check failed for ${ext.metadata.id}: $e');
        healthReport[ext.metadata.id] = false;
      }
    }
    return healthReport;
  }
}
