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

  async getActiveContexts(): Promise<any[]> {
    await this.simulateDelay();
    // Return mock context for Developer mode
    return [
      {
        id: "ctx-debt-1",
        name: "High Credit Card Utilization",
        active: true,
        priority: "CRITICAL",
        confidence: 96,
        impact_score: 85,
        urgency: 90,
        recommended_mission_id: "m-debt-payoff",
        detected_at: new Date().toISOString(),
        explanation: {
          reason: "Credit utilization is 81%.",
          expected_impact: "Completing this mission could save approximately $1,500 annually in interest.",
          recommended_action: "Execute immediate transfer to high-interest accounts.",
          confidence_score: 96,
          supporting_evidence: [
            "Chase Sapphire balance is $12,450 / $15,000 limit.",
            "Average daily interest charge is $8.45."
          ]
        },
        cards: [
          {
            id: "card-1",
            card_type: "DEBT_ALERT",
            title: "Critical Debt Level Detected",
            description: "Your credit utilization is harming your credit score and costing you daily interest.",
            priority: "CRITICAL",
            explanation: {
              reason: "Utilization > 80%",
              expected_impact: "Credit score drop of ~40 points",
              recommended_action: "Pay down $5,000",
              confidence_score: 99,
              supporting_evidence: ["Equifax rules", "Current balance ratio"]
            },
            actions: [
              {
                id: "act-1",
                label: "Review Debt Mission",
                action_type: "NAVIGATE",
                icon: "Target",
                payload: { route: "/missions/m-debt-payoff" },
                primary: true
              }
            ],
            data: { utilization: 81, balance: 12450 }
          }
        ]
      }
    ];
  }

  async getAdaptiveDashboardLayout(): Promise<any> {
    await this.simulateDelay();
    return {
      top_section: "active_mission",
      widgets: ["cash_flow", "recent_transactions", "ai_priorities"],
      pinned_cards: []
    };
  }

  async getQuickActions(): Promise<any[]> {
    await this.simulateDelay();
    return [
      {
        id: "qa-pay-debt",
        label: "Pay EMI",
        action_type: "EXECUTE_TRANSFER",
        icon: "CreditCard",
        payload: { target: "debt" },
        primary: true
      },
      {
        id: "qa-ask-ai",
        label: "Ask AI",
        action_type: "OPEN_COPILOT",
        icon: "Bot",
        payload: {},
        primary: false
      }
    ];
  }

  async getWorkspaces(): Promise<any[]> {
    await this.simulateDelay();
    return [
      {
        id: "ws_expenses",
        name: "Expenses",
        description: "Manage and analyze daily expenses",
        icon: "CreditCard",
        path: "/workspaces/expenses",
        is_default: true,
        snapshots: [
          {
            id: "snap_1",
            name: "Default View",
            created_at: new Date().toISOString(),
            layout_config: { sidebarSize: 20, inspectorSize: 25 },
            widgets: [
              { id: "w_kpi_1", widget_type: "KPI", title: "Total Expenses", data_source: "mock", layout: { w: 3, h: 2, x: 0, y: 0 }, settings: {} },
              { id: "w_chart_1", widget_type: "CHART", title: "Spending Trends", data_source: "mock", layout: { w: 9, h: 4, x: 3, y: 0 }, settings: {} },
              { id: "w_note_1", widget_type: "NOTE", title: "Scratchpad", data_source: "mock", layout: { w: 4, h: 3, x: 0, y: 4 }, settings: { content: "# Expense Notes\n\n- Cut back on dining out\n- Review AWS bill" } }
            ]
          }
        ],
        metadata: {}
      }
    ];
  }

  async getAICapabilities(): Promise<any[]> {
    await this.simulateDelay();
    return [
      {
        id: "cap_chat_01",
        name: "Chat",
        description: "General conversational AI capability.",
        version: "1.0.0",
        category: "Interaction",
        supported_input_types: ["text"],
        supported_output_types: ["text", "markdown"],
        streaming_support: true,
        multimodal_support: false,
        requires_approval: false,
        expected_latency: "low",
        offline_availability: false,
        permissions: []
      },
      {
        id: "cap_financial_analysis_01",
        name: "Financial Analysis",
        description: "Analyze spending patterns and cash flow.",
        version: "1.2.0",
        category: "Analysis",
        supported_input_types: ["text", "structured_data"],
        supported_output_types: ["text", "chart", "table"],
        streaming_support: true,
        multimodal_support: false,
        requires_approval: false,
        expected_latency: "medium",
        offline_availability: false,
        permissions: []
      },
      {
        id: "cap_receipt_ocr_01",
        name: "Receipt OCR",
        description: "Extract structured data from receipt images.",
        version: "2.0.0",
        category: "Extraction",
        supported_input_types: ["image/jpeg", "image/png", "application/pdf"],
        supported_output_types: ["structured_data"],
        streaming_support: false,
        multimodal_support: true,
        requires_approval: false,
        expected_latency: "high",
        offline_availability: false,
        permissions: []
      }
    ];
  }

  async sendAIChat(payload: any, onChunk: (text: string) => void, onTool: (tool: any) => void): Promise<void> {
    await this.simulateDelay();
    
    // Check if the user is asking to create a budget to trigger approval flow
    const isBudgetRequest = payload.message?.toLowerCase().includes('budget');
    
    if (isBudgetRequest) {
      onChunk("I can help you create a budget for that. Let me prepare the action for your approval.");
      await new Promise(r => setTimeout(r, 1000));
      onTool({
        id: `tool_${Date.now()}`,
        tool_name: 'CreateBudget',
        arguments: { category: 'Dining', amount: 500 },
        status: 'PENDING',
        requires_approval: true,
        approval_level: 'TWO_STEP',
        approval_metadata: {
          title: 'Confirm Budget Creation',
          summary: 'You are about to establish a $500 monthly limit for Dining.',
          reason: 'This aligns with your Goal to reduce discretionary spending by 15% this quarter.',
          expected_financial_impact: 'Saves ~$120/month based on historical dining average.',
          expected_risks: ['May trigger over-budget alerts if weekend dining habits persist.'],
          confidence_score: 94,
          alternative_options: ['Set budget to $600', 'Wait until next month'],
          estimated_cost: '$0',
          estimated_benefit: '$1,440/year',
          undo_availability: true,
          rollback_availability: true,
          referenced_policies: ['PFOS-BUDGET-02']
        }
      });
      return;
    }
    
    const reply = `I received your message while you are in the **${payload.context.workspace_name}** workspace. I am ready to assist with financial forecasting, transaction search, or budget creation!`;
    let currentText = '';
    
    for (let i = 0; i < reply.length; i++) {
      currentText += reply[i];
      onChunk(currentText);
      await new Promise(r => setTimeout(r, 15));
    }
    
    // Send a final metadata packet
    onTool({
      id: "explainability_1",
      tool_name: "_explainability",
      arguments: {},
      status: "SUCCESS",
      requires_approval: false,
      result: {
        confidence: 0.96,
        policies: ["PFOS-SEC-001", "PFOS-MEM-003"],
        sources: ["KnowledgeGraph (Node: UserProfile)"],
        active_workspace: payload.context?.workspaceId,
        influencing_memories: [
          {
            type: "Long-Term Memory",
            confidence: 98,
            content: "User prioritizes aggressive debt payoff over investing.",
            source: "Household Profile",
            reason: "Aligned with current query."
          },
          {
            type: "Episodic Memory",
            confidence: 85,
            content: "User mentioned wanting to save $5,000 for a vacation.",
            source: "Conversation on 2026-06-12",
            reason: "Contextual relevance to budget generation."
          }
        ]
      }
    });
  }
}
