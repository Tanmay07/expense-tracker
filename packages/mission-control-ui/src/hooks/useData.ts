import { useQuery } from '@tanstack/react-query';
import { DashboardService, ExpenseService, MissionService } from '../core/services';
import { useDevStore } from '../store/useDevStore';

// We add activePersonaId to the queryKey so that when the user switches personas
// in Dev Mode, TanStack Query automatically refetches/invalidates the cache!
export function useDashboardMetrics() {
  const activePersonaId = useDevStore(state => state.activePersonaId);
  return useQuery({
    queryKey: ['dashboardMetrics', activePersonaId],
    queryFn: () => DashboardService.getMetrics(),
  });
}

export function useExpenses() {
  const activePersonaId = useDevStore(state => state.activePersonaId);
  return useQuery({
    queryKey: ['expenses', activePersonaId],
    queryFn: () => ExpenseService.getExpenses(),
  });
}

export function useMissions() {
  const activePersonaId = useDevStore(state => state.activePersonaId);
  return useQuery({
    queryKey: ['missions', activePersonaId],
    queryFn: () => MissionService.getMissions(),
  });
}
