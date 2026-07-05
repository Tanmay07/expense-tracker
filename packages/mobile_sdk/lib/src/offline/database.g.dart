// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'database.dart';

// ignore_for_file: type=lint
class $OfflineMutationsTable extends OfflineMutations
    with TableInfo<$OfflineMutationsTable, OfflineMutation> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $OfflineMutationsTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _idMeta = const VerificationMeta('id');
  @override
  late final GeneratedColumn<int> id = GeneratedColumn<int>(
    'id',
    aliasedName,
    false,
    hasAutoIncrement: true,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
    defaultConstraints: GeneratedColumn.constraintIsAlways(
      'PRIMARY KEY AUTOINCREMENT',
    ),
  );
  static const VerificationMeta _entityTypeMeta = const VerificationMeta(
    'entityType',
  );
  @override
  late final GeneratedColumn<String> entityType = GeneratedColumn<String>(
    'entity_type',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _actionMeta = const VerificationMeta('action');
  @override
  late final GeneratedColumn<String> action = GeneratedColumn<String>(
    'action',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _payloadMeta = const VerificationMeta(
    'payload',
  );
  @override
  late final GeneratedColumn<String> payload = GeneratedColumn<String>(
    'payload',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _createdAtMeta = const VerificationMeta(
    'createdAt',
  );
  @override
  late final GeneratedColumn<DateTime> createdAt = GeneratedColumn<DateTime>(
    'created_at',
    aliasedName,
    false,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: false,
    defaultValue: currentDateAndTime,
  );
  static const VerificationMeta _retryCountMeta = const VerificationMeta(
    'retryCount',
  );
  @override
  late final GeneratedColumn<int> retryCount = GeneratedColumn<int>(
    'retry_count',
    aliasedName,
    false,
    type: DriftSqlType.int,
    requiredDuringInsert: false,
    defaultValue: const Constant(0),
  );
  @override
  List<GeneratedColumn> get $columns => [
    id,
    entityType,
    action,
    payload,
    createdAt,
    retryCount,
  ];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'offline_mutations';
  @override
  VerificationContext validateIntegrity(
    Insertable<OfflineMutation> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('id')) {
      context.handle(_idMeta, id.isAcceptableOrUnknown(data['id']!, _idMeta));
    }
    if (data.containsKey('entity_type')) {
      context.handle(
        _entityTypeMeta,
        entityType.isAcceptableOrUnknown(data['entity_type']!, _entityTypeMeta),
      );
    } else if (isInserting) {
      context.missing(_entityTypeMeta);
    }
    if (data.containsKey('action')) {
      context.handle(
        _actionMeta,
        action.isAcceptableOrUnknown(data['action']!, _actionMeta),
      );
    } else if (isInserting) {
      context.missing(_actionMeta);
    }
    if (data.containsKey('payload')) {
      context.handle(
        _payloadMeta,
        payload.isAcceptableOrUnknown(data['payload']!, _payloadMeta),
      );
    } else if (isInserting) {
      context.missing(_payloadMeta);
    }
    if (data.containsKey('created_at')) {
      context.handle(
        _createdAtMeta,
        createdAt.isAcceptableOrUnknown(data['created_at']!, _createdAtMeta),
      );
    }
    if (data.containsKey('retry_count')) {
      context.handle(
        _retryCountMeta,
        retryCount.isAcceptableOrUnknown(data['retry_count']!, _retryCountMeta),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {id};
  @override
  OfflineMutation map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return OfflineMutation(
      id: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}id'],
      )!,
      entityType: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}entity_type'],
      )!,
      action: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}action'],
      )!,
      payload: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}payload'],
      )!,
      createdAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}created_at'],
      )!,
      retryCount: attachedDatabase.typeMapping.read(
        DriftSqlType.int,
        data['${effectivePrefix}retry_count'],
      )!,
    );
  }

  @override
  $OfflineMutationsTable createAlias(String alias) {
    return $OfflineMutationsTable(attachedDatabase, alias);
  }
}

