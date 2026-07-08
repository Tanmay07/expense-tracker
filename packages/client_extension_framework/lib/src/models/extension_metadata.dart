import 'package:freezed_annotation/freezed_annotation.dart';

part 'extension_metadata.freezed.dart';
part 'extension_metadata.g.dart';

@freezed
class ExtensionMetadata with _$ExtensionMetadata {
  const factory ExtensionMetadata({
    required String id,
    required String name,
    required String description,
    required String version,
    required String author,
    required ExtensionCategory category,
    
    @Default([]) List<String> dependencies,
    @Default([]) List<String> permissions,
    @Default({}) Map<String, bool> featureFlags,
    @Default({}) Map<String, dynamic> configurationSchema,
    
    required String minSdkVersion,
    required String minPlatformVersion,
  }) = _ExtensionMetadata;

  factory ExtensionMetadata.fromJson(Map<String, dynamic> json) => _$ExtensionMetadataFromJson(json);
}

enum ExtensionCategory {
  auth,
  ai,
  sync,
  notification,
  storage,
  payments,
  camera,
  biometrics,
  analytics,
  ocr,
  search,
  reporting,
  widget,
  voice,
  theme,
  localization,
  bankingConnector,
  investmentConnector,
  tax,
  advisor,
  household,
  whiteLabel,
  enterpriseBranding,
  experimental,
  other,
}
