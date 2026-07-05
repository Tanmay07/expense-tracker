import type { IDataProvider } from './IDataProvider';
import type { Expense, Mission, DashboardMetrics } from '../models';

export class BackendProvider implements IDataProvider {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  async getExpenses(): Promise<Expense[]> {
    const res = await fetch(`${this.baseUrl}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch expenses');
    return res.json();
  }

  async getMissions(): Promise<Mission[]> {
    const res = await fetch(`${this.baseUrl}/missions`);
    if (!res.ok) throw new Error('Failed to fetch missions');
    return res.json();
  }

  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const res = await fetch(`${this.baseUrl}/dashboard/metrics`);
    if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
    return res.json();
  }
}
