import { useEffect } from 'react';
import { useAppStore } from '../store/useAppStore';
import { useContextStore } from '../store/useContextStore';
import { BackendProvider } from '../core/providers/BackendProvider';
import { DeveloperProvider } from '../core/providers/DeveloperProvider';

export function useContextInit() {
  const { currentProvider, activePersona } = useAppStore();
  const setContextData = useContextStore(state => state.setContextData);
  const setLoading = useContextStore(state => state.setLoading);

  useEffect(() => {
    let mounted = true;

    async function loadContext() {
      setLoading(true);
      try {
        const provider = currentProvider === 'backend' ? new BackendProvider() : new DeveloperProvider();
        
        const [contexts, layout, actions] = await Promise.all([
          provider.getActiveContexts(),
          provider.getAdaptiveDashboardLayout(),
          provider.getQuickActions()
        ]);

        if (mounted) {
          setContextData({ contexts, layout, actions });
        }
      } catch (error) {
        console.error('Failed to load context:', error);
        // Fallback state or error handling could go here
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    }

    loadContext();

    return () => {
      mounted = false;
    };
  }, [currentProvider, activePersona, setContextData, setLoading]); // Re-run when provider or persona changes
}
