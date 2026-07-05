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

export interface AICapability {
  id: string;
  name: string;
  description: string;
  version: string;
  category: string;
  supported_input_types: string[];
  supported_output_types: string[];
  streaming_support: boolean;
  multimodal_support: boolean;
  requires_approval: boolean;
  expected_latency: string;
  offline_availability: boolean;
  feature_flag?: string;
  permissions: string[];
}

export interface IDataProvider {
  getAdaptiveDashboard: () => Promise<any>;
  getQuickActions: () => Promise<any>;
  getWorkspaces: () => Promise<any>;
  getAITools?: () => Promise<any>;
  getAICapabilities?: () => Promise<AICapability[]>;
  sendAIChat?: (payload: any, onChunk: (text: string) => void, onTool: (tool: any) => void) => Promise<void>;
}

export interface AdaptiveDashboardLayout {
  top_section: 'active_mission' | 'metrics';
  widgets: string[];
  pinned_cards: ContextCard[];
}
