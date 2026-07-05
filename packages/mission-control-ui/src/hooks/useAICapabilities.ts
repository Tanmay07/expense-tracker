import { useQuery } from '@tanstack/react-query';
import { useAppStore } from '../store/useAppStore';
import type { AICapability } from '../core/models';

export function useAICapabilities() {
  const getProvider = useAppStore(state => state.getProvider);
  const isOfflineMode = useAppStore(state => state.isOfflineMode);

  return useQuery<AICapability[], Error>({
    queryKey: ['aiCapabilities'],
    queryFn: async () => {
      const provider = getProvider();
      if (!provider.getAICapabilities) {
        return [];
      }
      return provider.getAICapabilities();
    },
    // Cache capabilities for a long time (e.g. 10 minutes)
    staleTime: 10 * 60 * 1000,
    // Automatically refetch in the background
    refetchInterval: 15 * 60 * 1000,
    // If we're offline, use cached data if available, but queryFn might fail if no cache
    // In a real app we might intercept the error or rely on the provider to handle offline caching
    select: (data) => {
      if (isOfflineMode) {
        return data.filter(cap => cap.offline_availability);
      }
      return data;
    }
  });
}
