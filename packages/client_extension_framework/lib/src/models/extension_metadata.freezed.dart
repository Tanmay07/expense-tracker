// GENERATED CODE - DO NOT MODIFY BY HAND
// coverage:ignore-file
// ignore_for_file: type=lint
// ignore_for_file: unused_element, deprecated_member_use, deprecated_member_use_from_same_package, use_function_type_syntax_for_parameters, unnecessary_const, avoid_init_to_null, invalid_override_different_default_values_named, prefer_expression_function_bodies, annotate_overrides, invalid_annotation_target, unnecessary_question_mark

part of 'extension_metadata.dart';

// **************************************************************************
// FreezedGenerator
// **************************************************************************

// dart format off
T _$identity<T>(T value) => value;

/// @nodoc
mixin _$ExtensionMetadata {

 String get id; String get name; String get description; String get version; String get author; ExtensionCategory get category; List<String> get dependencies; List<String> get permissions; Map<String, bool> get featureFlags; Map<String, dynamic> get configurationSchema; String get minSdkVersion; String get minPlatformVersion;
/// Create a copy of ExtensionMetadata
/// with the given fields replaced by the non-null parameter values.
@JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
$ExtensionMetadataCopyWith<ExtensionMetadata> get copyWith => _$ExtensionMetadataCopyWithImpl<ExtensionMetadata>(this as ExtensionMetadata, _$identity);

  /// Serializes this ExtensionMetadata to a JSON map.
  Map<String, dynamic> toJson();


@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is ExtensionMetadata&&(identical(other.id, id) || other.id == id)&&(identical(other.name, name) || other.name == name)&&(identical(other.description, description) || other.description == description)&&(identical(other.version, version) || other.version == version)&&(identical(other.author, author) || other.author == author)&&(identical(other.category, category) || other.category == category)&&const DeepCollectionEquality().equals(other.dependencies, dependencies)&&const DeepCollectionEquality().equals(other.permissions, permissions)&&const DeepCollectionEquality().equals(other.featureFlags, featureFlags)&&const DeepCollectionEquality().equals(other.configurationSchema, configurationSchema)&&(identical(other.minSdkVersion, minSdkVersion) || other.minSdkVersion == minSdkVersion)&&(identical(other.minPlatformVersion, minPlatformVersion) || other.minPlatformVersion == minPlatformVersion));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,name,description,version,author,category,const DeepCollectionEquality().hash(dependencies),const DeepCollectionEquality().hash(permissions),const DeepCollectionEquality().hash(featureFlags),const DeepCollectionEquality().hash(configurationSchema),minSdkVersion,minPlatformVersion);

@override
String toString() {
  return 'ExtensionMetadata(id: $id, name: $name, description: $description, version: $version, author: $author, category: $category, dependencies: $dependencies, permissions: $permissions, featureFlags: $featureFlags, configurationSchema: $configurationSchema, minSdkVersion: $minSdkVersion, minPlatformVersion: $minPlatformVersion)';
}


}

