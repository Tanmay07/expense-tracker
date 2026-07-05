import { Outlet } from 'react-router-dom';
import { useState } from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CommandPalette } from './CommandPalette';
import { CopilotPanel } from '../features/copilot/CopilotPanel';
import { MessageSquarePlus } from 'lucide-react';

export function Shell() {
  const [copilotOpen, setCopilotOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <Header />
        <main className="flex-1 overflow-y-auto p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>

        <button 
          onClick={() => setCopilotOpen(true)}
          className="fixed bottom-6 right-6 p-4 bg-blue-600 hover:bg-blue-700 text-white rounded-full shadow-lg hover:shadow-xl transition-all z-30"
          aria-label="Open AI Copilot"
        >
          <MessageSquarePlus className="w-6 h-6" />
        </button>
      </div>
      <CommandPalette />
      <CopilotPanel isOpen={copilotOpen} onClose={() => setCopilotOpen(false)} />
    </div>
  );
}
