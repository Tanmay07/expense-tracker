import type { Expense, Mission, DashboardMetrics } from '../models';

export interface IDataProvider {
  getExpenses(): Promise<Expense[]>;
  getMissions(): Promise<Mission[]>;
  getDashboardMetrics(): Promise<DashboardMetrics>;
}
