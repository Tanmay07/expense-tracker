export interface Expense {
  id: string;
  merchant: string;
  category: string;
  amount: number;
  date: string;
  status: 'Cleared' | 'Pending';
  tags: string[];
}

export interface MissionTask {
  id: string;
  name: string;
  completed: boolean;
}

export interface Mission {
  id: string;
  title: string;
  description: string;
  status: 'ACTIVE' | 'COMPLETED' | 'FAILED';
  progress: number;
  agent: string;
  tasks: MissionTask[];
}

export interface DashboardMetrics {
  netWorth: number;
  netWorthTrend: number; // percentage
  cashFlow: number;
  cashFlowTrend: number;
  activeGoals: number;
  atRiskGoals: number;
  pendingBills: number;
  billsDueDays: number;
}
