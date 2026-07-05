import { useState, useRef, useEffect } from 'react';
import { Bot, Send, Paperclip, X, Settings2, Minimize2, Maximize2, PlayCircle, Square, SkipBack, SkipForward, Circle, WifiOff } from 'lucide-react';
import { useAIStore } from '../../store/useAIStore';
import { useAppStore } from '../../store/useAppStore';
import { useContextAssembler } from '../../hooks/useContextAssembler';
import { useSessionReplay } from '../../store/useSessionReplay';
import { useTelemetry } from '../../store/useTelemetry';
import { useOfflineSync } from '../../store/useOfflineSync';
import { cn } from '../../utils/cn';
import { AIMessage } from './components/AIMessage';

import { useAICapabilities } from '../../hooks/useAICapabilities';

export function AICopilotPanel() {
  const { isShellOpen, shellMode, toggleShell, setShellMode, turns, addTurn, updateLastTurn, queueAction } = useAIStore();
  const { isRecording, isReplaying, startRecording, stopRecording, startReplay, stopReplay, stepForward, stepBack, sessions } = useSessionReplay();
  const { isOfflineMode } = useAppStore();
  const { trackEvent } = useTelemetry();
  const { queueLength } = useOfflineSync();
  const { assembleContext } = useContextAssembler();
  const { data: capabilities } = useAICapabilities();
  const chatCapability = capabilities?.find(c => c.id === 'cap_chat_01');
  const [input, setInput] = useState('');
  const [isQuerying, setIsQuerying] = useState(false);
  const [attachments, setAttachments] = useState<File[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [turns]);

  if (!isShellOpen) return null;

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setAttachments(prev => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeAttachment = (index: number) => {
    setAttachments(prev => prev.filter((_, i) => i !== index));
  };

  const handleSend = async () => {
    if (!input.trim() && attachments.length === 0) return;
    
    const context = assembleContext();
    const userMessageId = `msg_${Date.now()}`;
    const userTurn = { 
      id: userMessageId, 
      role: 'user' as const, 
      content: input, 
      timestamp: new Date().toISOString(), 
      metadata: { ...context, attachments: attachments.map(f => f.name) } 
    };
    
    addTurn(userTurn);
    useSessionReplay.getState().recordEvent('TURN_ADDED', userTurn);
    trackEvent('CONVERSATION_STARTED', { hasAttachments: attachments.length > 0 });
    
    if (isOfflineMode) {
      queueAction({ type: 'TURN', payload: userTurn });
      // Show optimistic offline response
      const offlineMsgId = `msg_${Date.now() + 1}`;
      addTurn({ 
        id: offlineMsgId, 
        role: 'assistant' as const, 
        content: "You're currently offline. Your message has been queued and will be sent when connection is restored.", 
        timestamp: new Date().toISOString(), 
        isStreaming: false 
      });
      setInput('');
      setAttachments([]);
      return;
    }

    setInput('');
    setAttachments([]);

    const assistantMessageId = `msg_${Date.now() + 1}`;
    const initialAssistantTurn = { id: assistantMessageId, role: 'assistant' as const, content: '', timestamp: new Date().toISOString(), isStreaming: true };
    addTurn(initialAssistantTurn);
    useSessionReplay.getState().recordEvent('TURN_ADDED', initialAssistantTurn);
    
    setIsQuerying(true);
    try {
      const provider = useAppStore.getState().getProvider();
      if (provider.sendAIChat) {
        await provider.sendAIChat(
          { message: input, context, attachments: userTurn.metadata.attachments },
          (chunk: string) => {
            updateLastTurn(chunk, true);
          },
          (tool: any) => {
            useAIStore.getState().updateLastTurn('', true); // ensure last turn is grabbed
            useAIStore.setState(state => {
              const newTurns = [...state.turns];
              const lastTurn = newTurns[newTurns.length - 1];
              lastTurn.tool_invocations = lastTurn.tool_invocations || [];
              lastTurn.tool_invocations.push(tool);
              if (tool.result && tool.tool_name === '_explainability') {
                 lastTurn.metadata = tool.result;
                 lastTurn.tool_invocations = lastTurn.tool_invocations.filter((t: any) => t.id !== tool.id);
              }
              return { turns: newTurns };
            });
          }
        );
      }
      updateLastTurn(useAIStore.getState().turns[useAIStore.getState().turns.length - 1].content, false);
    } catch (err) {
      updateLastTurn("Sorry, I encountered an error connecting to the AI Platform.", false);
    } finally {
      setIsQuerying(false);
    }
  };

  const isFloating = shellMode === 'floating';
  const isFullscreen = shellMode === 'fullscreen';

  const ocrCapability = capabilities?.find(c => c.id === 'cap_receipt_ocr_01');
  const showOcrBadge = attachments.length > 0 && ocrCapability;

  return (
    <div className={cn(
      "flex flex-col bg-white dark:bg-gray-900 shadow-2xl transition-all",
      isFloating ? "fixed bottom-4 right-4 w-[400px] h-[600px] rounded-xl border border-gray-200 dark:border-gray-800 z-50" : 
      isFullscreen ? "fixed inset-0 z-50" : "h-full"
    )}>
      {/* Header */}
      <div className="h-14 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800 shrink-0 bg-gray-50 dark:bg-gray-950 rounded-t-xl">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 rounded-md bg-blue-600 flex items-center justify-center text-white">
            <Bot size={14} />
          </div>
          <span className="font-semibold text-sm">Enterprise AI</span>
          
          {isRecording && (
            <span className="ml-2 flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider text-red-500 bg-red-50 dark:bg-red-900/20 px-2 py-0.5 rounded-full animate-pulse">
              <Circle size={8} className="fill-current" /> Rec
            </span>
          )}
          {isOfflineMode && (
            <span className="ml-2 flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider text-amber-600 bg-amber-50 dark:bg-amber-900/20 px-2 py-0.5 rounded-full" title="Offline Mode">
              <WifiOff size={10} /> {queueLength > 0 ? `${queueLength} queued` : 'Offline'}
            </span>
          )}
        </div>
        
        {isReplaying ? (
           <div className="flex items-center gap-1 bg-amber-100 dark:bg-amber-900/30 px-2 py-1 rounded-lg">
             <button onClick={() => stepBack()} className="p-1 hover:bg-amber-200 dark:hover:bg-amber-800 rounded text-amber-700 dark:text-amber-400">
               <SkipBack size={14} />
             </button>
             <button onClick={() => stepForward()} className="p-1 hover:bg-amber-200 dark:hover:bg-amber-800 rounded text-amber-700 dark:text-amber-400">
               <SkipForward size={14} />
             </button>
             <button onClick={() => stopReplay()} className="p-1 hover:bg-amber-200 dark:hover:bg-amber-800 rounded text-amber-700 dark:text-amber-400 ml-2 border-l border-amber-200 dark:border-amber-700 pl-2">
               <Square size={14} />
             </button>
           </div>
        ) : (
          <div className="flex items-center gap-1 text-gray-500">
            {!isRecording ? (
               <button 
                 onClick={() => startRecording()}
                 className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors text-red-500 hover:text-red-600"
                 title="Record Session"
               >
                 <Circle size={16} />
               </button>
            ) : (
               <button 
                 onClick={() => stopRecording()}
                 className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors text-gray-500 hover:text-gray-700"
                 title="Stop Recording"
               >
                 <Square size={16} />
               </button>
            )}
            
            {sessions.length > 0 && !isRecording && (
               <button 
                 onClick={() => {
                   startReplay(sessions[sessions.length - 1].id);
                 }}
                 className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors text-amber-500 hover:text-amber-600"
                 title="Replay Last Session"
               >
                 <PlayCircle size={16} />
               </button>
            )}
            
            <div className="w-px h-4 bg-gray-300 dark:bg-gray-700 mx-1" />
            
            <button 
              onClick={() => setShellMode(isFloating ? 'docked' : 'floating')}
              className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
              title={isFloating ? "Dock to sidebar" : "Float"}
            >
              <Settings2 size={16} />
            </button>
            <button 
              onClick={() => setShellMode(isFullscreen ? (isFloating ? 'floating' : 'docked') : 'fullscreen')}
              className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
              title="Toggle Fullscreen"
            >
              {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
            </button>
            <button 
              onClick={toggleShell}
              className="p-1.5 rounded hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
            >
              <X size={16} />
            </button>
          </div>
        )}
      </div>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {turns.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-center text-gray-500 space-y-4">
            <Bot size={40} className="text-gray-300 dark:text-gray-700" />
            <div>
              <p className="font-medium text-gray-900 dark:text-gray-100">How can I assist you?</p>
              <p className="text-sm">I have full context of your current workspace.</p>
            </div>
          </div>
        ) : (
          turns.map((turn) => (
            <AIMessage key={turn.id} turn={turn} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800 rounded-b-xl shrink-0">
        {!chatCapability ? (
          <div className="text-center py-4 bg-orange-50 dark:bg-orange-950/30 text-orange-600 dark:text-orange-400 rounded-lg border border-orange-200 dark:border-orange-800">
            <span className="text-sm font-medium">Chat capability is currently degraded or unavailable offline.</span>
          </div>
        ) : (
          <div className="flex flex-col gap-2">
            {showOcrBadge && (
              <div className="flex items-center gap-2 px-3 py-1.5 bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 rounded-lg text-xs font-medium self-start">
                <Bot size={12} />
                OCR Capability Detected
              </div>
            )}
            
            {attachments.length > 0 && (
              <div className="flex items-center gap-2 overflow-x-auto pb-1">
                {attachments.map((file, i) => (
                  <div key={i} className="flex items-center gap-1.5 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-2.5 py-1.5 rounded-lg text-xs shrink-0">
                    <span className="truncate max-w-[150px]">{file.name}</span>
                    <button onClick={() => removeAttachment(i)} className="p-0.5 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-full">
                      <X size={12} />
                    </button>
                  </div>
                ))}
              </div>
            )}
            
            <div className="relative flex items-center bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-lg shadow-sm focus-within:ring-1 focus-within:ring-blue-500 focus-within:border-blue-500 overflow-hidden transition-all">
              <label className="p-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 cursor-pointer">
                <Paperclip size={18} />
                <input type="file" className="hidden" multiple onChange={handleFileUpload} />
              </label>
              <input 
                type="text" 
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder="Ask AI anything..."
                className="flex-1 bg-transparent border-none py-3 outline-none text-sm text-gray-900 dark:text-gray-100 placeholder-gray-500"
                disabled={isQuerying}
              />
              <button 
                onClick={handleSend}
                disabled={(!input.trim() && attachments.length === 0) || isQuerying}
                className="p-3 text-blue-600 disabled:text-gray-400 hover:text-blue-700 disabled:hover:text-gray-400 transition-colors"
              >
                <Send size={18} />
              </button>
            </div>
          </div>
        )}
        <div className="mt-2 text-center flex flex-col items-center gap-1">
          <span className="text-[10px] text-gray-400 uppercase tracking-wider">
            {chatCapability ? `Powered by PFOS AI • ${chatCapability.version} • Governed Mode` : 'AI operates in governed mode. Context is fully shared.'}
          </span>
        </div>
      </div>
    </div>
  );
}
