import type { Expense, Mission, DashboardMetrics } from '../../core/models';

export const GROWTH_PERSONA = {
  id: 'growth-1',
  name: 'Growth & Investments',
  description: 'High net worth, focus on growth and tax harvesting.',
  metrics: {
    netWorth: 1425000.00,
    netWorthTrend: 2.4,
    cashFlow: 12240.50,
    cashFlowTrend: 12,
    activeGoals: 4,
    atRiskGoals: 1,
    pendingBills: 850.00,
    billsDueDays: 3
  } as DashboardMetrics,
  expenses: [
    { id: '1', merchant: 'Whole Foods Market', category: 'Groceries', amount: 142.50, date: '2023-10-25', status: 'Cleared', tags: ['Needs'] },
    { id: '2', merchant: 'Equinox', category: 'Health', amount: 300.00, date: '2023-10-24', status: 'Cleared', tags: ['Subscription', 'Wants'] },
    { id: '3', merchant: 'Vanguard S&P 500', category: 'Investment', amount: 5000.00, date: '2023-10-22', status: 'Cleared', tags: ['Growth'] },
    { id: '4', merchant: 'Apple Store', category: 'Electronics', amount: 2499.00, date: '2023-10-20', status: 'Cleared', tags: ['Wants', 'Tax Deductible'] }
  ] as Expense[],
  missions: [
    {
      id: 'm1',
      title: 'Tax Loss Harvesting',
      description: 'Execute trades to harvest $4,500 in unrealized losses before EOY.',
      status: 'ACTIVE',
      progress: 40,
      agent: 'Wealth Agent',
      tasks: [
        { id: 't1', name: 'Identify losing positions', completed: true },
        { id: 't2', name: 'Analyze wash sale rules', completed: true },
        { id: 't3', name: 'Execute sell orders', completed: false }
      ]
    }
  ] as Mission[]
};

export const STABILIZATION_PERSONA = {
  id: 'stab-1',
  name: 'Debt & Stabilization',
  description: 'Focus on debt payoff and strict budgeting.',
  metrics: {
    netWorth: -15400.00,
    netWorthTrend: 5.1,
    cashFlow: 450.00,
    cashFlowTrend: -2,
    activeGoals: 2,
    atRiskGoals: 2,
    pendingBills: 2150.00,
    billsDueDays: 1
  } as DashboardMetrics,
  expenses: [
    { id: '1', merchant: 'Chase Credit Card', category: 'Debt', amount: 800.00, date: '2023-10-25', status: 'Cleared', tags: ['Needs', 'Debt'] },
    { id: '2', merchant: 'Grocery Outlet', category: 'Groceries', amount: 45.50, date: '2023-10-24', status: 'Cleared', tags: ['Needs'] },
    { id: '3', merchant: 'PG&E Utility', category: 'Bills', amount: 112.50, date: '2023-10-22', status: 'Pending', tags: ['Needs', 'Recurring'] }
  ] as Expense[],
  missions: [
    {
      id: 'm2',
      title: 'Credit Card Payoff',
      description: 'Allocate all excess cash flow to highest interest debt (Chase API).',
      status: 'ACTIVE',
      progress: 60,
      agent: 'Debt Agent',
      tasks: [
        { id: 't1', name: 'Calculate excess cash flow', completed: true },
        { id: 't2', name: 'Identify highest APR account', completed: true },
        { id: 't3', name: 'Execute payment transfer', completed: false }
      ]
    }
  ] as Mission[]
};