class OfflineMutation extends DataClass implements Insertable<OfflineMutation> {
  final int id;
  final String entityType;
  final String action;
  final String payload;
  final DateTime createdAt;
  final int retryCount;
  const OfflineMutation({
    required this.id,
    required this.entityType,
    required this.action,
    required this.payload,
    required this.createdAt,
    required this.retryCount,
  });
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['id'] = Variable<int>(id);
    map['entity_type'] = Variable<String>(entityType);
    map['action'] = Variable<String>(action);
    map['payload'] = Variable<String>(payload);
    map['created_at'] = Variable<DateTime>(createdAt);
    map['retry_count'] = Variable<int>(retryCount);
    return map;
  }

  OfflineMutationsCompanion toCompanion(bool nullToAbsent) {
    return OfflineMutationsCompanion(
      id: Value(id),
      entityType: Value(entityType),
      action: Value(action),
      payload: Value(payload),
      createdAt: Value(createdAt),
      retryCount: Value(retryCount),
    );
  }

  factory OfflineMutation.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return OfflineMutation(
      id: serializer.fromJson<int>(json['id']),
      entityType: serializer.fromJson<String>(json['entityType']),
      action: serializer.fromJson<String>(json['action']),
      payload: serializer.fromJson<String>(json['payload']),
      createdAt: serializer.fromJson<DateTime>(json['createdAt']),
      retryCount: serializer.fromJson<int>(json['retryCount']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'id': serializer.toJson<int>(id),
      'entityType': serializer.toJson<String>(entityType),
      'action': serializer.toJson<String>(action),
      'payload': serializer.toJson<String>(payload),
      'createdAt': serializer.toJson<DateTime>(createdAt),
      'retryCount': serializer.toJson<int>(retryCount),
    };
  }

  OfflineMutation copyWith({
    int? id,
    String? entityType,
    String? action,
    String? payload,
    DateTime? createdAt,
    int? retryCount,
  }) => OfflineMutation(
    id: id ?? this.id,
    entityType: entityType ?? this.entityType,
    action: action ?? this.action,
    payload: payload ?? this.payload,
    createdAt: createdAt ?? this.createdAt,
    retryCount: retryCount ?? this.retryCount,
  );
  OfflineMutation copyWithCompanion(OfflineMutationsCompanion data) {
    return OfflineMutation(
      id: data.id.present ? data.id.value : this.id,
      entityType: data.entityType.present
          ? data.entityType.value
          : this.entityType,
      action: data.action.present ? data.action.value : this.action,
      payload: data.payload.present ? data.payload.value : this.payload,
      createdAt: data.createdAt.present ? data.createdAt.value : this.createdAt,
      retryCount: data.retryCount.present
          ? data.retryCount.value
          : this.retryCount,
    );
  }

  @override
  String toString() {
    return (StringBuffer('OfflineMutation(')
          ..write('id: $id, ')
          ..write('entityType: $entityType, ')
          ..write('action: $action, ')
          ..write('payload: $payload, ')
          ..write('createdAt: $createdAt, ')
          ..write('retryCount: $retryCount')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode =>
      Object.hash(id, entityType, action, payload, createdAt, retryCount);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is OfflineMutation &&
          other.id == this.id &&
          other.entityType == this.entityType &&
          other.action == this.action &&
          other.payload == this.payload &&
          other.createdAt == this.createdAt &&
          other.retryCount == this.retryCount);
}

class OfflineMutationsCompanion extends UpdateCompanion<OfflineMutation> {
  final Value<int> id;
  final Value<String> entityType;
  final Value<String> action;
  final Value<String> payload;
  final Value<DateTime> createdAt;
  final Value<int> retryCount;
  const OfflineMutationsCompanion({
    this.id = const Value.absent(),
    this.entityType = const Value.absent(),
    this.action = const Value.absent(),
    this.payload = const Value.absent(),
    this.createdAt = const Value.absent(),
    this.retryCount = const Value.absent(),
  });
  OfflineMutationsCompanion.insert({
    this.id = const Value.absent(),
    required String entityType,
    required String action,
    required String payload,
    this.createdAt = const Value.absent(),
    this.retryCount = const Value.absent(),
  }) : entityType = Value(entityType),
       action = Value(action),
       payload = Value(payload);
  static Insertable<OfflineMutation> custom({
    Expression<int>? id,
    Expression<String>? entityType,
    Expression<String>? action,
    Expression<String>? payload,
    Expression<DateTime>? createdAt,
    Expression<int>? retryCount,
  }) {
    return RawValuesInsertable({
      if (id != null) 'id': id,
      if (entityType != null) 'entity_type': entityType,
      if (action != null) 'action': action,
      if (payload != null) 'payload': payload,
      if (createdAt != null) 'created_at': createdAt,
      if (retryCount != null) 'retry_count': retryCount,
    });
  }

