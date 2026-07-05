import { NavLink, Outlet } from 'react-router-dom';
import { Group, Panel, Separator } from 'react-resizable-panels';
import { LayoutDashboard, Target, Activity, Share2, MessageSquare, Menu, Command, PanelRightOpen, PanelRightClose } from 'lucide-react';
import { useWorkspaceStore } from '../../../store/useWorkspaceStore';
import { useAIStore } from '../../../store/useAIStore';
import { UniversalInspector } from './UniversalInspector';
import { AICopilotPanel } from '../../../features/ai/AICopilotPanel';

export function Shell() {
  const { 
    workspaces,
    sidebarSize, 
    inspectorSize, 
    isInspectorOpen, 
    setSidebarSize, 
    setInspectorSize, 
    toggleInspector 
  } = useWorkspaceStore();

  const { isShellOpen, shellMode, toggleShell } = useAIStore();

  const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Mission Home' },
    { to: '/missions', icon: Target, label: 'Mission Center' },
    { to: '/decisions', icon: Activity, label: 'Decision Center' },
    { to: '/timeline', icon: Activity, label: 'Timeline' },
    { to: '/graph', icon: Share2, label: 'Graph Explorer' },
  ];

  return (
    <div className="flex h-screen w-full bg-gray-50 text-gray-900 overflow-hidden dark:bg-gray-950 dark:text-gray-100">
      <Group orientation="horizontal">
        
        {/* Left Sidebar */}
        <Panel 
          defaultSize={sidebarSize} 
          minSize={15} 
          maxSize={25}
          onResize={(size) => setSidebarSize(size)}
          className="flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-800"
        >
          <div className="h-14 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800 shrink-0">
            <span className="font-bold text-base tracking-tight truncate">Mission Control</span>
            <button className="p-1.5 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-500">
              <Menu size={18} />
            </button>
          </div>
          <nav className="flex-1 overflow-y-auto py-3">
            <ul className="space-y-0.5 px-2">
              {navItems.map((item) => (
                <li key={item.to}>
                  <NavLink
                    to={item.to}
                    className={({ isActive }) =>
                      `flex items-center px-3 py-2 rounded-md transition-colors text-sm font-medium ${
                        isActive 
                          ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' 
                          : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                      }`
                    }
                  >
                    <item.icon size={18} className="shrink-0" />
                    <span className="ml-3 truncate">{item.label}</span>
                  </NavLink>
                </li>
              ))}
            </ul>

            {workspaces.length > 0 && (
              <div className="mt-6">
                <div className="px-5 mb-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  Workspaces
                </div>
                <ul className="space-y-0.5 px-2">
                  {workspaces.map((ws) => (
                    <li key={ws.id}>
                      <NavLink
                        to={ws.path}
                        className={({ isActive }) =>
                          `flex items-center px-3 py-2 rounded-md transition-colors text-sm font-medium ${
                            isActive 
                              ? 'bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300' 
                              : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                          }`
                        }
                      >
                        <LayoutDashboard size={18} className="shrink-0 opacity-70" />
                        <span className="ml-3 truncate">{ws.name}</span>
                      </NavLink>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </nav>
        </Panel>

        <Separator className="w-1.5 bg-transparent hover:bg-blue-500/50 active:bg-blue-500 transition-colors cursor-col-resize" />

        {/* Main Canvas */}
        <Panel className="flex flex-col h-full bg-gray-50 dark:bg-gray-950 relative">
          <header className="h-14 flex items-center justify-between px-6 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 shrink-0 z-10">
            <div className="flex-1"></div>
            <div className="flex items-center gap-3">
              <button 
                onClick={toggleShell}
                className="flex items-center text-xs text-white bg-blue-600 dark:bg-blue-700 px-3 py-1.5 rounded-md hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors shadow-sm font-medium"
              >
                <MessageSquare size={14} className="mr-1.5" />
                <span>Ask AI (Cmd+J)</span>
              </button>
              <button className="flex items-center text-xs text-gray-500 bg-gray-100 dark:bg-gray-800 px-2.5 py-1.5 rounded-md hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors border border-gray-200 dark:border-gray-700">
                <Command size={14} className="mr-1.5" />
                <span>Cmd + K</span>
              </button>
              
              <div className="w-px h-4 bg-gray-300 dark:bg-gray-700 mx-1"></div>
              
              <button 
                onClick={toggleInspector}
                className={`p-1.5 rounded-md transition-colors ${isInspectorOpen ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/30' : 'text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800'}`}
                title="Toggle Inspector (Cmd+I)"
              >
                {isInspectorOpen ? <PanelRightClose size={18} /> : <PanelRightOpen size={18} />}
              </button>

              <div className="w-7 h-7 bg-blue-600 rounded-full flex items-center justify-center text-white text-xs font-bold ml-1">
                TA
              </div>
            </div>
          </header>

          <main className="flex-1 overflow-auto p-6 relative">
            <Outlet />
          </main>
        </Panel>

        {/* Universal Inspector Panel */}
        {isInspectorOpen && (
          <>
            <Separator className="w-1.5 bg-transparent hover:bg-blue-500/50 active:bg-blue-500 transition-colors cursor-col-resize z-20" />
            <Panel 
              defaultSize={inspectorSize} 
              minSize={20} 
              maxSize={40}
              onResize={(size) => setInspectorSize(size)}
              className="flex flex-col bg-white dark:bg-gray-900 border-l border-gray-200 dark:border-gray-800 z-10"
            >
              <UniversalInspector />
            </Panel>
          </>
        )}

        {/* AI Copilot Panel (Docked) */}
        {isShellOpen && shellMode === 'docked' && (
          <>
            <Separator className="w-1.5 bg-transparent hover:bg-blue-500/50 active:bg-blue-500 transition-colors cursor-col-resize z-20" />
            <Panel 
              defaultSize={30} 
              minSize={25} 
              maxSize={50}
              className="flex flex-col z-10 border-l border-gray-200 dark:border-gray-800"
            >
              <AICopilotPanel />
            </Panel>
          </>
        )}

      </Group>

      {/* AI Copilot Panel (Floating / Fullscreen) */}
      {isShellOpen && shellMode !== 'docked' && (
        <AICopilotPanel />
      )}
    </div>
  );
}
