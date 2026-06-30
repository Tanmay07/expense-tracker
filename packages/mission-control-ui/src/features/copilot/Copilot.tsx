import { useState } from 'react';
import { Send, Sparkles } from 'lucide-react';

export function Copilot() {
  const [messages, setMessages] = useState([
    { id: 1, type: 'bot', text: 'Hello! I am your PFOS AI Copilot. How can I assist you with your financial missions today?' }
  ]);
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { id: Date.now(), type: 'user', text: input }]);
    setInput('');
    setTimeout(() => {
      setMessages(prev => [...prev, { id: Date.now(), type: 'bot', text: 'Based on the Decision Registry, this strategy would require an operational review. Shall I prepare a simulation?' }]);
    }, 1000);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)] max-w-4xl mx-auto bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800 flex items-center">
        <Sparkles size={20} className="text-blue-600 mr-2" />
        <h2 className="font-bold text-lg">AI Copilot Workspace</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] p-3 rounded-2xl ${msg.type === 'user' ? 'bg-blue-600 text-white rounded-br-none' : 'bg-gray-100 dark:bg-gray-800 rounded-bl-none'}`}>
              {msg.text}
            </div>
          </div>
        ))}
      </div>

      <div className="p-4 border-t border-gray-200 dark:border-gray-800">
        <div className="flex items-center space-x-2">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
            placeholder="Ask a question, run a simulation, or compare strategies..." 
            className="flex-1 p-3 rounded-lg border border-gray-300 dark:border-gray-700 bg-transparent focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button onClick={handleSend} className="p-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors">
            <Send size={20} />
          </button>
        </div>
      </div>
    </div>
  );
}
