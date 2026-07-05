import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Loader2, Plus } from 'lucide-react';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import type { WidgetConfig } from '../store/useWorkspaceStore';
import { WidgetGrid } from '../features/workspace/WidgetGrid';

export function WorkspaceView() {
  const { id } = useParams<{ id: string }>();
  const { workspaces } = useWorkspaceStore();
  const [widgets, setWidgets] = useState<WidgetConfig[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // In a real app, this would fetch the workspace layout from the BFF
  // For now, we look it up in the store (which might be populated from BFF in App.tsx)
  useEffect(() => {
    setIsLoading(true);
    // Simulate network delay
    const timer = setTimeout(() => {
      const ws = workspaces.find(w => w.id === `ws_${id}` || w.path.includes(id || ''));
      if (ws && ws.snapshots.length > 0) {
        setWidgets(ws.snapshots[0].widgets);
      } else {
        // Fallback widgets if not found
        setWidgets([
          { id: "w_fallback_1", widget_type: "KPI", title: "Total Value", data_source: "mock.total", layout: { w: 3, h: 1, x: 0, y: 0 }, settings: {} },
          { id: "w_fallback_2", widget_type: "NOTE", title: "Scratchpad", data_source: "mock.note", layout: { w: 3, h: 2, x: 3, y: 0 }, settings: { content: "Draft ideas here..." } }
        ]);
      }
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [id, workspaces]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center h-full gap-4 text-gray-500">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
        <p className="text-sm font-medium animate-pulse">Loading Workspace Layout...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight capitalize">{id} Workspace</h1>
          <p className="text-gray-500 mt-1">Manage and inspect your financial widgets.</p>
        </div>
        <div className="flex items-center gap-3">
          <button 
            onClick={() => alert('Snapshot saved to offline storage!')}
            className="flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-700 dark:text-gray-300 text-sm font-medium rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors shadow-sm"
          >
            Save Snapshot
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors shadow-sm">
            <Plus size={16} />
            Add Widget
          </button>
        </div>
      </div>

      <WidgetGrid widgets={widgets} onWidgetsChange={setWidgets} />
    </div>
  );
}
