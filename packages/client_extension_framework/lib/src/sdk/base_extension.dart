import '../models/extension_metadata.dart';
import 'capability.dart';

abstract class BaseExtension {
  ExtensionMetadata get metadata;
  
  /// Triggered when the extension is first registered
  Future<void> onInstall() async {}

  /// Triggered to initialize internal state, connect to DBs, etc.
  Future<void> onInitialize() async {}

  /// Hook to apply dynamic configurations
  Future<void> onConfigure(Map<String, dynamic> config) async {}

  /// Triggered when the extension is enabled by the user or admin
  Future<void> onEnable() async {}

  /// Triggered when the extension is disabled
  Future<void> onDisable() async {}

  /// Returns true if the extension is healthy
  Future<bool> onHealthCheck() async {
    return true;
  }

  /// Hook for cleanup during app shutdown or uninstall
  Future<void> onShutdown() async {}
}

abstract class BasePlugin extends BaseExtension {
  /// Plugins can dynamically expose capabilities to the host framework
  List<Capability> get capabilities;
}
