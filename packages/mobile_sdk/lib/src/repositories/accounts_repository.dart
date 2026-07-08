import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';
import '../offline/cache_service.dart';
import '../offline/sync_service.dart';
import 'base_repository.dart';

final accountsRepositoryProvider = Provider<AccountsRepository>((ref) {
  return AccountsRepository(
    apiClient: ref.watch(apiClientProvider),
    cacheService: ref.watch(cacheServiceProvider),
    syncService: ref.watch(syncServiceProvider),
  );
});

class AccountsRepository extends BaseRepository {
  AccountsRepository({
    required super.apiClient,
    required super.cacheService,
    required super.syncService,
  });

  Future<List<dynamic>> getAccounts({bool forceNetwork = false}) async {
    final data = await fetchWithStrategy(
      '/accounts',
      cacheKey: 'accounts_list',
      forceNetwork: forceNetwork,
    );
    
    if (data != null && data is List) {
      return data;
    }
    return [];
  }

  Future<void> createAccount(Map<String, dynamic> accountData) async {
    // Queue mutation for offline-first architecture
    await mutateOfflineFirst('account', 'CREATE', accountData);
    
    // Invalidate local cache optimistically
    await cacheService.removeCache('accounts_list');
  }
}
