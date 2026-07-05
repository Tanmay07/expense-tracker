import { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { useContextStore } from '../store/useContextStore';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import { BackendProvider } from '../core/providers/BackendProvider';
import { DeveloperProvider } from '../core/providers/DeveloperProvider';

export function useContextInit() {
  const { currentProvider, activePersona } = useAppStore();
  const setContextData = useContextStore(state => state.setContextData);
  const setLoading = useContextStore(state => state.setLoading);
  const setWorkspaces = useWorkspaceStore(state => state.setWorkspaces);

  useEffect(() => {
    let mounted = true;

    async function loadData() {
      setLoading(true);
      try {
        const provider = currentProvider === 'backend' ? new BackendProvider() : new DeveloperProvider();
        
        const [contexts, layout, actions, workspaces] = await Promise.all([
          provider.getActiveContexts(),
          provider.getAdaptiveDashboardLayout(),
          provider.getQuickActions(),
          provider.getWorkspaces ? provider.getWorkspaces() : Promise.resolve([])
        ]);

        if (mounted) {
          setContextData({ contexts, layout, actions });
          if (workspaces.length > 0) setWorkspaces(workspaces);
        }
      } catch (error) {
        console.error('Failed to load app data:', error);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadData();

    return () => {
      mounted = false;
    };
  }, [currentProvider, activePersona, setContextData, setLoading, setWorkspaces]);
}
