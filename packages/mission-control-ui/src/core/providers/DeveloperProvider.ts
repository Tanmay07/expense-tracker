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
}