  OfflineMutationsCompanion copyWith({
    Value<int>? id,
    Value<String>? entityType,
    Value<String>? action,
    Value<String>? payload,
    Value<DateTime>? createdAt,
    Value<int>? retryCount,
  }) {
    return OfflineMutationsCompanion(
      id: id ?? this.id,
      entityType: entityType ?? this.entityType,
      action: action ?? this.action,
      payload: payload ?? this.payload,
      createdAt: createdAt ?? this.createdAt,
      retryCount: retryCount ?? this.retryCount,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (id.present) {
      map['id'] = Variable<int>(id.value);
    }
    if (entityType.present) {
      map['entity_type'] = Variable<String>(entityType.value);
    }
    if (action.present) {
      map['action'] = Variable<String>(action.value);
    }
    if (payload.present) {
      map['payload'] = Variable<String>(payload.value);
    }
    if (createdAt.present) {
      map['created_at'] = Variable<DateTime>(createdAt.value);
    }
    if (retryCount.present) {
      map['retry_count'] = Variable<int>(retryCount.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('OfflineMutationsCompanion(')
          ..write('id: $id, ')
          ..write('entityType: $entityType, ')
          ..write('action: $action, ')
          ..write('payload: $payload, ')
          ..write('createdAt: $createdAt, ')
          ..write('retryCount: $retryCount')
          ..write(')'))
        .toString();
  }
}

class $CacheEntitiesTable extends CacheEntities
    with TableInfo<$CacheEntitiesTable, CacheEntity> {
  @override
  final GeneratedDatabase attachedDatabase;
  final String? _alias;
  $CacheEntitiesTable(this.attachedDatabase, [this._alias]);
  static const VerificationMeta _keyMeta = const VerificationMeta('key');
  @override
  late final GeneratedColumn<String> key = GeneratedColumn<String>(
    'key',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _valueMeta = const VerificationMeta('value');
  @override
  late final GeneratedColumn<String> value = GeneratedColumn<String>(
    'value',
    aliasedName,
    false,
    type: DriftSqlType.string,
    requiredDuringInsert: true,
  );
  static const VerificationMeta _expiresAtMeta = const VerificationMeta(
    'expiresAt',
  );
  @override
  late final GeneratedColumn<DateTime> expiresAt = GeneratedColumn<DateTime>(
    'expires_at',
    aliasedName,
    true,
    type: DriftSqlType.dateTime,
    requiredDuringInsert: false,
  );
  @override
  List<GeneratedColumn> get $columns => [key, value, expiresAt];
  @override
  String get aliasedName => _alias ?? actualTableName;
  @override
  String get actualTableName => $name;
  static const String $name = 'cache_entities';
  @override
  VerificationContext validateIntegrity(
    Insertable<CacheEntity> instance, {
    bool isInserting = false,
  }) {
    final context = VerificationContext();
    final data = instance.toColumns(true);
    if (data.containsKey('key')) {
      context.handle(
        _keyMeta,
        key.isAcceptableOrUnknown(data['key']!, _keyMeta),
      );
    } else if (isInserting) {
      context.missing(_keyMeta);
    }
    if (data.containsKey('value')) {
      context.handle(
        _valueMeta,
        value.isAcceptableOrUnknown(data['value']!, _valueMeta),
      );
    } else if (isInserting) {
      context.missing(_valueMeta);
    }
    if (data.containsKey('expires_at')) {
      context.handle(
        _expiresAtMeta,
        expiresAt.isAcceptableOrUnknown(data['expires_at']!, _expiresAtMeta),
      );
    }
    return context;
  }

  @override
  Set<GeneratedColumn> get $primaryKey => {key};
  @override
  CacheEntity map(Map<String, dynamic> data, {String? tablePrefix}) {
    final effectivePrefix = tablePrefix != null ? '$tablePrefix.' : '';
    return CacheEntity(
      key: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}key'],
      )!,
      value: attachedDatabase.typeMapping.read(
        DriftSqlType.string,
        data['${effectivePrefix}value'],
      )!,
      expiresAt: attachedDatabase.typeMapping.read(
        DriftSqlType.dateTime,
        data['${effectivePrefix}expires_at'],
      ),
    );
  }

  @override
  $CacheEntitiesTable createAlias(String alias) {
    return $CacheEntitiesTable(attachedDatabase, alias);
  }
}

class CacheEntity extends DataClass implements Insertable<CacheEntity> {
  final String key;
  final String value;
  final DateTime? expiresAt;
  const CacheEntity({required this.key, required this.value, this.expiresAt});
  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    map['key'] = Variable<String>(key);
    map['value'] = Variable<String>(value);
    if (!nullToAbsent || expiresAt != null) {
      map['expires_at'] = Variable<DateTime>(expiresAt);
    }
    return map;
  }

