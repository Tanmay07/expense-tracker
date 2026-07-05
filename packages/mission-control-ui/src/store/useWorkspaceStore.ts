import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface WidgetConfig {
  id: string;
  widget_type: string;
  title: string;
  data_source: string;
  layout: { w: number; h: number; x: number; y: number };
  settings: Record<string, any>;
}

export interface WorkspaceSnapshot {
  id: string;
  name: string;
  created_at: string;
  widgets: WidgetConfig[];
  layout_config: { sidebar_width: number; inspector_width: number; [key: string]: any };
}

export interface WorkspaceModel {
  id: string;
  name: string;
  description: string;
  icon: string;
  path: string;
  is_default: boolean;
  active_snapshot_id?: string;
  snapshots: WorkspaceSnapshot[];
  metadata: Record<string, any>;
}

interface WorkspaceState {
  workspaces: WorkspaceModel[];
  activeWorkspaceId: string | null;
  sidebarSize: number;
  inspectorSize: number;
  isInspectorOpen: boolean;
  selectedEntityId: string | null;
  setWorkspaces: (workspaces: WorkspaceModel[]) => void;
  setActiveWorkspace: (id: string) => void;
  setSidebarSize: (size: any) => void;
  setInspectorSize: (size: any) => void;
  toggleInspector: () => void;
  setSelectedEntity: (id: string | null) => void;
}

export const useWorkspaceStore = create<WorkspaceState>()(
  persist(
    (set) => ({
      workspaces: [],
      activeWorkspaceId: null,
      sidebarSize: 20 as any, // Will adapt to react-resizable-panels v4 format
      inspectorSize: 25 as any,
      isInspectorOpen: false,
      selectedEntityId: null,
      setWorkspaces: (workspaces) => set({ workspaces }),
      setActiveWorkspace: (id) => set({ activeWorkspaceId: id }),
      setSidebarSize: (size) => set({ sidebarSize: size }),
      setInspectorSize: (size) => set({ inspectorSize: size }),
      toggleInspector: () => set((state) => ({ isInspectorOpen: !state.isInspectorOpen })),
      setSelectedEntity: (id) => set({ selectedEntityId: id, isInspectorOpen: !!id })
    }),
    {
      name: 'pfos-workspace-storage'
    }
  )
);
