import type { IDataProvider } from './IDataProvider';
import type { Expense, Mission, DashboardMetrics } from '../models';
import { GROWTH_PERSONA, STABILIZATION_PERSONA } from '../../data/personas';
import { useDevStore } from '../../store/useDevStore';

export class DeveloperProvider implements IDataProvider {
  private getPersona() {
    const { activePersonaId } = useDevStore.getState();
    return activePersonaId === GROWTH_PERSONA.id ? GROWTH_PERSONA : STABILIZATION_PERSONA;
  }

  private async simulateDelay() {
    const { mockNetworkDelay } = useDevStore.getState();
    return new Promise(resolve => setTimeout(resolve, mockNetworkDelay));
  }

  async getExpenses(): Promise<Expense[]> {
    await this.simulateDelay();
    return this.getPersona().expenses;
  }

  async getMissions(): Promise<Mission[]> {
    await this.simulateDelay();
    return this.getPersona().missions;
  }

  async getDashboardMetrics(): Promise<DashboardMetrics> {
    await this.simulateDelay();
    return this.getPersona().metrics;
  }
}
