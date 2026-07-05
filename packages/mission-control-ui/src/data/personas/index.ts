import type { Expense, Mission, DashboardMetrics } from '../../core/models';

const MERCHANTS = ['Whole Foods', 'Equinox', 'Vanguard', 'Apple Store', 'PG&E', 'Chevron', 'Netflix', 'Amazon', 'Target', 'Starbucks'];
const CATEGORIES = ['Groceries', 'Health', 'Investment', 'Electronics', 'Bills', 'Auto', 'Entertainment', 'Shopping', 'Dining'];

function generateExpenses(count: number, personaPrefix: string): Expense[] {
  return Array.from({ length: count }).map((_, i) => ({
    id: `${personaPrefix}-exp-${i}`,
    merchant: MERCHANTS[Math.floor(Math.random() * MERCHANTS.length)],
    category: CATEGORIES[Math.floor(Math.random() * CATEGORIES.length)],
    amount: parseFloat((Math.random() * 500 + 5).toFixed(2)),
    date: new Date(Date.now() - Math.floor(Math.random() * 90) * 86400000).toISOString().split('T')[0],
    status: Math.random() > 0.2 ? 'Cleared' : 'Pending',
    tags: Math.random() > 0.5 ? ['Needs'] : ['Wants']
  }));
}

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
  expenses: generateExpenses(1000, 'growth'),
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
  expenses: generateExpenses(500, 'stab'),
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

export const PERSONAS = {
  [GROWTH_PERSONA.id]: GROWTH_PERSONA,
  [STABILIZATION_PERSONA.id]: STABILIZATION_PERSONA
};
