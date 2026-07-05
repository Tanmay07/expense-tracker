import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:drift/drift.dart';
import '../api/api_client.dart';
import 'database.dart';

final syncServiceProvider = Provider<SyncService>((ref) {
  final db = SdkDatabase();
  final apiClient = ref.watch(apiClientProvider);
  return SyncService(db, apiClient);
});

class SyncService {
  final SdkDatabase _db;
  final ApiClient _apiClient;
  bool _isSyncing = false;

  SyncService(this._db, this._apiClient);

  Future<void> queueMutation(String entityType, String action, Map<String, dynamic> payload) async {
    await _db.into(_db.offlineMutations).insert(
      OfflineMutationsCompanion(
        entityType: Value(entityType),
        action: Value(action),
        payload: Value(jsonEncode(payload)),
      ),
    );
    
    // Attempt opportunistic sync if online
    _triggerBackgroundSync();
  }

  Future<void> _triggerBackgroundSync() async {
    if (_isSyncing) return;
    _isSyncing = true;

    try {
      final pendingMutations = await (_db.select(_db.offlineMutations)
            ..orderBy([(t) => OrderingTerm.asc(t.createdAt)])
            ..limit(50)) // Process in batches
          .get();

      for (final mutation in pendingMutations) {
        bool success = await _pushMutationToBff(mutation);
        
        if (success) {
          // Remove successful mutation from queue
          await (_db.delete(_db.offlineMutations)..where((tbl) => tbl.id.equals(mutation.id))).go();
        } else {
          // Increment retry count or handle dead-letter queue logic
          await (_db.update(_db.offlineMutations)..where((tbl) => tbl.id.equals(mutation.id))).write(
            OfflineMutationsCompanion(
              retryCount: Value(mutation.retryCount + 1),
            ),
          );
        }
      }
    } finally {
      _isSyncing = false;
    }
  }

  Future<bool> _pushMutationToBff(OfflineMutation mutation) async {
    try {
      final payloadData = jsonDecode(mutation.payload);
      
      // Push to BFF
      final response = await _apiClient.post('/sync/mutations', data: payloadData);
      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }
}
