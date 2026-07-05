import { ProviderResolver } from '../providers/ProviderResolver';

export class DashboardService {
  static async getMetrics() {
    return ProviderResolver.resolve().getDashboardMetrics();
  }
}

export class ExpenseService {
  static async getExpenses() {
    return ProviderResolver.resolve().getExpenses();
  }
}

export class MissionService {
  static async getMissions() {
    return ProviderResolver.resolve().getMissions();
  }
}
