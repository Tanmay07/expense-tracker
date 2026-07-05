import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';
import 'package:drift/drift.dart' as drift;
import '../core/database/database.dart';

final syncServiceProvider = Provider<SyncService>((ref) {
  // Provide a dummy Dio for now. In a real app, this comes from a network provider
  return SyncService(AppDatabase(), Dio());
});

class SyncService {
  final AppDatabase _db;
  final Dio _apiClient;

  SyncService(this._db, this._apiClient);

  Future<void> queueMutation(String endpoint, String method, String payload) async {
    await _db.into(_db.offlineMutations).insert(
      OfflineMutationsCompanion.insert(
        endpoint: endpoint,
        method: method,
        payloadJson: payload,
      ),
    );
    // Attempt sync immediately
    _attemptSync();
  }

  Future<void> _attemptSync() async {
    // Basic background sync loop implementation
    final pending = await _db.select(_db.offlineMutations).get();

    for (final mutation in pending) {
      try {
        final response = await _apiClient.request(
          mutation.endpoint,
          data: mutation.payloadJson,
          options: Options(method: mutation.method),
        );

        if (response.statusCode != null && response.statusCode! >= 200 && response.statusCode! < 300) {
          // Success, remove from queue
          await (_db.delete(_db.offlineMutations)..where((t) => t.id.equals(mutation.id))).go();
        } else {
          // Fail, increment retry
          await _incrementRetry(mutation);
        }
      } catch (e) {
        // Network error, increment retry
        await _incrementRetry(mutation);
      }
    }
  }

  Future<void> _incrementRetry(OfflineMutation mutation) async {
    if (mutation.retryCount >= 5) {
      // Move to dead letter queue or drop
      await (_db.delete(_db.offlineMutations)..where((t) => t.id.equals(mutation.id))).go();
    } else {
      await (_db.update(_db.offlineMutations)..where((t) => t.id.equals(mutation.id))).write(
        OfflineMutationsCompanion(
          retryCount: drift.Value(mutation.retryCount + 1),
        ),
      );
    }
  }
}
