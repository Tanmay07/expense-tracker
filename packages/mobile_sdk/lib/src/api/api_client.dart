import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../security/security_service.dart';

final apiClientProvider = Provider<ApiClient>((ref) {
  final securityService = ref.watch(securityServiceProvider);
  return ApiClient(securityService);
});

class ApiClient {
  late final Dio _dio;

  ApiClient(SecurityService securityService) {
    _dio = Dio(BaseOptions(
      baseUrl: const String.fromEnvironment('API_BASE_URL', defaultValue: 'https://api.financeos.local'),
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 15),
      sendTimeout: const Duration(seconds: 15),
    ));

    // Register Interceptors
    _dio.interceptors.addAll([
      _AuthInterceptor(securityService),
      _RetryInterceptor(),
    ]);
  }

  Future<Response<T>> get<T>(String path, {Map<String, dynamic>? queryParameters}) {
    return _dio.get<T>(path, queryParameters: queryParameters);
  }

  Future<Response<T>> post<T>(String path, {dynamic data, Map<String, dynamic>? queryParameters}) {
    return _dio.post<T>(path, data: data, queryParameters: queryParameters);
  }

  Future<Response<T>> put<T>(String path, {dynamic data, Map<String, dynamic>? queryParameters}) {
    return _dio.put<T>(path, data: data, queryParameters: queryParameters);
  }

  Future<Response<T>> delete<T>(String path, {dynamic data, Map<String, dynamic>? queryParameters}) {
    return _dio.delete<T>(path, data: data, queryParameters: queryParameters);
  }
}

class _AuthInterceptor extends Interceptor {
  final SecurityService _securityService;

  _AuthInterceptor(this._securityService);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    final token = await _securityService.readSecureItem('auth_jwt_token');
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    options.headers['X-Platform-Client'] = 'MobileSDK/1.0.0';
    super.onRequest(options, handler);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    if (err.response?.statusCode == 401) {
      // Handle automatic token refresh logic here, typically by catching 401
      // and retrying the request after calling refreshToken() on Auth Service.
    }
    super.onError(err, handler);
  }
}

class _RetryInterceptor extends Interceptor {
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    // Implement exponential backoff for 5xx errors or network timeouts
    if (err.type == DioExceptionType.connectionTimeout || err.response?.statusCode == 503) {
      // Schedule retry
    }
    super.onError(err, handler);
  }
}
