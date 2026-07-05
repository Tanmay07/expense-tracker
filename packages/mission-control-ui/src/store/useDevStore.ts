import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { GROWTH_PERSONA } from '../data/personas';

interface DevStoreState {
  activePersonaId: string;
  setActivePersonaId: (id: string) => void;
  mockNetworkDelay: number;
  setMockNetworkDelay: (delay: number) => void;
}

export const useDevStore = create<DevStoreState>()(
  persist(
    (set) => ({
      activePersonaId: GROWTH_PERSONA.id,
      setActivePersonaId: (id) => set({ activePersonaId: id }),
      mockNetworkDelay: 500, // ms
      setMockNetworkDelay: (delay) => set({ mockNetworkDelay: delay }),
    }),
    { name: 'pfos-dev-storage' }
  )
);
