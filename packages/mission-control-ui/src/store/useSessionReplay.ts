import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { useAIStore } from './useAIStore';
import type { AITurn } from './useAIStore';

interface ReplayEvent {
  timestamp: string;
  type: 'TURN_ADDED' | 'TOOL_INVOCATION' | 'APPROVAL_STATUS_CHANGED' | 'CAPABILITY_DETECTED';
  payload: any;
}

interface ReplaySession {
  id: string;
  start_time: string;
  end_time?: string;
  events: ReplayEvent[];
  initial_state: AITurn[];
}

interface ReplayStore {
  isRecording: boolean;
  isReplaying: boolean;
  sessions: ReplaySession[];
  currentSessionId: string | null;
  playbackIndex: number;
  
  startRecording: () => void;
  stopRecording: () => void;
  recordEvent: (type: ReplayEvent['type'], payload: any) => void;
  
  startReplay: (sessionId: string) => void;
  stopReplay: () => void;
  stepForward: () => void;
  stepBack: () => void;
  jumpTo: (index: number) => void;
}

export const useSessionReplay = create<ReplayStore>()(
  persist(
    (set, get) => ({
      isRecording: false,
      isReplaying: false,
      sessions: [],
      currentSessionId: null,
      playbackIndex: -1,

      startRecording: () => {
        const id = `session_${Date.now()}`;
        set((state) => ({
          isRecording: true,
          currentSessionId: id,
          sessions: [
            ...state.sessions,
            {
              id,
              start_time: new Date().toISOString(),
              events: [],
              initial_state: [...useAIStore.getState().turns]
            }
          ]
        }));
      },

      stopRecording: () => {
        set((state) => ({
          isRecording: false,
          sessions: state.sessions.map(s => 
            s.id === state.currentSessionId 
              ? { ...s, end_time: new Date().toISOString() }
              : s
          ),
          currentSessionId: null
        }));
      },

      recordEvent: (type, payload) => {
        const { isRecording, currentSessionId } = get();
        if (!isRecording || !currentSessionId) return;

        set((state) => ({
          sessions: state.sessions.map(s => 
            s.id === currentSessionId
              ? { ...s, events: [...s.events, { timestamp: new Date().toISOString(), type, payload }] }
              : s
          )
        }));
      },

      startReplay: (sessionId) => {
        const session = get().sessions.find(s => s.id === sessionId);
        if (!session) return;
        
        // Restore initial state
        useAIStore.setState({ turns: session.initial_state });
        
        set({ isReplaying: true, currentSessionId: sessionId, playbackIndex: -1 });
      },

      stopReplay: () => {
        set({ isReplaying: false, currentSessionId: null, playbackIndex: -1 });
      },

      stepForward: () => {
        const { isReplaying, currentSessionId, playbackIndex, sessions } = get();
        if (!isReplaying || !currentSessionId) return;
        
        const session = sessions.find(s => s.id === currentSessionId);
        if (!session || playbackIndex >= session.events.length - 1) return;

        const nextIndex = playbackIndex + 1;
        const event = session.events[nextIndex];
        
        // Apply deterministic mutation based on event type
        if (event.type === 'TURN_ADDED') {
           useAIStore.setState(state => ({ turns: [...state.turns, event.payload] }));
        }
        
        set({ playbackIndex: nextIndex });
      },

      stepBack: () => {
        // Needs full deterministic rewind, currently we just jump from 0 for simplicity
        const { playbackIndex } = get();
        if (playbackIndex > -1) {
          get().jumpTo(playbackIndex - 1);
        }
      },

      jumpTo: (targetIndex) => {
        const { isReplaying, currentSessionId, sessions } = get();
        if (!isReplaying || !currentSessionId) return;
        const session = sessions.find(s => s.id === currentSessionId);
        if (!session) return;

        useAIStore.setState({ turns: session.initial_state });
        for (let i = 0; i <= targetIndex; i++) {
           const event = session.events[i];
           if (event.type === 'TURN_ADDED') {
             useAIStore.setState(state => ({ turns: [...state.turns, event.payload] }));
           }
        }
        
        set({ playbackIndex: targetIndex });
      }
    }),
    { name: 'pfos-replay-store' }
  )
);
