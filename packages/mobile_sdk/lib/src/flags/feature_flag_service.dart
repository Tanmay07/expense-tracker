import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';
import '../offline/cache_service.dart';

final featureFlagServiceProvider = Provider<FeatureFlagService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final cacheService = ref.watch(cacheServiceProvider);
  return FeatureFlagService(apiClient, cacheService);
});

class FeatureFlagService {
  final ApiClient _apiClient;
  final CacheService _cacheService;
  static const String _flagsCacheKey = 'feature_flags_cache';

  FeatureFlagService(this._apiClient, this._cacheService);

  Future<void> fetchAndCacheFlags() async {
    try {
      final response = await _apiClient.get('/flags');
      if (response.statusCode == 200) {
        await _cacheService.setCache(_flagsCacheKey, response.data, ttl: const Duration(hours: 24));
      }
    } catch (e) {
      // Silently fail and fallback to cache
    }
  }

  Future<bool> isFeatureEnabled(String featureKey, {bool defaultValue = false}) async {
    final cachedFlags = await _cacheService.getCache(_flagsCacheKey);
    if (cachedFlags != null && cachedFlags is Map) {
      if (cachedFlags.containsKey(featureKey)) {
        return cachedFlags[featureKey] == true;
      }
    }
    return defaultValue;
  }
}
