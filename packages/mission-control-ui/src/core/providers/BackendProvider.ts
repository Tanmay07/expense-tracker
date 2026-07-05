import type { IDataProvider } from './IDataProvider';
import type { Expense, Mission, DashboardMetrics } from '../models';

export class BackendProvider implements IDataProvider {
  private baseUrl: string;

  constructor(baseUrl: string = '/api/v1') {
    this.baseUrl = baseUrl;
  }

  async getExpenses(): Promise<Expense[]> {
    const res = await fetch(`${this.baseUrl}/expenses`);
    if (!res.ok) throw new Error('Failed to fetch expenses');
    return res.json();
  }

  async getMissions(): Promise<Mission[]> {
    const res = await fetch(`${this.baseUrl}/missions`);
    if (!res.ok) throw new Error('Failed to fetch missions');
    return res.json();
  }

  async getDashboardMetrics(): Promise<DashboardMetrics> {
    const res = await fetch(`${this.baseUrl}/dashboard/metrics`);
    if (!res.ok) throw new Error('Failed to fetch dashboard metrics');
    return res.json();
  }

  async getActiveContexts(): Promise<any[]> {
    const res = await fetch(`${this.baseUrl}/bff/context`);
    if (!res.ok) throw new Error('Failed to fetch context');
    const data = await res.json();
    return data.contexts;
  }

  async getAdaptiveDashboardLayout(): Promise<any> {
    const res = await fetch(`${this.baseUrl}/bff/dashboard/adaptive`);
    if (!res.ok) throw new Error('Failed to fetch dashboard layout');
    const data = await res.json();
    return data.layout;
  }

  async getQuickActions(): Promise<any[]> {
    const res = await fetch(`${this.baseUrl}/bff/quick-actions`);
    if (!res.ok) throw new Error('Failed to fetch quick actions');
    const data = await res.json();
    return data.actions;
  }

  async getWorkspaces(): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/bff/workspaces`, {
      headers: { 'mock_user_123': 'true' }
    });
    if (!response.ok) throw new Error('Failed to fetch workspaces');
    const data = await response.json();
    return data.workspaces;
  }

  async getAICapabilities(): Promise<any[]> {
    const response = await fetch(`${this.baseUrl}/ai/capabilities`, {
      headers: { 'mock_user_123': 'true' }
    });
    if (!response.ok) throw new Error('Failed to fetch capabilities');
    const data = await response.json();
    return data.capabilities;
  }

  async sendAIChat(payload: any, onChunk: (text: string) => void, onTool: (tool: any) => void): Promise<void> {
    const response = await fetch(`${this.baseUrl}/ai/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'mock_user_123': 'true' },
      body: JSON.stringify(payload)
    });
    
    if (!response.ok) throw new Error('Failed to send AI chat');
    
    const data = await response.json();
    onChunk(data.reply);
    
    if (data.tool_invocations) {
      data.tool_invocations.forEach((t: any) => onTool(t));
    }
  }
}
