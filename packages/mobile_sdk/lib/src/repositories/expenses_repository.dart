import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';
import '../offline/cache_service.dart';
import '../offline/sync_service.dart';
import 'base_repository.dart';

final expensesRepositoryProvider = Provider<ExpensesRepository>((ref) {
  return ExpensesRepository(
    apiClient: ref.watch(apiClientProvider),
    cacheService: ref.watch(cacheServiceProvider),
    syncService: ref.watch(syncServiceProvider),
  );
});

class ExpensesRepository extends BaseRepository {
  ExpensesRepository({
    required super.apiClient,
    required super.cacheService,
    required super.syncService,
  });

  Future<List<dynamic>> getExpenses({bool forceNetwork = false}) async {
    final data = await fetchWithStrategy(
      '/expenses',
      cacheKey: 'expenses_list',
      forceNetwork: forceNetwork,
    );
    
    if (data != null && data is List) {
      return data;
    }
    return [];
  }

  Future<void> createExpense(Map<String, dynamic> expenseData) async {
    // Queue mutation for offline-first architecture
    await mutateOfflineFirst('expense', 'CREATE', expenseData);
    
    // Invalidate local cache optimistically
    await cacheService.removeCache('expenses_list');
  }
}
