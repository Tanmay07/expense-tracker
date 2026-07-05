import { useAppStore } from '../store/useAppStore';
import { useWorkspaceStore } from '../store/useWorkspaceStore';
import { useLocation } from 'react-router-dom';

export function useContextAssembler() {
  const { activePersona, isOfflineMode } = useAppStore();
  const { activeWorkspaceId, selectedEntityId, workspaces } = useWorkspaceStore();
  const location = useLocation();

  const assembleContext = () => {
    // Determine current logical workspace from route if not explicitly set
    let logicalWorkspace = activeWorkspaceId;
    if (!logicalWorkspace) {
      if (location.pathname.includes('/workspaces/')) {
        logicalWorkspace = location.pathname.split('/').pop() || null;
      } else if (location.pathname === '/missions') {
        logicalWorkspace = 'mission_center';
      } else if (location.pathname === '/') {
        logicalWorkspace = 'mission_home';
      }
    }

    const currentWorkspaceData = workspaces.find(w => w.id === logicalWorkspace || w.path.includes(logicalWorkspace || ''));

    return {
      active_workspace: logicalWorkspace,
      workspace_name: currentWorkspaceData?.name || 'Global',
      selected_entity_id: selectedEntityId,
      user_persona: activePersona,
      current_time: new Date().toISOString(),
      is_offline: isOfflineMode,
      current_route: location.pathname
    };
  };

  return { assembleContext };
}
