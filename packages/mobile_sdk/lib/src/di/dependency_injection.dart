import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';

// SDK Core Provider
final enterpriseSdkProvider = Provider<EnterpriseSdk>((ref) {
  return EnterpriseSdk(ref);
});

// The EnterpriseSdk facade orchestrates the initialization and exposes services
class EnterpriseSdk {
  final Ref _ref;
  bool _isInitialized = false;

  EnterpriseSdk(this._ref);

  Future<void> initialize() async {
    if (_isInitialized) return;
    
    // Initialize required internal services (e.g. database, secure storage) here
    // before allowing the UI to query repositories.
    
    _isInitialized = true;
  }

  // Example of exposing the API client directly for testing/internal use (though repositories are preferred)
  ApiClient get apiClient => _ref.read(apiClientProvider);

  bool get isInitialized => _isInitialized;
}
