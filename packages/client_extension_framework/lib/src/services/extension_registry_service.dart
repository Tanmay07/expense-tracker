import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../sdk/base_extension.dart';
import 'dependency_resolver_service.dart';

final extensionRegistryServiceProvider = Provider<ExtensionRegistryService>((ref) {
  final resolver = ref.watch(dependencyResolverServiceProvider);
  return ExtensionRegistryService(resolver);
});

class ExtensionRegistryService {
  final DependencyResolverService _dependencyResolver;
  
  final Map<String, BaseExtension> _registeredExtensions = {};
  bool _isSealed = false;

  ExtensionRegistryService(this._dependencyResolver);

  /// Registers an extension into the staging area.
  /// Throws if the registry is already sealed.
  void registerExtension(BaseExtension extension) {
    if (_isSealed) {
      throw StateError('Cannot register extensions after the registry is sealed.');
    }
    if (_registeredExtensions.containsKey(extension.metadata.id)) {
      throw ArgumentError('Extension with ID ${extension.metadata.id} is already registered.');
    }
    
    _registeredExtensions[extension.metadata.id] = extension;
  }

  /// Seals the registry, resolves dependencies, and returns the strictly ordered list
  /// of plugins for safe initialization.
  List<BaseExtension> sealAndResolve() {
    if (_isSealed) {
      throw StateError('Registry is already sealed.');
    }

    _isSealed = true;
    final allExtensions = _registeredExtensions.values.toList();
    
    // Resolve and sort dependencies (throws if invalid)
    return _dependencyResolver.resolveDependencies(allExtensions);
  }

  /// Returns a registered extension by ID.
  BaseExtension? getExtension(String id) {
    return _registeredExtensions[id];
  }

  /// Returns all registered extensions
  List<BaseExtension> getAllExtensions() {
    return _registeredExtensions.values.toList();
  }
}
