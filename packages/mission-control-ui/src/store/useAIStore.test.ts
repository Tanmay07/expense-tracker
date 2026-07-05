import { describe, it, expect, beforeEach } from 'vitest';
import { useAIStore } from './useAIStore';

describe('useAIStore', () => {
  beforeEach(() => {
    // Reset state before each test
    useAIStore.setState({
      isShellOpen: false,
      shellMode: 'floating',
      turns: [],
      offline_queue: [],
      syncStatus: 'IDLE',
    });
  });

  it('toggles the shell state', () => {
    expect(useAIStore.getState().isShellOpen).toBe(false);
    useAIStore.getState().toggleShell();
    expect(useAIStore.getState().isShellOpen).toBe(true);
  });

  it('queues an offline action', () => {
    const actionPayload = { content: 'test message' };
    useAIStore.getState().queueAction({ type: 'TURN', payload: actionPayload });
    
    const state = useAIStore.getState();
    expect(state.offline_queue.length).toBe(1);
    expect(state.offline_queue[0].type).toBe('TURN');
    expect(state.offline_queue[0].payload).toEqual(actionPayload);
  });

  it('removes an action from the offline queue', () => {
    useAIStore.getState().queueAction({ type: 'TURN', payload: {} });
    const actionId = useAIStore.getState().offline_queue[0].id;
    
    useAIStore.getState().removeAction(actionId);
    expect(useAIStore.getState().offline_queue.length).toBe(0);
  });

  it('adds a turn correctly', () => {
    const turn = { id: '1', role: 'user' as const, content: 'Hello', timestamp: '123' };
    useAIStore.getState().addTurn(turn);
    
    const state = useAIStore.getState();
    expect(state.turns.length).toBe(1);
    expect(state.turns[0]).toEqual(turn);
  });
});
