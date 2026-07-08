import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';
import '../offline/cache_service.dart';

final aiServiceProvider = Provider<AiService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final cacheService = ref.watch(cacheServiceProvider);
  return AiService(apiClient, cacheService);
});

class AiService {
  final ApiClient _apiClient;
  final CacheService _cacheService;

  AiService(this._apiClient, this._cacheService);

  /// Discovers available AI capabilities from the platform and caches them locally
  Future<List<String>> discoverCapabilities() async {
    try {
      final response = await _apiClient.get('/ai/capabilities');
      if (response.statusCode == 200 && response.data != null) {
        final List<String> capabilities = List<String>.from(response.data['capabilities'] ?? []);
        await _cacheService.setCache('ai_capabilities', capabilities, ttl: const Duration(hours: 24));
        return capabilities;
      }
    } catch (e) {
      // Fallback to cache if offline
      final cached = await _cacheService.getCache('ai_capabilities');
      if (cached != null) {
        return List<String>.from(cached);
      }
    }
    return [];
  }

  /// Sends a raw intent (voice transcript or text) to the AI platform
  Future<String> sendIntent(String intentText, {Map<String, dynamic>? context}) async {
    try {
      final payload = <String, dynamic>{'text': intentText};
      if (context != null) {
        payload['context'] = context;
      }

      final response = await _apiClient.post(
        '/ai/intent',
        data: payload,
      );

      if (response.statusCode == 200 && response.data != null) {
        return response.data['reply'] ?? 'Received and processed.';
      }
      return 'I received your request but encountered an unexpected response format.';
    } catch (e) {
      return 'I am currently unable to reach the AI core. Please check your connection.';
    }
  }

  /// Sends approval for an autonomous action
  Future<bool> approveAction(String actionId) async {
    try {
      final response = await _apiClient.post('/ai/actions/$actionId/approve');
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
