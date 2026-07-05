import 'dart:convert';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:drift/drift.dart';
import 'database.dart';

final cacheServiceProvider = Provider<CacheService>((ref) {
  final db = SdkDatabase(); // In a real app we might want this as a singleton provider
  return CacheService(db);
});

class CacheService {
  final SdkDatabase _db;

  CacheService(this._db);

  Future<void> setCache(String key, dynamic value, {Duration? ttl}) async {
    final expiresAt = ttl != null ? DateTime.now().add(ttl) : null;
    
    await _db.into(_db.cacheEntities).insertOnConflictUpdate(
      CacheEntitiesCompanion(
        key: Value(key),
        value: Value(jsonEncode(value)),
        expiresAt: Value(expiresAt),
      )
    );
  }

  Future<dynamic> getCache(String key) async {
    final cacheEntity = await (_db.select(_db.cacheEntities)
          ..where((tbl) => tbl.key.equals(key)))
        .getSingleOrNull();

    if (cacheEntity == null) return null;

    if (cacheEntity.expiresAt != null && DateTime.now().isAfter(cacheEntity.expiresAt!)) {
      await removeCache(key);
      return null;
    }

    return jsonDecode(cacheEntity.value);
  }

  Future<void> removeCache(String key) async {
    await (_db.delete(_db.cacheEntities)..where((tbl) => tbl.key.equals(key))).go();
  }

  Future<void> clearAll() async {
    await _db.delete(_db.cacheEntities).go();
  }
}