  CacheEntitiesCompanion toCompanion(bool nullToAbsent) {
    return CacheEntitiesCompanion(
      key: Value(key),
      value: Value(value),
      expiresAt: expiresAt == null && nullToAbsent
          ? const Value.absent()
          : Value(expiresAt),
    );
  }

  factory CacheEntity.fromJson(
    Map<String, dynamic> json, {
    ValueSerializer? serializer,
  }) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return CacheEntity(
      key: serializer.fromJson<String>(json['key']),
      value: serializer.fromJson<String>(json['value']),
      expiresAt: serializer.fromJson<DateTime?>(json['expiresAt']),
    );
  }
  @override
  Map<String, dynamic> toJson({ValueSerializer? serializer}) {
    serializer ??= driftRuntimeOptions.defaultSerializer;
    return <String, dynamic>{
      'key': serializer.toJson<String>(key),
      'value': serializer.toJson<String>(value),
      'expiresAt': serializer.toJson<DateTime?>(expiresAt),
    };
  }

  CacheEntity copyWith({
    String? key,
    String? value,
    Value<DateTime?> expiresAt = const Value.absent(),
  }) => CacheEntity(
    key: key ?? this.key,
    value: value ?? this.value,
    expiresAt: expiresAt.present ? expiresAt.value : this.expiresAt,
  );
  CacheEntity copyWithCompanion(CacheEntitiesCompanion data) {
    return CacheEntity(
      key: data.key.present ? data.key.value : this.key,
      value: data.value.present ? data.value.value : this.value,
      expiresAt: data.expiresAt.present ? data.expiresAt.value : this.expiresAt,
    );
  }

  @override
  String toString() {
    return (StringBuffer('CacheEntity(')
          ..write('key: $key, ')
          ..write('value: $value, ')
          ..write('expiresAt: $expiresAt')
          ..write(')'))
        .toString();
  }

  @override
  int get hashCode => Object.hash(key, value, expiresAt);
  @override
  bool operator ==(Object other) =>
      identical(this, other) ||
      (other is CacheEntity &&
          other.key == this.key &&
          other.value == this.value &&
          other.expiresAt == this.expiresAt);
}

class CacheEntitiesCompanion extends UpdateCompanion<CacheEntity> {
  final Value<String> key;
  final Value<String> value;
  final Value<DateTime?> expiresAt;
  final Value<int> rowid;
  const CacheEntitiesCompanion({
    this.key = const Value.absent(),
    this.value = const Value.absent(),
    this.expiresAt = const Value.absent(),
    this.rowid = const Value.absent(),
  });
  CacheEntitiesCompanion.insert({
    required String key,
    required String value,
    this.expiresAt = const Value.absent(),
    this.rowid = const Value.absent(),
  }) : key = Value(key),
       value = Value(value);
  static Insertable<CacheEntity> custom({
    Expression<String>? key,
    Expression<String>? value,
    Expression<DateTime>? expiresAt,
    Expression<int>? rowid,
  }) {
    return RawValuesInsertable({
      if (key != null) 'key': key,
      if (value != null) 'value': value,
      if (expiresAt != null) 'expires_at': expiresAt,
      if (rowid != null) 'rowid': rowid,
    });
  }

