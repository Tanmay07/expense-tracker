import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../services/voice_service.dart';
import '../../../services/api/bff_client.dart';

class AiShellScreen extends ConsumerStatefulWidget {
  const AiShellScreen({super.key});

  @override
  ConsumerState<AiShellScreen> createState() => _AiShellScreenState();
}

class _AiShellScreenState extends ConsumerState<AiShellScreen> {
  final TextEditingController _textController = TextEditingController();
  final List<String> _messages = [];
  bool _isListening = false;

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;
    
    setState(() {
      _messages.add('User: $text');
    });
    
    _textController.clear();
    
    final bffClient = ref.read(bffClientProvider);
    final response = await bffClient.sendIntent(text);
    
    setState(() {
      _messages.add('AI: $response');
    });
  }

  Future<void> _toggleVoice() async {
    final voiceService = ref.read(voiceServiceProvider);
    
    if (_isListening) {
      await voiceService.stopListening();
      setState(() {
        _isListening = false;
        if (_textController.text.isNotEmpty) {
          _sendMessage(_textController.text);
        }
      });
    } else {
      setState(() => _isListening = true);
      await voiceService.startListening((words) {
        setState(() {
          _textController.text = words;
        });
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('AI Assistant'),
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final isUser = _messages[index].startsWith('User:');
                final message = _messages[index].replaceFirst(isUser ? 'User: ' : 'AI: ', '');
                
                return Align(
                  alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    decoration: BoxDecoration(
                      color: isUser ? theme.colorScheme.primary : theme.colorScheme.surfaceContainerHighest,
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Text(
                      message,
                      style: TextStyle(
                        color: isUser ? theme.colorScheme.onPrimary : theme.colorScheme.onSurface,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          _buildInputBar(theme),
        ],
      ),
    );
  }

  Widget _buildInputBar(ThemeData theme) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: theme.colorScheme.surface,
        border: Border(top: BorderSide(color: theme.dividerColor)),
      ),
      child: Row(
        children: [
          IconButton(
            icon: Icon(_isListening ? Icons.mic : Icons.mic_none),
            color: _isListening ? theme.colorScheme.error : theme.colorScheme.primary,
            onPressed: _toggleVoice,
          ),
          Expanded(
            child: TextField(
              controller: _textController,
              decoration: const InputDecoration(
                hintText: 'Ask anything...',
                border: InputBorder.none,
              ),
              onSubmitted: _sendMessage,
            ),
          ),
          IconButton(
            icon: const Icon(Icons.send),
            color: theme.colorScheme.primary,
            onPressed: () => _sendMessage(_textController.text),
          ),
        ],
      ),
    );
  }
}
