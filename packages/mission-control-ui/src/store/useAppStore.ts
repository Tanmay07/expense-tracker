import { create } from 'zustand'

interface AppState {
  sidebarOpen: boolean
  toggleSidebar: () => void
  commandPaletteOpen: boolean
  setCommandPaletteOpen: (open: boolean) => void
  devMode: boolean
  toggleDevMode: () => void
}

export const useAppStore = create<AppState>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  commandPaletteOpen: false,
  setCommandPaletteOpen: (open) => set({ commandPaletteOpen: open }),
  devMode: true, // Enabled by default for development as per request
  toggleDevMode: () => set((state) => ({ devMode: !state.devMode })),
}))