  CacheEntitiesCompanion copyWith({
    Value<String>? key,
    Value<String>? value,
    Value<DateTime?>? expiresAt,
    Value<int>? rowid,
  }) {
    return CacheEntitiesCompanion(
      key: key ?? this.key,
      value: value ?? this.value,
      expiresAt: expiresAt ?? this.expiresAt,
      rowid: rowid ?? this.rowid,
    );
  }

  @override
  Map<String, Expression> toColumns(bool nullToAbsent) {
    final map = <String, Expression>{};
    if (key.present) {
      map['key'] = Variable<String>(key.value);
    }
    if (value.present) {
      map['value'] = Variable<String>(value.value);
    }
    if (expiresAt.present) {
      map['expires_at'] = Variable<DateTime>(expiresAt.value);
    }
    if (rowid.present) {
      map['rowid'] = Variable<int>(rowid.value);
    }
    return map;
  }

  @override
  String toString() {
    return (StringBuffer('CacheEntitiesCompanion(')
          ..write('key: $key, ')
          ..write('value: $value, ')
          ..write('expiresAt: $expiresAt, ')
          ..write('rowid: $rowid')
          ..write(')'))
        .toString();
  }
}

abstract class _$SdkDatabase extends GeneratedDatabase {
  _$SdkDatabase(QueryExecutor e) : super(e);
  $SdkDatabaseManager get managers => $SdkDatabaseManager(this);
  late final $OfflineMutationsTable offlineMutations = $OfflineMutationsTable(
    this,
  );
  late final $CacheEntitiesTable cacheEntities = $CacheEntitiesTable(this);
  @override
  Iterable<TableInfo<Table, Object?>> get allTables =>
      allSchemaEntities.whereType<TableInfo<Table, Object?>>();
  @override
  List<DatabaseSchemaEntity> get allSchemaEntities => [
    offlineMutations,
    cacheEntities,
  ];
}

typedef $$OfflineMutationsTableCreateCompanionBuilder =
    OfflineMutationsCompanion Function({
      Value<int> id,
      required String entityType,
      required String action,
      required String payload,
      Value<DateTime> createdAt,
      Value<int> retryCount,
    });
typedef $$OfflineMutationsTableUpdateCompanionBuilder =
    OfflineMutationsCompanion Function({
      Value<int> id,
      Value<String> entityType,
      Value<String> action,
      Value<String> payload,
      Value<DateTime> createdAt,
      Value<int> retryCount,
    });

