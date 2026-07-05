import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:permission_handler/permission_handler.dart';

final voiceServiceProvider = Provider<VoiceService>((ref) {
  return VoiceService(SpeechToText());
});

class VoiceService {
  final SpeechToText _speech;
  bool _isInitialized = false;

  VoiceService(this._speech);

  Future<bool> initialize() async {
    if (_isInitialized) return true;
    
    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      return false;
    }

    _isInitialized = await _speech.initialize(
      onError: (error) => debugPrint('Speech error: $error'),
      onStatus: (status) => debugPrint('Speech status: $status'),
    );
    return _isInitialized;
  }

  Future<void> startListening(Function(String) onResult) async {
    if (!_isInitialized) {
      final initialized = await initialize();
      if (!initialized) return;
    }

    await _speech.listen(
      onResult: (result) {
        onResult(result.recognizedWords);
      },
      listenOptions: SpeechListenOptions(
        listenFor: const Duration(seconds: 30),
        pauseFor: const Duration(seconds: 5),
        partialResults: true,
        cancelOnError: true,
        listenMode: ListenMode.dictation,
      ),
    );
  }

  Future<void> stopListening() async {
    if (_speech.isListening) {
      await _speech.stop();
    }
  }

  bool get isListening => _speech.isListening;
}
