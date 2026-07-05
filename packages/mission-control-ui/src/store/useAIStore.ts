import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface ApprovalMetadata {
  title: string;
  summary: string;
  reason: string;
  expected_financial_impact?: string;
  expected_risks: string[];
  confidence_score: number;
  alternative_options: string[];
  estimated_cost?: string;
  estimated_benefit?: string;
  undo_availability: boolean;
  rollback_availability: boolean;
  referenced_policies: string[];
}

export interface ToolInvocation {
  id: string;
  tool_name: string;
  arguments: Record<string, any>;
  status: 'PENDING' | 'APPROVED' | 'REJECTED' | 'EXECUTING' | 'SUCCESS' | 'ERROR';
  result?: Record<string, any>;
  requires_approval: boolean;
  approval_status?: 'PENDING' | 'APPROVED' | 'REJECTED';
  approval_level?: 'INFORM_ONLY' | 'RECOMMENDATION' | 'ONE_CLICK' | 'TWO_STEP' | 'HOUSEHOLD';
  approval_metadata?: ApprovalMetadata;
}

export interface AITurn {
  id: string;
  role: 'user' | 'assistant' | 'system' | 'tool';
  content: string;
  timestamp: string;
  tool_invocations?: ToolInvocation[];
  metadata?: Record<string, any>;
  isStreaming?: boolean;
}

export interface OfflineAction {
  id: string;
  type: 'TURN' | 'APPROVAL' | 'WIDGET_PIN';
  payload: any;
  timestamp: string;
  retryCount: number;
}

export interface AIStore {
  // Shell State
  isShellOpen: boolean;
  shellMode: 'docked' | 'floating' | 'fullscreen';
  toggleShell: () => void;
  setShellMode: (mode: 'docked' | 'floating' | 'fullscreen') => void;
  
  // Conversation State
  turns: AITurn[];
  addTurn: (turn: AITurn) => void;
  updateLastTurn: (content: string, isStreaming: boolean) => void;
  updateToolStatus: (turnId: string, toolId: string, status: ToolInvocation['status'], result?: any) => void;
  clearHistory: () => void;

  // Offline Synchronization State
  offline_queue: OfflineAction[];
  syncStatus: 'IDLE' | 'SYNCING' | 'ERROR';
  queueAction: (action: Omit<OfflineAction, 'id' | 'timestamp' | 'retryCount'>) => void;
  removeAction: (id: string) => void;
  setSyncStatus: (status: 'IDLE' | 'SYNCING' | 'ERROR') => void;
}

export const useAIStore = create<AIStore>()(
  persist(
    (set) => ({
      isShellOpen: false,
      shellMode: 'floating',
      turns: [],
      offline_queue: [],
      syncStatus: 'IDLE',

      toggleShell: () => set((state) => ({ isShellOpen: !state.isShellOpen })),
      setShellMode: (mode) => set({ shellMode: mode }),

      queueAction: (action) => set((state) => ({
        offline_queue: [
          ...state.offline_queue,
          {
            ...action,
            id: `action_${Date.now()}`,
            timestamp: new Date().toISOString(),
            retryCount: 0
          }
        ]
      })),

      removeAction: (id) => set((state) => ({
        offline_queue: state.offline_queue.filter(a => a.id !== id)
      })),

      setSyncStatus: (status) => set({ syncStatus: status }),

      addTurn: (turn) => set((state) => ({ turns: [...state.turns, turn] })),
      updateLastTurn: (content, isStreaming) => set((state) => {
        if (state.turns.length === 0) return state;
        const newTurns = [...state.turns];
        newTurns[newTurns.length - 1] = { 
          ...newTurns[newTurns.length - 1], 
          content,
          isStreaming 
        };
        return { turns: newTurns };
      }),
      clearHistory: () => set({ turns: [] }),
      updateToolStatus: (turnId, toolId, status, result) => set((state) => ({
        turns: state.turns.map(turn => {
          if (turn.id !== turnId) return turn;
          return {
            ...turn,
            tool_invocations: turn.tool_invocations?.map(tool => 
              tool.id === toolId ? { ...tool, status, result } : tool
            )
          };
        })
      }))
    }),
    {
      name: 'pfos-ai-storage',
      partialize: (state) => ({ 
        turns: state.turns,
        offline_queue: state.offline_queue
      })
    }
  )
);
