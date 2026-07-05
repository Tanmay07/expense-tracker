import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export type FeatureFlag = 'investments' | 'analytics' | 'budgets' | 'governance' | 'knowledgeGraph';

interface FeatureFlagState {
  flags: Record<FeatureFlag, boolean>;
  toggleFlag: (flag: FeatureFlag) => void;
}

export const useFeatureFlags = create<FeatureFlagState>()(
  persist(
    (set) => ({
      flags: {
        investments: false,
        analytics: false,
        budgets: false,
        governance: false,
        knowledgeGraph: false,
      },
      toggleFlag: (flag) => set((state) => ({ 
        flags: { ...state.flags, [flag]: !state.flags[flag] } 
      })),
    }),
    { name: 'pfos-feature-flags' }
  )
);
