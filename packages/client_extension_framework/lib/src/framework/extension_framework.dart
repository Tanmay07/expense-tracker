// ignore_for_file: prefer_initializing_formals
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter/foundation.dart';
import '../sdk/base_extension.dart';
import '../services/extension_registry_service.dart';
import '../services/lifecycle_manager_service.dart';
import '../services/security_sandbox_service.dart';

final extensionFrameworkProvider = Provider<ExtensionFramework>((ref) {
  final registry = ref.watch(extensionRegistryServiceProvider);
  final lifecycle = ref.watch(lifecycleManagerServiceProvider);
  final sandbox = ref.watch(securitySandboxServiceProvider);
  
  return ExtensionFramework(
    registry: registry,
    lifecycle: lifecycle,
    sandbox: sandbox,
  );
});

class ExtensionFramework {
  final ExtensionRegistryService _registry;
  final LifecycleManagerService _lifecycle;
  final SecuritySandboxService _sandbox;

  bool _isInitialized = false;

  ExtensionFramework({
    required ExtensionRegistryService registry,
    required LifecycleManagerService lifecycle,
    required SecuritySandboxService sandbox,
  })  : _registry = registry,
        _lifecycle = lifecycle,
        _sandbox = sandbox;

  /// Registers an extension into the framework.
  /// Cannot be called after [boot] has been executed.
  void registerExtension(BaseExtension extension) {
    _registry.registerExtension(extension);
  }

  /// Boots the Extension Framework.
  /// This seals the registry, resolves the topological dependency graph,
  /// and initializes all extensions in the required order.
  Future<void> boot() async {
    if (_isInitialized) {
      debugPrint('ExtensionFramework is already initialized.');
      return;
    }

    debugPrint('Booting Extension Framework...');
    
    // 1. Seal registry and resolve dependencies
    final sortedExtensions = _registry.sealAndResolve();
    
    debugPrint('Successfully resolved dependency graph for ${sortedExtensions.length} extensions.');

    // 2. Initialize all extensions securely
    await _lifecycle.initializeExtensions(sortedExtensions);

    _isInitialized = true;
    debugPrint('Extension Framework booted successfully.');
  }

  /// Enables a specific extension by ID.
  Future<void> enableExtension(String id) async {
    final ext = _registry.getExtension(id);
    if (ext != null) {
      await _lifecycle.enableExtension(ext);
    } else {
      debugPrint('Warning: Attempted to enable unknown extension $id.');
    }
  }

  /// Disables a specific extension by ID.
  Future<void> disableExtension(String id) async {
    final ext = _registry.getExtension(id);
    if (ext != null) {
      await _lifecycle.disableExtension(ext);
    }
  }

  /// Invokes a capability securely through the sandbox.
  Future<dynamic> invokeCapability({
    required String targetExtensionId,
    required String capabilityId,
    required Map<String, dynamic> arguments,
    required BaseExtension caller,
  }) async {
    return _sandbox.invokeCapability(
      targetExtensionId: targetExtensionId,
      capabilityId: capabilityId,
      arguments: arguments,
      caller: caller,
    );
  }

  /// Returns the overall health map of all registered extensions.
  Future<Map<String, bool>> getHealthReport() async {
    final allExtensions = _registry.getAllExtensions();
    return _lifecycle.checkHealth(allExtensions);
  }
}
