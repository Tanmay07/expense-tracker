import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:dio/dio.dart';

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: 'http://localhost:3000/api/bff',
    connectTimeout: const Duration(seconds: 5),
    receiveTimeout: const Duration(seconds: 3),
  ));
  
  // Add interceptors for auth/telemetry in future sprints
  return dio;
});

final bffClientProvider = Provider<BffClient>((ref) {
  return BffClient(ref.watch(dioProvider));
});

// A simple Mission model for the UI
class MissionModel {
  final String id;
  final String title;
  final String type;
  final String priority;

  MissionModel({required this.id, required this.title, required this.type, required this.priority});
}

class BffClient {
  // ignore: unused_field
  final Dio _dio;

  BffClient(this._dio);

  Future<List<MissionModel>> fetchMissions() async {
    // In a real implementation this calls _dio.get('/missions')
    // For now we mock the BFF response to rapidly build the UI
    await Future.delayed(const Duration(milliseconds: 800));
    return [
      MissionModel(id: '1', title: 'Review Uncategorized Expenses', type: 'TODAYS_TASKS', priority: 'HIGH'),
      MissionModel(id: '2', title: 'Optimize Savings Rate', type: 'SAVINGS_SUGGESTIONS', priority: 'MEDIUM'),
    ];
  }

  Future<List<Map<String, dynamic>>> fetchWorkspaces() async {
    await Future.delayed(const Duration(milliseconds: 600));
    return [
      {'id': 'expenses', 'name': 'Expenses', 'icon': 'receipt'},
      {'id': 'investments', 'name': 'Investments', 'icon': 'trending_up'},
      {'id': 'goals', 'name': 'Goals', 'icon': 'flag'},
    ];
  }
}

// Riverpod providers for UI consumption
final missionsProvider = FutureProvider<List<MissionModel>>((ref) async {
  return ref.watch(bffClientProvider).fetchMissions();
});

final workspacesProvider = FutureProvider<List<Map<String, dynamic>>>((ref) async {
  return ref.watch(bffClientProvider).fetchWorkspaces();
});