class $$OfflineMutationsTableFilterComposer
    extends Composer<_$SdkDatabase, $OfflineMutationsTable> {
  $$OfflineMutationsTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<int> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get entityType => $composableBuilder(
    column: $table.entityType,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get action => $composableBuilder(
    column: $table.action,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get payload => $composableBuilder(
    column: $table.payload,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get createdAt => $composableBuilder(
    column: $table.createdAt,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<int> get retryCount => $composableBuilder(
    column: $table.retryCount,
    builder: (column) => ColumnFilters(column),
  );
}

class $$OfflineMutationsTableOrderingComposer
    extends Composer<_$SdkDatabase, $OfflineMutationsTable> {
  $$OfflineMutationsTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<int> get id => $composableBuilder(
    column: $table.id,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get entityType => $composableBuilder(
    column: $table.entityType,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get action => $composableBuilder(
    column: $table.action,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get payload => $composableBuilder(
    column: $table.payload,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get createdAt => $composableBuilder(
    column: $table.createdAt,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<int> get retryCount => $composableBuilder(
    column: $table.retryCount,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$OfflineMutationsTableAnnotationComposer
    extends Composer<_$SdkDatabase, $OfflineMutationsTable> {
  $$OfflineMutationsTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<int> get id =>
      $composableBuilder(column: $table.id, builder: (column) => column);

  GeneratedColumn<String> get entityType => $composableBuilder(
    column: $table.entityType,
    builder: (column) => column,
  );

  GeneratedColumn<String> get action =>
      $composableBuilder(column: $table.action, builder: (column) => column);

  GeneratedColumn<String> get payload =>
      $composableBuilder(column: $table.payload, builder: (column) => column);

  GeneratedColumn<DateTime> get createdAt =>
      $composableBuilder(column: $table.createdAt, builder: (column) => column);

  GeneratedColumn<int> get retryCount => $composableBuilder(
    column: $table.retryCount,
    builder: (column) => column,
  );
}

class $$OfflineMutationsTableTableManager
    extends
        RootTableManager<
          _$SdkDatabase,
          $OfflineMutationsTable,
          OfflineMutation,
          $$OfflineMutationsTableFilterComposer,
          $$OfflineMutationsTableOrderingComposer,
          $$OfflineMutationsTableAnnotationComposer,
          $$OfflineMutationsTableCreateCompanionBuilder,
          $$OfflineMutationsTableUpdateCompanionBuilder,
          (
            OfflineMutation,
            BaseReferences<
              _$SdkDatabase,
              $OfflineMutationsTable,
              OfflineMutation
            >,
          ),
          OfflineMutation,
          PrefetchHooks Function()
        > {
  $$OfflineMutationsTableTableManager(
    _$SdkDatabase db,
    $OfflineMutationsTable table,
  ) : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$OfflineMutationsTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$OfflineMutationsTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$OfflineMutationsTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<int> id = const Value.absent(),
                Value<String> entityType = const Value.absent(),
                Value<String> action = const Value.absent(),
                Value<String> payload = const Value.absent(),
                Value<DateTime> createdAt = const Value.absent(),
                Value<int> retryCount = const Value.absent(),
              }) => OfflineMutationsCompanion(
                id: id,
                entityType: entityType,
                action: action,
                payload: payload,
                createdAt: createdAt,
                retryCount: retryCount,
              ),
          createCompanionCallback:
              ({
                Value<int> id = const Value.absent(),
                required String entityType,
                required String action,
                required String payload,
                Value<DateTime> createdAt = const Value.absent(),
                Value<int> retryCount = const Value.absent(),
              }) => OfflineMutationsCompanion.insert(
                id: id,
                entityType: entityType,
                action: action,
                payload: payload,
                createdAt: createdAt,
                retryCount: retryCount,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$OfflineMutationsTableProcessedTableManager =
    ProcessedTableManager<
      _$SdkDatabase,
      $OfflineMutationsTable,
      OfflineMutation,
      $$OfflineMutationsTableFilterComposer,
      $$OfflineMutationsTableOrderingComposer,
      $$OfflineMutationsTableAnnotationComposer,
      $$OfflineMutationsTableCreateCompanionBuilder,
      $$OfflineMutationsTableUpdateCompanionBuilder,
      (
        OfflineMutation,
        BaseReferences<_$SdkDatabase, $OfflineMutationsTable, OfflineMutation>,
      ),
      OfflineMutation,
      PrefetchHooks Function()
    >;
typedef $$CacheEntitiesTableCreateCompanionBuilder =
    CacheEntitiesCompanion Function({
      required String key,
      required String value,
      Value<DateTime?> expiresAt,
      Value<int> rowid,
    });
typedef $$CacheEntitiesTableUpdateCompanionBuilder =
    CacheEntitiesCompanion Function({
      Value<String> key,
      Value<String> value,
      Value<DateTime?> expiresAt,
      Value<int> rowid,
    });

class $$CacheEntitiesTableFilterComposer
    extends Composer<_$SdkDatabase, $CacheEntitiesTable> {
  $$CacheEntitiesTableFilterComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnFilters<String> get key => $composableBuilder(
    column: $table.key,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<String> get value => $composableBuilder(
    column: $table.value,
    builder: (column) => ColumnFilters(column),
  );

  ColumnFilters<DateTime> get expiresAt => $composableBuilder(
    column: $table.expiresAt,
    builder: (column) => ColumnFilters(column),
  );
}

class $$CacheEntitiesTableOrderingComposer
    extends Composer<_$SdkDatabase, $CacheEntitiesTable> {
  $$CacheEntitiesTableOrderingComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  ColumnOrderings<String> get key => $composableBuilder(
    column: $table.key,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<String> get value => $composableBuilder(
    column: $table.value,
    builder: (column) => ColumnOrderings(column),
  );

  ColumnOrderings<DateTime> get expiresAt => $composableBuilder(
    column: $table.expiresAt,
    builder: (column) => ColumnOrderings(column),
  );
}

class $$CacheEntitiesTableAnnotationComposer
    extends Composer<_$SdkDatabase, $CacheEntitiesTable> {
  $$CacheEntitiesTableAnnotationComposer({
    required super.$db,
    required super.$table,
    super.joinBuilder,
    super.$addJoinBuilderToRootComposer,
    super.$removeJoinBuilderFromRootComposer,
  });
  GeneratedColumn<String> get key =>
      $composableBuilder(column: $table.key, builder: (column) => column);

  GeneratedColumn<String> get value =>
      $composableBuilder(column: $table.value, builder: (column) => column);

  GeneratedColumn<DateTime> get expiresAt =>
      $composableBuilder(column: $table.expiresAt, builder: (column) => column);
}

class $$CacheEntitiesTableTableManager
    extends
        RootTableManager<
          _$SdkDatabase,
          $CacheEntitiesTable,
          CacheEntity,
          $$CacheEntitiesTableFilterComposer,
          $$CacheEntitiesTableOrderingComposer,
          $$CacheEntitiesTableAnnotationComposer,
          $$CacheEntitiesTableCreateCompanionBuilder,
          $$CacheEntitiesTableUpdateCompanionBuilder,
          (
            CacheEntity,
            BaseReferences<_$SdkDatabase, $CacheEntitiesTable, CacheEntity>,
          ),
          CacheEntity,
          PrefetchHooks Function()
        > {
  $$CacheEntitiesTableTableManager(_$SdkDatabase db, $CacheEntitiesTable table)
    : super(
        TableManagerState(
          db: db,
          table: table,
          createFilteringComposer: () =>
              $$CacheEntitiesTableFilterComposer($db: db, $table: table),
          createOrderingComposer: () =>
              $$CacheEntitiesTableOrderingComposer($db: db, $table: table),
          createComputedFieldComposer: () =>
              $$CacheEntitiesTableAnnotationComposer($db: db, $table: table),
          updateCompanionCallback:
              ({
                Value<String> key = const Value.absent(),
                Value<String> value = const Value.absent(),
                Value<DateTime?> expiresAt = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => CacheEntitiesCompanion(
                key: key,
                value: value,
                expiresAt: expiresAt,
                rowid: rowid,
              ),
          createCompanionCallback:
              ({
                required String key,
                required String value,
                Value<DateTime?> expiresAt = const Value.absent(),
                Value<int> rowid = const Value.absent(),
              }) => CacheEntitiesCompanion.insert(
                key: key,
                value: value,
                expiresAt: expiresAt,
                rowid: rowid,
              ),
          withReferenceMapper: (p0) => p0
              .map((e) => (e.readTable(table), BaseReferences(db, table, e)))
              .toList(),
          prefetchHooksCallback: null,
        ),
      );
}

typedef $$CacheEntitiesTableProcessedTableManager =
    ProcessedTableManager<
      _$SdkDatabase,
      $CacheEntitiesTable,
      CacheEntity,
      $$CacheEntitiesTableFilterComposer,
      $$CacheEntitiesTableOrderingComposer,
      $$CacheEntitiesTableAnnotationComposer,
      $$CacheEntitiesTableCreateCompanionBuilder,
      $$CacheEntitiesTableUpdateCompanionBuilder,
      (
        CacheEntity,
        BaseReferences<_$SdkDatabase, $CacheEntitiesTable, CacheEntity>,
      ),
      CacheEntity,
      PrefetchHooks Function()
    >;

class $SdkDatabaseManager {
  final _$SdkDatabase _db;
  $SdkDatabaseManager(this._db);
  $$OfflineMutationsTableTableManager get offlineMutations =>
      $$OfflineMutationsTableTableManager(_db, _db.offlineMutations);
  $$CacheEntitiesTableTableManager get cacheEntities =>
      $$CacheEntitiesTableTableManager(_db, _db.cacheEntities);
}
