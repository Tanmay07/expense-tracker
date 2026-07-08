import 'package:mockito/annotations.dart';
import 'package:dio/dio.dart';
import 'package:mobile_sdk/mobile_sdk.dart';

@GenerateMocks([
  Dio,
  ApiClient,
  CacheService,
  SyncService,
  SecurityService,
])
void main() {}
