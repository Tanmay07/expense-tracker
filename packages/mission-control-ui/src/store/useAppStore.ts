import { create } from 'zustand'

export type ProviderType = 'backend' | 'developer' | 'offline';

interface AppState {
  sidebarOpen: boolean
  toggleSidebar: () => void
  commandPaletteOpen: boolean
  setCommandPaletteOpen: (open: boolean) => void
  devMode: boolean
  toggleDevMode: () => void
  currentProvider: ProviderType
  setCurrentProvider: (provider: ProviderType) => void
  activePersona: string
  setActivePersona: (persona: string) => void
  isOfflineMode: boolean
  setOfflineMode: (offline: boolean) => void
  getProvider: () => any
}

import { BackendProvider } from '../core/providers/BackendProvider'
import { DeveloperProvider } from '../core/providers/DeveloperProvider'

export const useAppStore = create<AppState>((set, get) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  commandPaletteOpen: false,
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  devMode: true,
  toggleDevMode: () => set((state) => ({ devMode: !state.devMode })),
  currentProvider: 'developer',
  setCurrentProvider: (provider) => set({ currentProvider: provider }),
  activePersona: 'growth-1',
  setActivePersona: (persona) => set({ activePersona: persona }),
  isOfflineMode: false,
  setOfflineMode: (offline) => set({ isOfflineMode: offline }),
  getProvider: () => {
    const isDev = get().currentProvider === 'developer';
    if (isDev) {
      return new DeveloperProvider();
    }
    return new BackendProvider();
  }
}))
