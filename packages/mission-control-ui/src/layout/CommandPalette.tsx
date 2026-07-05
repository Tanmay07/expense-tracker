import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Command } from 'cmdk';
import { Search, Calculator, Target, Briefcase, Settings, Laptop, PiggyBank, BrainCircuit } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };
    document.addEventListener('keydown', down);
    return () => document.removeEventListener('keydown', down);
  }, []);

  const handleSelect = (path: string) => {
    setOpen(false);
    navigate(path);
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-start justify-center pt-[20vh] px-4">
          <motion.div 
            initial={{ opacity: 0 }} 
            animate={{ opacity: 1 }} 
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
            onClick={() => setOpen(false)}
          />
          <motion.div 
            initial={{ opacity: 0, scale: 0.95, y: -20 }} 
            animate={{ opacity: 1, scale: 1, y: 0 }} 
            exit={{ opacity: 0, scale: 0.95, y: -20 }}
            className="relative w-full max-w-xl bg-card border border-border shadow-2xl rounded-xl overflow-hidden"
          >
            <Command label="Global Command Palette" shouldFilter={true} className="w-full">
              <div className="flex items-center px-4 py-3 border-b border-border">
                <Search className="w-5 h-5 text-muted-foreground mr-3 shrink-0" />
                <Command.Input 
                  value={search}
                  onValueChange={setSearch}
                  placeholder="Search missions, goals, transactions, or commands..." 
                  className="w-full bg-transparent border-none outline-none placeholder:text-muted-foreground text-foreground text-lg"
                  autoFocus
                />
              </div>

              <Command.List className="max-h-[60vh] overflow-y-auto p-2 scrollbar-thin scrollbar-thumb-secondary">
                <Command.Empty className="py-12 text-center text-muted-foreground text-sm">
                  No results found for "{search}".
                </Command.Empty>

                <Command.Group heading="Workspaces" className="px-2 py-3 text-xs font-medium text-muted-foreground [&_[cmdk-group-heading]]:mb-2">
                  <Command.Item onSelect={() => handleSelect('/')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <Laptop className="w-4 h-4 shrink-0" />
                    Home Dashboard
                  </Command.Item>
                  <Command.Item onSelect={() => handleSelect('/expenses')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <Calculator className="w-4 h-4 shrink-0" />
                    Expense Management
                  </Command.Item>
                  <Command.Item onSelect={() => handleSelect('/missions')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <Target className="w-4 h-4 shrink-0" />
                    Mission Center
                  </Command.Item>
                  <Command.Item onSelect={() => handleSelect('/investments')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <Briefcase className="w-4 h-4 shrink-0" />
                    Investment Portfolio
                  </Command.Item>
                  <Command.Item onSelect={() => handleSelect('/budgets')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <PiggyBank className="w-4 h-4 shrink-0" />
                    Budget Planner
                  </Command.Item>
                </Command.Group>

                <Command.Group heading="Settings & Admin" className="px-2 py-3 text-xs font-medium text-muted-foreground [&_[cmdk-group-heading]]:mb-2 border-t border-border mt-1">
                  <Command.Item onSelect={() => handleSelect('/settings')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <Settings className="w-4 h-4 shrink-0" />
                    Developer Workspace
                  </Command.Item>
                  <Command.Item onSelect={() => handleSelect('/knowledge-graph')} className="flex items-center gap-3 px-3 py-2.5 rounded-md cursor-pointer hover:bg-secondary text-sm text-foreground transition-colors aria-selected:bg-secondary aria-selected:text-blue-400">
                    <BrainCircuit className="w-4 h-4 shrink-0" />
                    Knowledge Graph Explorer
                  </Command.Item>
                </Command.Group>
              </Command.List>
            </Command>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
