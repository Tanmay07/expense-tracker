import { Link, useLocation } from 'react-router-dom';
import { Home, CreditCard, Activity, Target, Shield, Settings, Lightbulb, PieChart, Database, Coins } from 'lucide-react';
import { useAppStore } from '../store/useAppStore';
import { cn } from '../utils/cn';

const NAV_ITEMS = [
  { icon: Home, label: 'Home', path: '/' },
  { icon: CreditCard, label: 'Expenses', path: '/expenses' },
  { icon: Target, label: 'Mission Center', path: '/missions' },
  { icon: Activity, label: 'Investments', path: '/investments' },
  { icon: PieChart, label: 'Analytics', path: '/analytics' },
  { icon: Coins, label: 'Budgets', path: '/budgets' },
  { icon: Shield, label: 'Governance', path: '/governance' },
  { icon: Database, label: 'Knowledge Graph', path: '/knowledge-graph' },
];

export function Sidebar() {
  const { sidebarOpen } = useAppStore();
  const location = useLocation();

  return (
    <aside
      className={cn(
        "flex flex-col border-r border-border bg-background transition-all duration-300",
        sidebarOpen ? "w-64" : "w-16"
      )}
    >
      <div className="flex items-center justify-center h-16 border-b border-border">
        {sidebarOpen ? (
          <span className="text-lg font-bold tracking-tight">Mission Control</span>
        ) : (
          <Lightbulb className="w-6 h-6 text-primary" />
        )}
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={cn(
                "flex items-center px-3 py-2 rounded-md transition-colors",
                isActive 
                  ? "bg-secondary text-secondary-foreground font-medium" 
                  : "text-muted-foreground hover:bg-secondary/50 hover:text-foreground",
                !sidebarOpen && "justify-center"
              )}
            >
              <item.icon className="w-5 h-5 shrink-0" />
              {sidebarOpen && <span className="ml-3 truncate">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="p-3 border-t border-border">
        <Link
          to="/settings"
          className={cn(
            "flex items-center px-3 py-2 rounded-md transition-colors text-muted-foreground hover:bg-secondary/50 hover:text-foreground",
            !sidebarOpen && "justify-center"
          )}
        >
          <Settings className="w-5 h-5 shrink-0" />
          {sidebarOpen && <span className="ml-3">Settings</span>}
        </Link>
      </div>
    </aside>
  );
}
