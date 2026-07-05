import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:local_auth/local_auth.dart';

final securityServiceProvider = Provider<SecurityService>((ref) {
  const secureStorage = FlutterSecureStorage();
  final localAuth = LocalAuthentication();
  return SecurityService(secureStorage, localAuth);
});

class SecurityService {
  final FlutterSecureStorage _secureStorage;
  final LocalAuthentication _localAuth;

  SecurityService(this._secureStorage, this._localAuth);

  Future<void> saveSecureItem(String key, String value) async {
    await _secureStorage.write(key: key, value: value);
  }

  Future<String?> readSecureItem(String key) async {
    return await _secureStorage.read(key: key);
  }

  Future<void> deleteSecureItem(String key) async {
    await _secureStorage.delete(key: key);
  }

  Future<void> clearAll() async {
    await _secureStorage.deleteAll();
  }

  Future<bool> isBiometricAvailable() async {
    final bool canAuthenticateWithBiometrics = await _localAuth.canCheckBiometrics;
    final bool canAuthenticate = canAuthenticateWithBiometrics || await _localAuth.isDeviceSupported();
    return canAuthenticate;
  }

  Future<bool> authenticateWithBiometrics(String reason) async {
    if (!await isBiometricAvailable()) return false;

    try {
      return await _localAuth.authenticate(
        localizedReason: reason,
        biometricOnly: true,
        persistAcrossBackgrounding: true,
      );
    } catch (e) {
      // Log biometric error via telemetry later
      return false;
    }
  }
}
