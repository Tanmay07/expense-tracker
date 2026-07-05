import { Menu, Search, Bell } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';

export function Header() {
  const { toggleSidebar, setCommandPaletteOpen } = useAppStore();

  return (
    <header className="h-16 flex items-center justify-between px-4 border-b border-border bg-background/80 backdrop-blur-md sticky top-0 z-10">
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="p-2 -ml-2 text-muted-foreground hover:text-foreground rounded-md hover:bg-secondary/50 transition-colors"
          aria-label="Toggle Sidebar"
        >
          <Menu className="w-5 h-5" />
        </button>
        
        <button 
          onClick={() => setCommandPaletteOpen(true)}
          className="flex items-center gap-2 px-3 py-1.5 text-sm text-muted-foreground bg-secondary/30 hover:bg-secondary/50 rounded-md border border-border/50 transition-colors w-64"
        >
          <Search className="w-4 h-4" />
          <span>Search...</span>
          <kbd className="ml-auto text-xs font-mono bg-background px-1.5 py-0.5 rounded border border-border">⌘K</kbd>
        </button>
      </div>
      
      <div className="flex items-center gap-4">
        <button className="p-2 text-muted-foreground hover:text-foreground rounded-full hover:bg-secondary/50 transition-colors relative">
          <Bell className="w-5 h-5" />
          <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-blue-500 rounded-full"></span>
        </button>
        <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500"></div>
      </div>
    </header>
  );
}
