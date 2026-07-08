import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:dio/dio.dart';
import 'package:mobile_sdk/mobile_sdk.dart';
import 'mocks.mocks.dart';

void main() {
  late MockApiClient mockApiClient;
  late MockCacheService mockCacheService;
  late MockSyncService mockSyncService;
  late AccountsRepository accountsRepository;

  setUp(() {
    mockApiClient = MockApiClient();
    mockCacheService = MockCacheService();
    mockSyncService = MockSyncService();

    accountsRepository = AccountsRepository(
      apiClient: mockApiClient,
      cacheService: mockCacheService,
      syncService: mockSyncService,
    );
  });

  group('AccountsRepository', () {
    test('getAccounts returns network data and updates cache', () async {
      // Arrange
      final mockData = [
        {'id': '1', 'name': 'Checking Account'}
      ];
      final mockResponse = Response(
        requestOptions: RequestOptions(path: '/accounts'),
        statusCode: 200,
        data: mockData,
      );

      when(mockCacheService.getCache('accounts_list')).thenAnswer((_) async => null);
      when(mockApiClient.get('/accounts')).thenAnswer((_) async => mockResponse);

      // Act
      final result = await accountsRepository.getAccounts();

      // Assert
      expect(result, mockData);
      verify(mockApiClient.get('/accounts')).called(1);
      verify(mockCacheService.setCache('accounts_list', mockData, ttl: const Duration(minutes: 15))).called(1);
    });

    test('getAccounts returns cached data if available (network not forced)', () async {
      // Arrange
      final cachedData = [
        {'id': '2', 'name': 'Savings Account'}
      ];
      
      when(mockCacheService.getCache('accounts_list')).thenAnswer((_) async => cachedData);

      // Act
      final result = await accountsRepository.getAccounts();

      // Assert
      expect(result, cachedData);
      verify(mockCacheService.getCache('accounts_list')).called(1);
      verifyNever(mockApiClient.get(any)); // Network should not be called
    });

    test('createAccount queues mutation offline', () async {
      // Arrange
      final accountData = {'name': 'New Account'};

      // Act
      await accountsRepository.createAccount(accountData);

      // Assert
      verify(mockSyncService.queueMutation('account', 'CREATE', accountData)).called(1);
      verify(mockCacheService.removeCache('accounts_list')).called(1); // Ensure cache is invalidated
    });
  });
}
