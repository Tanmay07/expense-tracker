import type { IDataProvider } from './IDataProvider';
import { BackendProvider } from './BackendProvider';
import { DeveloperProvider } from './DeveloperProvider';
import { useAppStore } from '../../store/useAppStore';

// In a real scenario, OfflineProvider would sit between Backend and Developer
export class ProviderResolver {
  private static backend = new BackendProvider();
  private static developer = new DeveloperProvider();

  static resolve(): IDataProvider {
    const { devMode } = useAppStore.getState();
    
    // For Phase 1 architecture, if dev mode is enabled, we force the DeveloperProvider
    // so we can test the Persona data without relying on the unlinked backend.
    if (devMode) {
      return this.developer;
    }

    // Otherwise, try backend
    return this.backend;
  }
}