/// @nodoc
abstract mixin class $ExtensionMetadataCopyWith<$Res>  {
  factory $ExtensionMetadataCopyWith(ExtensionMetadata value, $Res Function(ExtensionMetadata) _then) = _$ExtensionMetadataCopyWithImpl;
@useResult
$Res call({
 String id, String name, String description, String version, String author, ExtensionCategory category, List<String> dependencies, List<String> permissions, Map<String, bool> featureFlags, Map<String, dynamic> configurationSchema, String minSdkVersion, String minPlatformVersion
});




}
/// @nodoc
class _$ExtensionMetadataCopyWithImpl<$Res>
    implements $ExtensionMetadataCopyWith<$Res> {
  _$ExtensionMetadataCopyWithImpl(this._self, this._then);

  final ExtensionMetadata _self;
  final $Res Function(ExtensionMetadata) _then;

/// Create a copy of ExtensionMetadata
/// with the given fields replaced by the non-null parameter values.
@pragma('vm:prefer-inline') @override $Res call({Object? id = null,Object? name = null,Object? description = null,Object? version = null,Object? author = null,Object? category = null,Object? dependencies = null,Object? permissions = null,Object? featureFlags = null,Object? configurationSchema = null,Object? minSdkVersion = null,Object? minPlatformVersion = null,}) {
  return _then(_self.copyWith(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,name: null == name ? _self.name : name // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,version: null == version ? _self.version : version // ignore: cast_nullable_to_non_nullable
as String,author: null == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as ExtensionCategory,dependencies: null == dependencies ? _self.dependencies : dependencies // ignore: cast_nullable_to_non_nullable
as List<String>,permissions: null == permissions ? _self.permissions : permissions // ignore: cast_nullable_to_non_nullable
as List<String>,featureFlags: null == featureFlags ? _self.featureFlags : featureFlags // ignore: cast_nullable_to_non_nullable
as Map<String, bool>,configurationSchema: null == configurationSchema ? _self.configurationSchema : configurationSchema // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>,minSdkVersion: null == minSdkVersion ? _self.minSdkVersion : minSdkVersion // ignore: cast_nullable_to_non_nullable
as String,minPlatformVersion: null == minPlatformVersion ? _self.minPlatformVersion : minPlatformVersion // ignore: cast_nullable_to_non_nullable
as String,
  ));
}

}


