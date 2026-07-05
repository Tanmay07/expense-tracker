import 'dart:io';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'database.g.dart';

@DataClassName('OfflineMutation')
class OfflineMutations extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get entityType => text()();
  TextColumn get action => text()(); // CREATE, UPDATE, DELETE
  TextColumn get payload => text()(); // JSON string
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
  IntColumn get retryCount => integer().withDefault(const Constant(0))();
}

@DataClassName('CacheEntity')
class CacheEntities extends Table {
  TextColumn get key => text()();
  TextColumn get value => text()(); // JSON string
  DateTimeColumn get expiresAt => dateTime().nullable()();

  @override
  Set<Column> get primaryKey => {key};
}

@DriftDatabase(tables: [OfflineMutations, CacheEntities])
class SdkDatabase extends _$SdkDatabase {
  SdkDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'enterprise_sdk.sqlite'));
    return NativeDatabase.createInBackground(file);
  });
}
