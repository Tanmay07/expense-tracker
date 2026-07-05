import { useEffect, useCallback } from 'react';
import { useAIStore } from './useAIStore';
import { useAppStore } from './useAppStore';

export function useOfflineSync() {
  const { offline_queue, syncStatus, setSyncStatus, removeAction } = useAIStore();
  const { isOfflineMode } = useAppStore();

  const processQueue = useCallback(async () => {
    if (offline_queue.length === 0 || isOfflineMode || syncStatus === 'SYNCING') return;

    setSyncStatus('SYNCING');
    
    // Process items sequentially to maintain order
    for (const action of offline_queue) {
      try {
        // In a real app we'd dispatch to the appropriate BFF endpoint
        // e.g. await fetch('/api/bff/sync', { method: 'POST', body: JSON.stringify(action) })
        console.log('[OfflineSync] Processing action:', action.id, action.type);
        
        // Simulate network delay
        await new Promise(r => setTimeout(r, 800));
        
        // Remove on success
        removeAction(action.id);
      } catch (err) {
        console.error('[OfflineSync] Failed to process action:', action.id);
        // On failure, we stop processing the queue to maintain order
        // The action's retryCount would be incremented in a full implementation
        setSyncStatus('ERROR');
        return;
      }
    }
    
    setSyncStatus('IDLE');
  }, [offline_queue, isOfflineMode, syncStatus, setSyncStatus, removeAction]);

  useEffect(() => {
    // Automatically try to sync when we come back online
    if (!isOfflineMode && offline_queue.length > 0) {
      processQueue();
    }
  }, [isOfflineMode, offline_queue.length, processQueue]);

  return {
    queueLength: offline_queue.length,
    syncStatus,
    forceSync: processQueue
  };
}
