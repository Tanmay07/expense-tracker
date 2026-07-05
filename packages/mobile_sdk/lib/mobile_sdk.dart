// Expose the core Dependency Injection layer and the main SDK Facade
export 'src/di/dependency_injection.dart';

// Expose the API components
export 'src/api/api_client.dart';

// Expose Auth & Security Modules
export 'src/auth/authentication_service.dart';
export 'src/security/security_service.dart';

// Expose Offline Sync & Cache Modules
export 'src/offline/cache_service.dart';
export 'src/offline/sync_service.dart';

// Expose Telemetry, Feature Flags & Notifications
export 'src/telemetry/telemetry_service.dart';
export 'src/flags/feature_flag_service.dart';
export 'src/notifications/notification_service.dart';
