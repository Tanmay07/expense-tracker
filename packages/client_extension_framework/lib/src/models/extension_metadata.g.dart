// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'extension_metadata.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

_ExtensionMetadata _$ExtensionMetadataFromJson(Map<String, dynamic> json) =>
    _ExtensionMetadata(
      id: json['id'] as String,
      name: json['name'] as String,
      description: json['description'] as String,
      version: json['version'] as String,
      author: json['author'] as String,
      category: $enumDecode(_$ExtensionCategoryEnumMap, json['category']),
      dependencies:
          (json['dependencies'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      permissions:
          (json['permissions'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          const [],
      featureFlags:
          (json['featureFlags'] as Map<String, dynamic>?)?.map(
            (k, e) => MapEntry(k, e as bool),
          ) ??
          const {},
      configurationSchema:
          json['configurationSchema'] as Map<String, dynamic>? ?? const {},
      minSdkVersion: json['minSdkVersion'] as String,
      minPlatformVersion: json['minPlatformVersion'] as String,
    );

Map<String, dynamic> _$ExtensionMetadataToJson(_ExtensionMetadata instance) =>
    <String, dynamic>{
      'id': instance.id,
      'name': instance.name,
      'description': instance.description,
      'version': instance.version,
      'author': instance.author,
      'category': _$ExtensionCategoryEnumMap[instance.category]!,
      'dependencies': instance.dependencies,
      'permissions': instance.permissions,
      'featureFlags': instance.featureFlags,
      'configurationSchema': instance.configurationSchema,
      'minSdkVersion': instance.minSdkVersion,
      'minPlatformVersion': instance.minPlatformVersion,
    };

const _$ExtensionCategoryEnumMap = {
  ExtensionCategory.auth: 'auth',
  ExtensionCategory.ai: 'ai',
  ExtensionCategory.sync: 'sync',
  ExtensionCategory.notification: 'notification',
  ExtensionCategory.storage: 'storage',
  ExtensionCategory.payments: 'payments',
  ExtensionCategory.camera: 'camera',
  ExtensionCategory.biometrics: 'biometrics',
  ExtensionCategory.analytics: 'analytics',
  ExtensionCategory.ocr: 'ocr',
  ExtensionCategory.search: 'search',
  ExtensionCategory.reporting: 'reporting',
  ExtensionCategory.widget: 'widget',
  ExtensionCategory.voice: 'voice',
  ExtensionCategory.theme: 'theme',
  ExtensionCategory.localization: 'localization',
  ExtensionCategory.bankingConnector: 'bankingConnector',
  ExtensionCategory.investmentConnector: 'investmentConnector',
  ExtensionCategory.tax: 'tax',
  ExtensionCategory.advisor: 'advisor',
  ExtensionCategory.household: 'household',
  ExtensionCategory.whiteLabel: 'whiteLabel',
  ExtensionCategory.enterpriseBranding: 'enterpriseBranding',
  ExtensionCategory.experimental: 'experimental',
  ExtensionCategory.other: 'other',
};
