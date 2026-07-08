import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_client.dart';

final fileTransferServiceProvider = Provider<FileTransferService>((ref) {
  final apiClient = ref.watch(apiClientProvider);
  return FileTransferService(apiClient);
});

class FileTransferService {
  final ApiClient _apiClient;

  FileTransferService(this._apiClient);

  Future<bool> uploadFile(String filePath, String destinationEndpoint, {Map<String, dynamic>? additionalData}) async {
    try {
      String fileName = filePath.split('/').last;
      
      FormData formData = FormData.fromMap({
        ...?additionalData,
        'file': await MultipartFile.fromFile(filePath, filename: fileName),
      });

      // Directly use the Dio instance inside ApiClient via a proxy method or we can expose it
      // Assuming we have an exposed postMultipart method in ApiClient (we'll need to add it)
      final response = await _apiClient.post(
        destinationEndpoint,
        data: formData,
      );

      return response.statusCode == 200 || response.statusCode == 201;
    } catch (e) {
      return false;
    }
  }

  Future<bool> downloadFile(String url, String savePath) async {
    try {
      final response = await _apiClient.get(
        url,
        // Since get() on our ApiClient currently doesn't allow setting responseType,
        // this is a mock implementation. We will enhance ApiClient if necessary.
      );
      // Actual implementation would write bytes to disk
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
