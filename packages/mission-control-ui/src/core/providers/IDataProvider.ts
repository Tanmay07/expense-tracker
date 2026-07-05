import type { Expense, Mission, DashboardMetrics } from '../models';

export interface IDataProvider {
  getExpenses(): Promise<Expense[]>;
  getMissions(): Promise<Mission[]>;
  getDashboardMetrics(): Promise<DashboardMetrics>;
  getActiveContexts(): Promise<any[]>;
  getAdaptiveDashboardLayout(): Promise<any>;
  getQuickActions(): Promise<any[]>;
  getWorkspaces?(): Promise<any[]>;
}
