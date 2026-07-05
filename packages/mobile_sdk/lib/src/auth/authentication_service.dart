import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';
import '../security/security_service.dart';

final authServiceProvider = Provider<AuthenticationService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  final securityService = ref.watch(securityServiceProvider);
  return AuthenticationService(apiClient, securityService);
});

class AuthenticationService {
  final ApiClient _apiClient;
  final SecurityService _securityService;
  
  static const String _tokenKey = 'auth_jwt_token';
  static const String _refreshTokenKey = 'auth_refresh_token';

  AuthenticationService(this._apiClient, this._securityService);

  Future<bool> login(String username, String password) async {
    try {
      final response = await _apiClient.post(
        '/auth/login',
        data: {'username': username, 'password': password},
      );

      if (response.statusCode == 200 && response.data != null) {
        final token = response.data['token'];
        final refreshToken = response.data['refresh_token'];
        
        await _securityService.saveSecureItem(_tokenKey, token);
        await _securityService.saveSecureItem(_refreshTokenKey, refreshToken);
        return true;
      }
      return false;
    } catch (e) {
      return false;
    }
  }

  Future<bool> validateSession() async {
    final token = await _securityService.readSecureItem(_tokenKey);
    if (token == null) return false;

    // Optional: Call a /auth/validate endpoint if local parsing isn't enough
    return true; 
  }

  Future<void> logout() async {
    await _securityService.deleteSecureItem(_tokenKey);
    await _securityService.deleteSecureItem(_refreshTokenKey);
    // Notify BFF about session termination if necessary
  }

  Future<bool> refreshToken() async {
    final refreshToken = await _securityService.readSecureItem(_refreshTokenKey);
    if (refreshToken == null) return false;

    try {
      final response = await _apiClient.post(
        '/auth/refresh',
        data: {'refresh_token': refreshToken},
      );

      if (response.statusCode == 200) {
        final newToken = response.data['token'];
        await _securityService.saveSecureItem(_tokenKey, newToken);
        return true;
      }
      return false;
    } catch (e) {
      await logout(); // Force logout on failed refresh
      return false;
    }
  }
}
