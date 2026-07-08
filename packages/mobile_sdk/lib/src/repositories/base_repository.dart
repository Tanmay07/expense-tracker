import '../api/api_client.dart';
import '../offline/cache_service.dart';
import '../offline/sync_service.dart';

abstract class BaseRepository {
  final ApiClient apiClient;
  final CacheService cacheService;
  final SyncService syncService;

  BaseRepository({
    required this.apiClient,
    required this.cacheService,
    required this.syncService,
  });

  /// Standard fetching with cache-first or network-first strategies.
  Future<dynamic> fetchWithStrategy(
    String endpoint, {
    required String cacheKey,
    bool forceNetwork = false,
  }) async {
    if (!forceNetwork) {
      final cached = await cacheService.getCache(cacheKey);
      if (cached != null) return cached;
    }

    try {
      final response = await apiClient.get(endpoint);
      if (response.statusCode == 200) {
        await cacheService.setCache(cacheKey, response.data, ttl: const Duration(minutes: 15));
        return response.data;
      }
    } catch (e) {
      // If network fails, attempt to fallback to stale cache
      return await cacheService.getCache(cacheKey);
    }
    return null;
  }

  /// Queues a mutation for offline syncing or immediate execution
  Future<void> mutateOfflineFirst(
    String entityType,
    String action,
    Map<String, dynamic> payload,
  ) async {
    await syncService.queueMutation(entityType, action, payload);
  }
}
