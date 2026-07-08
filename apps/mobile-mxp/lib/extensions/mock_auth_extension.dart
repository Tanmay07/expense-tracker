import 'package:client_extension_framework/client_extension_framework.dart';
import 'package:flutter/foundation.dart';

class MockAuthExtension extends BasePlugin {
  @override
  final ExtensionMetadata metadata = const ExtensionMetadata(
    id: 'com.financeos.mockauth',
    name: 'Mock Authentication Provider',
    description: 'Provides mock authentication for development environments',
    version: '1.0.0',
    author: 'FinanceOS Core Team',
    category: ExtensionCategory.auth,
    permissions: [],
    minSdkVersion: '^1.0.0',
    minPlatformVersion: '^1.0.0',
  );

  @override
  final List<Capability> capabilities = [];

  MockAuthExtension() {
    capabilities.add(MockLoginCapability());
  }

  @override
  Future<void> onInitialize() async {
    debugPrint('MockAuthExtension: onInitialize() called.');
    // Simulate some async initialization
    await Future.delayed(const Duration(milliseconds: 500));
    debugPrint('MockAuthExtension: Initialized successfully.');
  }

  @override
  Future<void> onEnable() async {
    debugPrint('MockAuthExtension: Enabled');
  }

  @override
  Future<void> onDisable() async {
    debugPrint('MockAuthExtension: Disabled');
  }
}

class MockLoginCapability extends Capability {
  @override
  String get id => 'login';

  @override
  String get description => 'Logs in a user with mock credentials';

  @override
  Map<String, dynamic> get inputSchema => {
    'type': 'object',
    'properties': {
      'username': {'type': 'string'},
      'password': {'type': 'string'}
    }
  };

  @override
  Map<String, dynamic> get outputSchema => {
    'type': 'object',
    'properties': {
      'status': {'type': 'string'},
      'token': {'type': 'string'},
      'userId': {'type': 'string'}
    }
  };

  @override
  Future<Map<String, dynamic>> execute(Map<String, dynamic> arguments) async {
    final username = arguments['username'] as String?;
    final password = arguments['password'] as String?;

    debugPrint('MockLoginCapability executing for user: $username');
    await Future.delayed(const Duration(seconds: 1)); // Simulate network

    if (username == 'admin' && password == 'admin') {
      return {
        'status': 'success',
        'token': 'mock-jwt-token-12345',
        'userId': 'usr_mock_999'
      };
    } else {
      throw Exception('Invalid mock credentials');
    }
  }
}
