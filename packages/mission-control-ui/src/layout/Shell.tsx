import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { Header } from './Header';
import { CopilotPanel } from '../features/copilot/CopilotPanel';
import { CommandPalette } from './CommandPalette';
import { useState } from 'react';

export function Shell() {
  const [copilotOpen, setCopilotOpen] = useState(false);

  return (
    <div className="flex h-screen bg-background text-foreground overflow-hidden font-sans">
      <Sidebar />
      <div className="flex flex-col flex-1 relative min-w-0">
        <Header toggleCopilot={() => setCopilotOpen(!copilotOpen)} />
        <main className="flex-1 overflow-auto p-6 md:p-8">
          <Outlet />
        </main>
      </div>
      <CopilotPanel isOpen={copilotOpen} onClose={() => setCopilotOpen(false)} />
      <CommandPalette />
    </div>
  );
}
