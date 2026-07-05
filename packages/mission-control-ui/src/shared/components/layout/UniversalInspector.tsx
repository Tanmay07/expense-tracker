import { X, Info, History, Database, Network } from 'lucide-react';
import { useWorkspaceStore } from '../../../store/useWorkspaceStore';

export function UniversalInspector() {
  const { selectedEntityId, toggleInspector } = useWorkspaceStore();

  return (
    <div className="flex flex-col h-full">
      {/* Header */}
      <div className="h-14 flex items-center justify-between px-4 border-b border-gray-200 dark:border-gray-800 shrink-0">
        <h2 className="font-semibold text-sm">Universal Inspector</h2>
        <button 
          onClick={toggleInspector}
          className="p-1 rounded-md text-gray-500 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
        >
          <X size={16} />
        </button>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto p-4">
        {selectedEntityId ? (
          <div className="space-y-6">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Database size={16} className="text-blue-500" />
                <h3 className="font-medium text-sm">Entity Metadata</h3>
              </div>
              <div className="bg-gray-50 dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-md p-3 text-xs font-mono text-gray-600 dark:text-gray-400 break-all">
                ID: {selectedEntityId}
              </div>
            </div>
            
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Network size={16} className="text-purple-500" />
                <h3 className="font-medium text-sm">Knowledge Graph</h3>
              </div>
              <p className="text-sm text-gray-500">Related nodes will appear here.</p>
            </div>

            <div>
              <div className="flex items-center gap-2 mb-2">
                <History size={16} className="text-emerald-500" />
                <h3 className="font-medium text-sm">Audit Trail</h3>
              </div>
              <p className="text-sm text-gray-500">Recent changes and decisions.</p>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-center text-gray-500 space-y-3">
            <Info size={32} className="text-gray-400" />
            <p className="text-sm">Select any widget, transaction, or mission to inspect its details.</p>
          </div>
        )}
      </div>
    </div>
  );
}
