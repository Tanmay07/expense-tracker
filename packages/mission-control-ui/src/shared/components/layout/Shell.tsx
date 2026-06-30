import { useState } from 'react';
import type { ReactNode } from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Target, Activity, Share2, MessageSquare, Menu, Command } from 'lucide-react';

interface ShellProps {
  children: ReactNode;
}

export function Shell({ children }: ShellProps) {
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Mission Home' },
    { to: '/missions', icon: Target, label: 'Mission Center' },
    { to: '/decisions', icon: Activity, label: 'Decision Center' },
    { to: '/timeline', icon: Activity, label: 'Timeline' },
    { to: '/copilot', icon: MessageSquare, label: 'AI Copilot' },
    { to: '/graph', icon: Share2, label: 'Graph Explorer' },
  ];

  return (
    <div className="flex h-screen bg-gray-50 text-gray-900 overflow-hidden dark:bg-gray-950 dark:text-gray-100">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} transition-all duration-300 border-r bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 flex flex-col`}>
        <div className="h-16 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800">
          {isSidebarOpen && <span className="font-bold text-lg tracking-tight">Mission Control</span>}
          <button onClick={() => setSidebarOpen(!isSidebarOpen)} className="p-2 rounded hover:bg-gray-100 dark:hover:bg-gray-800">
            <Menu size={20} />
          </button>
        </div>
        <nav className="flex-1 overflow-y-auto py-4">
          <ul className="space-y-1 px-2">
            {navItems.map((item) => (
              <li key={item.to}>
                <NavLink
                  to={item.to}
                  className={({ isActive }) =>
                    `flex items-center px-3 py-2 rounded-md transition-colors ${
                      isActive ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                    }`
                  }
                >
                  <item.icon size={20} className="shrink-0" />
                  {isSidebarOpen && <span className="ml-3 truncate">{item.label}</span>}
                </NavLink>
              </li>
            ))}
          </ul>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header */}
        <header className="h-16 flex items-center justify-between px-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
          <div className="flex-1"></div>
          <div className="flex items-center space-x-4">
            <button className="flex items-center text-sm text-gray-500 bg-gray-100 dark:bg-gray-800 px-3 py-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
              <Command size={16} className="mr-2" />
              <span>Cmd + K</span>
            </button>
            <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
              TA
            </div>
          </div>
        </header>

        {/* Scrollable Content */}
        <div className="flex-1 overflow-auto p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
