import { create } from 'zustand';
import type { FinancialContext, AdaptiveDashboardLayout, AdaptiveAction } from '../core/models';

interface ContextState {
  activeContexts: FinancialContext[];
  dashboardLayout: AdaptiveDashboardLayout | null;
  quickActions: AdaptiveAction[];
  isLoading: boolean;
  lastUpdated: number | null;
  setContextData: (data: { contexts: FinancialContext[], layout: AdaptiveDashboardLayout, actions: AdaptiveAction[] }) => void;
  setLoading: (loading: boolean) => void;
}

export const useContextStore = create<ContextState>((set) => ({
  activeContexts: [],
  dashboardLayout: null,
  quickActions: [],
  isLoading: true,
  lastUpdated: null,
  setContextData: (data) => set({
    activeContexts: data.contexts,
    dashboardLayout: data.layout,
    quickActions: data.actions,
    isLoading: false,
    lastUpdated: Date.now()
  }),
  setLoading: (loading) => set({ isLoading: loading })
}));
