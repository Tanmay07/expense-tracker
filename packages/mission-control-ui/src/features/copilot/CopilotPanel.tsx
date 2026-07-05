import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bot, X, Send, Command, Target } from 'lucide-react';
import { cn } from '../../utils/cn';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isStreaming?: boolean;
}

const SUGGESTED_PROMPTS = [
  "Analyze my spending this month",
  "How much can I put towards debt?",
  "Launch tax harvesting mission",
  "Explain the Wash Sale rule"
];

export function CopilotPanel({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hello! I am your Financial AI Copilot. How can I assist you with your finances today?',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  const handleSend = async (text: string = input) => {
    if (!text.trim()) return;

    const userMsg: Message = { id: Date.now().toString(), role: 'user', content: text, timestamp: new Date() };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsTyping(true);

    // Simulate streaming response
    setTimeout(() => {
      const responseContent = "I've analyzed your recent transactions. You have a significantly higher than average spend in the 'Dining' category this week. Would you like me to launch a strict budgeting mission for the remainder of the month to keep you on track?";
      
      const assistantMsgId = (Date.now() + 1).toString();
      setMessages(prev => [...prev, { id: assistantMsgId, role: 'assistant', content: '', timestamp: new Date(), isStreaming: true }]);
      setIsTyping(false);

      let currentLength = 0;
      const interval = setInterval(() => {
        currentLength += 3;
        if (currentLength >= responseContent.length) {
          clearInterval(interval);
          setMessages(prev => prev.map(m => m.id === assistantMsgId ? { ...m, content: responseContent, isStreaming: false } : m));
        } else {
          setMessages(prev => prev.map(m => m.id === assistantMsgId ? { ...m, content: responseContent.slice(0, currentLength) } : m));
        }
      }, 30);
    }, 1000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ x: 400, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          exit={{ x: 400, opacity: 0 }}
          transition={{ type: 'spring', damping: 25, stiffness: 200 }}
          className="fixed top-0 right-0 w-full md:w-[400px] h-screen bg-card border-l border-border shadow-2xl flex flex-col z-40"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-border bg-card/80 backdrop-blur-md">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20">
                <Bot className="w-4 h-4 text-blue-500" />
              </div>
              <div>
                <h2 className="font-semibold text-sm">AI Copilot</h2>
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                  Online (GPT-4o)
                </div>
              </div>
            </div>
            <button onClick={onClose} className="p-2 rounded-md hover:bg-secondary text-muted-foreground transition-colors">
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto p-4 space-y-6" ref={scrollRef}>
            {messages.map((msg) => (
              <div key={msg.id} className={cn("flex flex-col max-w-[85%]", msg.role === 'user' ? "ml-auto items-end" : "mr-auto items-start")}>
                <div className={cn("p-3 rounded-2xl text-sm shadow-sm", 
                  msg.role === 'user' 
                    ? "bg-blue-500 text-white rounded-br-none" 
                    : "bg-secondary text-foreground rounded-tl-none border border-border"
                )}>
                  {msg.content}
                  {msg.isStreaming && <span className="inline-block w-1.5 h-4 ml-1 bg-current animate-pulse align-middle" />}
                </div>
                <span className="text-[10px] text-muted-foreground mt-1 px-1">
                  {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
                
                {/* Simulated Widget in Copilot */}
                {msg.role === 'assistant' && !msg.isStreaming && msg.content.includes('strict budgeting mission') && (
                  <div className="mt-3 w-full p-4 bg-card border border-border rounded-xl shadow-sm relative overflow-hidden group">
                     <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
                     <div className="flex items-center gap-2 mb-2">
                       <Target className="w-4 h-4 text-blue-500" />
                       <span className="font-semibold text-sm">Budget Lockdown</span>
                     </div>
                     <p className="text-xs text-muted-foreground mb-3">Freeze discretionary spending until EOM.</p>
                     <button className="w-full py-1.5 bg-blue-500/10 text-blue-500 text-xs font-medium rounded hover:bg-blue-500/20 transition-colors">
                       Review Mission
                     </button>
                  </div>
                )}
              </div>
            ))}
            
            {isTyping && (
              <div className="flex flex-col mr-auto items-start max-w-[85%]">
                <div className="p-3 rounded-2xl bg-secondary text-foreground rounded-tl-none border border-border shadow-sm flex gap-1">
                  <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.3s]"></span>
                  <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce [animation-delay:-0.15s]"></span>
                  <span className="w-1.5 h-1.5 bg-muted-foreground rounded-full animate-bounce"></span>
                </div>
              </div>
            )}
          </div>

          {/* Context Indicators */}
          <div className="px-4 py-2 border-t border-border bg-secondary/30 flex gap-2 overflow-x-auto scrollbar-none">
            <span className="shrink-0 flex items-center gap-1 px-2 py-1 bg-background border border-border rounded text-[10px] font-medium text-muted-foreground">
              <Command className="w-3 h-3" /> Workspace Context Attached
            </span>
          </div>

          {/* Input Area */}
          <div className="p-4 bg-card border-t border-border">
            {messages.length < 3 && !isTyping && (
              <div className="flex flex-wrap gap-2 mb-3">
                {SUGGESTED_PROMPTS.map(p => (
                  <button 
                    key={p} 
                    onClick={() => handleSend(p)}
                    className="px-2.5 py-1 text-xs bg-secondary text-secondary-foreground rounded-full hover:bg-secondary/80 transition-colors border border-border"
                  >
                    {p}
                  </button>
                ))}
              </div>
            )}
            <div className="relative flex items-center">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && handleSend()}
                placeholder="Ask Copilot anything..."
                className="w-full bg-secondary border border-border rounded-xl py-3 pl-4 pr-12 text-sm outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all placeholder:text-muted-foreground"
              />
              <button 
                onClick={() => handleSend()}
                disabled={!input.trim() || isTyping}
                className="absolute right-2 p-1.5 bg-blue-500 text-white rounded-lg disabled:opacity-50 disabled:cursor-not-allowed hover:bg-blue-600 transition-colors"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
