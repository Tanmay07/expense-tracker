import { Sparkles, Send, Bot } from 'lucide-react';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { cn } from '../../utils/cn';

export function CopilotPanel({ isOpen, onClose }: { isOpen: boolean, onClose: () => void }) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your AFIP Copilot. How can I assist you with your finances today?' }
  ]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    
    setMessages(prev => [...prev, { role: 'user', content: query }]);
    setQuery('');
    
    // Mock response
    setTimeout(() => {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'I have analyzed your request. Would you like me to initiate a new mission to optimize your cash flow based on this?' 
      }]);
    }, 1000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div 
          initial={{ opacity: 0, x: 300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: 300 }}
          className="fixed right-0 top-0 bottom-0 w-80 md:w-96 border-l border-border bg-background/95 backdrop-blur-xl shadow-2xl z-40 flex flex-col"
        >
          <div className="p-4 border-b border-border flex items-center justify-between bg-card/50">
            <div className="flex items-center gap-2 font-medium">
              <Sparkles className="w-5 h-5 text-blue-500" />
              AI Copilot
            </div>
            <button onClick={onClose} className="text-muted-foreground hover:text-foreground text-sm font-medium">
              Close
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4 space-y-4">
            {messages.map((msg, i) => (
              <div key={i} className={cn(
                "flex gap-3 max-w-[85%]",
                msg.role === 'user' ? "ml-auto flex-row-reverse" : ""
              )}>
                <div className={cn(
                  "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                  msg.role === 'user' ? "bg-gradient-to-tr from-blue-500 to-purple-500" : "bg-secondary text-blue-500"
                )}>
                  {msg.role === 'assistant' && <Bot className="w-4 h-4" />}
                </div>
                <div className={cn(
                  "p-3 rounded-2xl text-sm",
                  msg.role === 'user' 
                    ? "bg-blue-600 text-white rounded-tr-sm" 
                    : "bg-secondary text-foreground rounded-tl-sm"
                )}>
                  {msg.content}
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-border bg-card/50">
            <form onSubmit={handleSubmit} className="relative">
              <input 
                type="text"
                placeholder="Ask about your finances..."
                value={query}
                onChange={e => setQuery(e.target.value)}
                className="w-full pl-4 pr-12 py-3 bg-background border border-border rounded-xl text-sm outline-none focus:border-blue-500 transition-colors"
              />
              <button 
                type="submit"
                disabled={!query.trim()}
                className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 text-blue-500 hover:bg-blue-500/10 rounded-lg transition-colors disabled:opacity-50"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
            <p className="text-[10px] text-center text-muted-foreground mt-2">
              AFIP Copilot can make mistakes. Verify important financial decisions.
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
