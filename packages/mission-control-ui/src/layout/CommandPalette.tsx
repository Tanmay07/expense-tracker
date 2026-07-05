import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';

// Simple implementation for now. In a real app, use cmDK or similar.
export function CommandPalette() {
  const { commandPaletteOpen, setCommandPaletteOpen } = useAppStore();
  const [query, setQuery] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setCommandPaletteOpen(!commandPaletteOpen);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, [commandPaletteOpen, setCommandPaletteOpen]);

  if (!commandPaletteOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] sm:pt-[20vh]">
      <div className="fixed inset-0 bg-background/80 backdrop-blur-sm" onClick={() => setCommandPaletteOpen(false)} />
      <div className="relative w-full max-w-xl rounded-xl border border-border bg-card shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="flex items-center px-4 border-b border-border">
          <Search className="w-5 h-5 text-muted-foreground mr-3" />
          <input
            autoFocus
            className="flex-1 h-14 bg-transparent outline-none text-foreground placeholder:text-muted-foreground"
            placeholder="Search commands, navigate, or ask Copilot..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button onClick={() => setCommandPaletteOpen(false)} className="text-muted-foreground hover:text-foreground">
            <X className="w-4 h-4" />
          </button>
        </div>
        <div className="max-h-[60vh] overflow-y-auto p-2">
          <div className="px-2 py-1.5 text-xs font-semibold text-muted-foreground">Navigation</div>
          {[
            { label: 'Go to Home', path: '/' },
            { label: 'Go to Expenses', path: '/expenses' },
            { label: 'Go to Missions', path: '/missions' },
            { label: 'Go to Settings', path: '/settings' },
          ].filter(item => item.label.toLowerCase().includes(query.toLowerCase())).map((item) => (
            <button
              key={item.path}
              className="w-full text-left flex items-center px-3 py-3 text-sm rounded-md hover:bg-secondary transition-colors"
              onClick={() => {
                navigate(item.path);
                setCommandPaletteOpen(false);
              }}
            >
              {item.label}
            </button>
          ))}
          {query.length > 2 && (
            <>
              <div className="px-2 py-1.5 mt-2 text-xs font-semibold text-muted-foreground">Ask Copilot</div>
              <button className="w-full text-left flex items-center px-3 py-3 text-sm rounded-md hover:bg-secondary text-blue-400 transition-colors">
                Ask AI: "{query}"
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
