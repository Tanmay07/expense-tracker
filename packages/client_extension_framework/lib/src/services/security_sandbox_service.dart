import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../sdk/base_extension.dart';
import 'extension_registry_service.dart';

final securitySandboxServiceProvider = Provider<SecuritySandboxService>((ref) {
  final registry = ref.watch(extensionRegistryServiceProvider);
  return SecuritySandboxService(registry);
});

class SecuritySandboxService {
  final ExtensionRegistryService _registry;

  SecuritySandboxService(this._registry);

  /// Securely invokes a capability on a target extension on behalf of a caller extension.
  /// Validates that the caller has explicitly declared the target capability in its permissions.
  Future<dynamic> invokeCapability({
    required String targetExtensionId,
    required String capabilityId,
    required Map<String, dynamic> arguments,
    required BaseExtension caller,
  }) async {
    // 1. Same-extension invocation is always permitted
    if (caller.metadata.id != targetExtensionId) {
      // 2. Cross-extension invocation requires explicit permission
      final requiredPermission = '$targetExtensionId:$capabilityId';
      if (!caller.metadata.permissions.contains(requiredPermission) && 
          !caller.metadata.permissions.contains('$targetExtensionId:*')) {
        throw SecurityException(
          'Security Sandbox Violation: Extension ${caller.metadata.id} '
          'attempted to invoke $targetExtensionId:$capabilityId without requesting permission.'
        );
      }
    }

    // 3. Retrieve target extension
    final targetExtension = _registry.getExtension(targetExtensionId);
    if (targetExtension == null) {
      throw StateError('Sandbox Error: Target extension $targetExtensionId is not registered.');
    }

    if (targetExtension is! BasePlugin) {
      throw StateError('Sandbox Error: Target extension $targetExtensionId does not expose capabilities.');
    }

    // 4. Find the requested capability
    final capability = targetExtension.capabilities.firstWhere(
      (cap) => cap.id == capabilityId,
      orElse: () => throw StateError('Sandbox Error: Capability $capabilityId not found on $targetExtensionId.'),
    );

    // 5. Execute within a secure boundary
    try {
      return await capability.execute(arguments);
    } catch (e) {
      throw Exception('Capability execution failed ($targetExtensionId:$capabilityId): $e');
    }
  }
}

class SecurityException implements Exception {
  final String message;
  SecurityException(this.message);

  @override
  String toString() => 'SecurityException: $message';
}