/// Adds pattern-matching-related methods to [ExtensionMetadata].
extension ExtensionMetadataPatterns on ExtensionMetadata {
/// A variant of `map` that fallback to returning `orElse`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeMap<TResult extends Object?>(TResult Function( _ExtensionMetadata value)?  $default,{required TResult orElse(),}){
final _that = this;
switch (_that) {
case _ExtensionMetadata() when $default != null:
return $default(_that);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// Callbacks receives the raw object, upcasted.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case final Subclass2 value:
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult map<TResult extends Object?>(TResult Function( _ExtensionMetadata value)  $default,){
final _that = this;
switch (_that) {
case _ExtensionMetadata():
return $default(_that);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `map` that fallback to returning `null`.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case final Subclass value:
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? mapOrNull<TResult extends Object?>(TResult? Function( _ExtensionMetadata value)?  $default,){
final _that = this;
switch (_that) {
case _ExtensionMetadata() when $default != null:
return $default(_that);case _:
  return null;

}
}
/// A variant of `when` that fallback to an `orElse` callback.
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return orElse();
/// }
/// ```

@optionalTypeArgs TResult maybeWhen<TResult extends Object?>(TResult Function( String id,  String name,  String description,  String version,  String author,  ExtensionCategory category,  List<String> dependencies,  List<String> permissions,  Map<String, bool> featureFlags,  Map<String, dynamic> configurationSchema,  String minSdkVersion,  String minPlatformVersion)?  $default,{required TResult orElse(),}) {final _that = this;
switch (_that) {
case _ExtensionMetadata() when $default != null:
return $default(_that.id,_that.name,_that.description,_that.version,_that.author,_that.category,_that.dependencies,_that.permissions,_that.featureFlags,_that.configurationSchema,_that.minSdkVersion,_that.minPlatformVersion);case _:
  return orElse();

}
}
/// A `switch`-like method, using callbacks.
///
/// As opposed to `map`, this offers destructuring.
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case Subclass2(:final field2):
///     return ...;
/// }
/// ```

@optionalTypeArgs TResult when<TResult extends Object?>(TResult Function( String id,  String name,  String description,  String version,  String author,  ExtensionCategory category,  List<String> dependencies,  List<String> permissions,  Map<String, bool> featureFlags,  Map<String, dynamic> configurationSchema,  String minSdkVersion,  String minPlatformVersion)  $default,) {final _that = this;
switch (_that) {
case _ExtensionMetadata():
return $default(_that.id,_that.name,_that.description,_that.version,_that.author,_that.category,_that.dependencies,_that.permissions,_that.featureFlags,_that.configurationSchema,_that.minSdkVersion,_that.minPlatformVersion);case _:
  throw StateError('Unexpected subclass');

}
}
/// A variant of `when` that fallback to returning `null`
///
/// It is equivalent to doing:
/// ```dart
/// switch (sealedClass) {
///   case Subclass(:final field):
///     return ...;
///   case _:
///     return null;
/// }
/// ```

@optionalTypeArgs TResult? whenOrNull<TResult extends Object?>(TResult? Function( String id,  String name,  String description,  String version,  String author,  ExtensionCategory category,  List<String> dependencies,  List<String> permissions,  Map<String, bool> featureFlags,  Map<String, dynamic> configurationSchema,  String minSdkVersion,  String minPlatformVersion)?  $default,) {final _that = this;
switch (_that) {
case _ExtensionMetadata() when $default != null:
return $default(_that.id,_that.name,_that.description,_that.version,_that.author,_that.category,_that.dependencies,_that.permissions,_that.featureFlags,_that.configurationSchema,_that.minSdkVersion,_that.minPlatformVersion);case _:
  return null;

}
}

}

/// @nodoc
@JsonSerializable()

class _ExtensionMetadata implements ExtensionMetadata {
  const _ExtensionMetadata({required this.id, required this.name, required this.description, required this.version, required this.author, required this.category, final  List<String> dependencies = const [], final  List<String> permissions = const [], final  Map<String, bool> featureFlags = const {}, final  Map<String, dynamic> configurationSchema = const {}, required this.minSdkVersion, required this.minPlatformVersion}): _dependencies = dependencies,_permissions = permissions,_featureFlags = featureFlags,_configurationSchema = configurationSchema;
  factory _ExtensionMetadata.fromJson(Map<String, dynamic> json) => _$ExtensionMetadataFromJson(json);

@override final  String id;
@override final  String name;
@override final  String description;
@override final  String version;
@override final  String author;
@override final  ExtensionCategory category;
 final  List<String> _dependencies;
@override@JsonKey() List<String> get dependencies {
  if (_dependencies is EqualUnmodifiableListView) return _dependencies;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_dependencies);
}

 final  List<String> _permissions;
@override@JsonKey() List<String> get permissions {
  if (_permissions is EqualUnmodifiableListView) return _permissions;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableListView(_permissions);
}

 final  Map<String, bool> _featureFlags;
@override@JsonKey() Map<String, bool> get featureFlags {
  if (_featureFlags is EqualUnmodifiableMapView) return _featureFlags;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableMapView(_featureFlags);
}

 final  Map<String, dynamic> _configurationSchema;
@override@JsonKey() Map<String, dynamic> get configurationSchema {
  if (_configurationSchema is EqualUnmodifiableMapView) return _configurationSchema;
  // ignore: implicit_dynamic_type
  return EqualUnmodifiableMapView(_configurationSchema);
}

@override final  String minSdkVersion;
@override final  String minPlatformVersion;

/// Create a copy of ExtensionMetadata
/// with the given fields replaced by the non-null parameter values.
@override @JsonKey(includeFromJson: false, includeToJson: false)
@pragma('vm:prefer-inline')
_$ExtensionMetadataCopyWith<_ExtensionMetadata> get copyWith => __$ExtensionMetadataCopyWithImpl<_ExtensionMetadata>(this, _$identity);

@override
Map<String, dynamic> toJson() {
  return _$ExtensionMetadataToJson(this, );
}

@override
bool operator ==(Object other) {
  return identical(this, other) || (other.runtimeType == runtimeType&&other is _ExtensionMetadata&&(identical(other.id, id) || other.id == id)&&(identical(other.name, name) || other.name == name)&&(identical(other.description, description) || other.description == description)&&(identical(other.version, version) || other.version == version)&&(identical(other.author, author) || other.author == author)&&(identical(other.category, category) || other.category == category)&&const DeepCollectionEquality().equals(other._dependencies, _dependencies)&&const DeepCollectionEquality().equals(other._permissions, _permissions)&&const DeepCollectionEquality().equals(other._featureFlags, _featureFlags)&&const DeepCollectionEquality().equals(other._configurationSchema, _configurationSchema)&&(identical(other.minSdkVersion, minSdkVersion) || other.minSdkVersion == minSdkVersion)&&(identical(other.minPlatformVersion, minPlatformVersion) || other.minPlatformVersion == minPlatformVersion));
}

@JsonKey(includeFromJson: false, includeToJson: false)
@override
int get hashCode => Object.hash(runtimeType,id,name,description,version,author,category,const DeepCollectionEquality().hash(_dependencies),const DeepCollectionEquality().hash(_permissions),const DeepCollectionEquality().hash(_featureFlags),const DeepCollectionEquality().hash(_configurationSchema),minSdkVersion,minPlatformVersion);

@override
String toString() {
  return 'ExtensionMetadata(id: $id, name: $name, description: $description, version: $version, author: $author, category: $category, dependencies: $dependencies, permissions: $permissions, featureFlags: $featureFlags, configurationSchema: $configurationSchema, minSdkVersion: $minSdkVersion, minPlatformVersion: $minPlatformVersion)';
}


}

/// @nodoc
abstract mixin class _$ExtensionMetadataCopyWith<$Res> implements $ExtensionMetadataCopyWith<$Res> {
  factory _$ExtensionMetadataCopyWith(_ExtensionMetadata value, $Res Function(_ExtensionMetadata) _then) = __$ExtensionMetadataCopyWithImpl;
@override @useResult
$Res call({
 String id, String name, String description, String version, String author, ExtensionCategory category, List<String> dependencies, List<String> permissions, Map<String, bool> featureFlags, Map<String, dynamic> configurationSchema, String minSdkVersion, String minPlatformVersion
});




}
/// @nodoc
class __$ExtensionMetadataCopyWithImpl<$Res>
    implements _$ExtensionMetadataCopyWith<$Res> {
  __$ExtensionMetadataCopyWithImpl(this._self, this._then);

  final _ExtensionMetadata _self;
  final $Res Function(_ExtensionMetadata) _then;

/// Create a copy of ExtensionMetadata
/// with the given fields replaced by the non-null parameter values.
@override @pragma('vm:prefer-inline') $Res call({Object? id = null,Object? name = null,Object? description = null,Object? version = null,Object? author = null,Object? category = null,Object? dependencies = null,Object? permissions = null,Object? featureFlags = null,Object? configurationSchema = null,Object? minSdkVersion = null,Object? minPlatformVersion = null,}) {
  return _then(_ExtensionMetadata(
id: null == id ? _self.id : id // ignore: cast_nullable_to_non_nullable
as String,name: null == name ? _self.name : name // ignore: cast_nullable_to_non_nullable
as String,description: null == description ? _self.description : description // ignore: cast_nullable_to_non_nullable
as String,version: null == version ? _self.version : version // ignore: cast_nullable_to_non_nullable
as String,author: null == author ? _self.author : author // ignore: cast_nullable_to_non_nullable
as String,category: null == category ? _self.category : category // ignore: cast_nullable_to_non_nullable
as ExtensionCategory,dependencies: null == dependencies ? _self._dependencies : dependencies // ignore: cast_nullable_to_non_nullable
as List<String>,permissions: null == permissions ? _self._permissions : permissions // ignore: cast_nullable_to_non_nullable
as List<String>,featureFlags: null == featureFlags ? _self._featureFlags : featureFlags // ignore: cast_nullable_to_non_nullable
as Map<String, bool>,configurationSchema: null == configurationSchema ? _self._configurationSchema : configurationSchema // ignore: cast_nullable_to_non_nullable
as Map<String, dynamic>,minSdkVersion: null == minSdkVersion ? _self.minSdkVersion : minSdkVersion // ignore: cast_nullable_to_non_nullable
as String,minPlatformVersion: null == minPlatformVersion ? _self.minPlatformVersion : minPlatformVersion // ignore: cast_nullable_to_non_nullable
as String,
  ));
}


}

// dart format on
