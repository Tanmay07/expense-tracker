import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../services/vision_service.dart';
import '../../../services/api/bff_client.dart';

class CameraScreen extends ConsumerStatefulWidget {
  const CameraScreen({super.key});

  @override
  ConsumerState<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends ConsumerState<CameraScreen> {
  bool _isProcessing = false;
  String? _result;

  Future<void> _scanReceipt() async {
    final visionService = ref.read(visionServiceProvider);
    final bffClient = ref.read(bffClientProvider);

    final imageFile = await visionService.captureReceipt();
    if (imageFile != null) {
      setState(() {
        _isProcessing = true;
        _result = null;
      });

      // Send to BFF for extraction
      final extractedData = await bffClient.uploadImageForExtraction(imageFile.path);

      setState(() {
        _isProcessing = false;
        _result = extractedData;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Document Scanner'),
      ),
      body: Center(
        child: _isProcessing
            ? const Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  CircularProgressIndicator(),
                  SizedBox(height: 16),
                  Text('Extracting data via AI Platform...'),
                ],
              )
            : _result != null
                ? Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.check_circle, color: Colors.green, size: 64),
                        const SizedBox(height: 16),
                        Text('Extraction Complete', style: theme.textTheme.headlineSmall),
                        const SizedBox(height: 16),
                        Text(_result!),
                        const SizedBox(height: 24),
                        ElevatedButton.icon(
                          onPressed: () => setState(() => _result = null),
                          icon: const Icon(Icons.refresh),
                          label: const Text('Scan Another'),
                        )
                      ],
                    ),
                  )
                : Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.document_scanner, size: 80, color: theme.colorScheme.primary.withValues(alpha: 0.5)),
                      const SizedBox(height: 16),
                      Text('Scan a receipt or document', style: theme.textTheme.titleLarge),
                      const SizedBox(height: 24),
                      FilledButton.icon(
                        onPressed: _scanReceipt,
                        icon: const Icon(Icons.camera_alt),
                        label: const Text('Open Camera'),
                      )
                    ],
                  ),
      ),
    );
  }
}
