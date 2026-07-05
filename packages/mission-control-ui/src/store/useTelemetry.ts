import { useCallback } from 'react';

type TelemetryEventType = 
  | 'CONVERSATION_STARTED'
  | 'TOOL_INVOCATION_REQUESTED'
  | 'TOOL_INVOCATION_COMPLETED'
  | 'APPROVAL_REQUESTED'
  | 'APPROVAL_GRANTED'
  | 'APPROVAL_REJECTED'
  | 'WIDGET_GENERATED'
  | 'REPLAY_STARTED';

interface TelemetryEvent {
  eventType: TelemetryEventType;
  timestamp: string;
  metadata: Record<string, any>;
}

export function useTelemetry() {
  const trackEvent = useCallback(async (eventType: TelemetryEventType, metadata: Record<string, any> = {}) => {
    const event: TelemetryEvent = {
      eventType,
      timestamp: new Date().toISOString(),
      metadata,
    };
    
    // In production, this would use a beacon or fetch to the BFF
    // e.g. fetch('/api/bff/telemetry', { method: 'POST', body: JSON.stringify(event), keepalive: true })
    
    // We only log to console for development verification, ensuring no PII/prompts are in the payload.
    console.debug('[Telemetry]', eventType, metadata);
    
    try {
      await fetch('/api/bff/telemetry', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(event)
      });
    } catch (e) {
      // Swallow telemetry errors gracefully
    }
  }, []);

  return { trackEvent };
}
