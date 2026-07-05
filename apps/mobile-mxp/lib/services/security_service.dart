import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:local_auth/local_auth.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final securityServiceProvider = Provider<SecurityService>((ref) {
  return SecurityService(
    const FlutterSecureStorage(),
    LocalAuthentication(),
  );
});

class SecurityService {
  final FlutterSecureStorage _secureStorage;
  final LocalAuthentication _localAuth;

  SecurityService(this._secureStorage, this._localAuth);

  Future<bool> authenticateBiometrics(String reason) async {
    try {
      final canCheckBiometrics = await _localAuth.canCheckBiometrics;
      final isDeviceSupported = await _localAuth.isDeviceSupported();

      if (!canCheckBiometrics || !isDeviceSupported) {
        return false;
      }

      return await _localAuth.authenticate(
        localizedReason: reason,
        biometricOnly: true,
      );
    } catch (e) {
      return false;
    }
  }

  Future<void> saveSecureToken(String key, String token) async {
    await _secureStorage.write(key: key, value: token);
  }

  Future<String?> getSecureToken(String key) async {
    return await _secureStorage.read(key: key);
  }

  Future<void> deleteSecureToken(String key) async {
    await _secureStorage.delete(key: key);
  }
}
