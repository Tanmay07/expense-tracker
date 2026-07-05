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

export interface ContextExplanation {
  reason: string;
  expected_impact: string;
  recommended_action: string;
  confidence_score: number;
  supporting_evidence: string[];
}

export interface AdaptiveAction {
  id: string;
  label: string;
  action_type: string;
  icon: string;
  payload: Record<string, any>;
  primary: boolean;
}

export interface ContextCard {
  id: string;
  card_type: string;
  title: string;
  description: string;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  explanation: ContextExplanation;
  actions: AdaptiveAction[];
  data: Record<string, any>;
}

export interface FinancialContext {
  id: string;
  name: string;
  active: boolean;
  priority: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  confidence: number;
  impact_score: number;
  urgency: number;
  recommended_mission_id?: string;
  detected_at: string;
  explanation: ContextExplanation;
  cards: ContextCard[];
}

export interface AdaptiveDashboardLayout {
  top_section: 'active_mission' | 'metrics';
  widgets: string[];
  pinned_cards: ContextCard[];
}
