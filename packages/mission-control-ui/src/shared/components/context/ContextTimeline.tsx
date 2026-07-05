import { motion } from 'framer-motion';
import { Target, Clock, ShieldCheck, ArrowRight, Bot, Bell } from 'lucide-react';
import { cn } from '../../../utils/cn';

interface TimelineEvent {
  id: string;
  type: 'CONTEXT_CHANGE' | 'MISSION_CHANGE' | 'AI_LEARNING' | 'FINANCIAL_EVENT';
  title: string;
  description: string;
  timestamp: string;
  icon: any;
  color: string;
}

const MOCK_TIMELINE: TimelineEvent[] = [
  {
    id: 'e1',
    type: 'CONTEXT_CHANGE',
    title: 'Context Shift: High Credit Utilization',
    description: 'System detected credit card utilization crossed 80%. Context priority elevated to CRITICAL.',
    timestamp: '2 hours ago',
    icon: Bell,
    color: 'text-red-500 bg-red-500/10 border-red-500/20'
  },
  {
    id: 'e2',
    type: 'MISSION_CHANGE',
    title: 'Mission Auto-Started: Debt Reduction',
    description: 'Autonomous agent activated "Credit Card Payoff" mission based on new context.',
    timestamp: '1 hour ago',
    icon: Target,
    color: 'text-blue-500 bg-blue-500/10 border-blue-500/20'
  },
  {
    id: 'e3',
    type: 'AI_LEARNING',
    title: 'AI Behavioral Adjustment',
    description: 'Learned preference: User prefers paying off highest interest debt first (Avalanche method).',
    timestamp: 'Yesterday',
    icon: Bot,
    color: 'text-purple-500 bg-purple-500/10 border-purple-500/20'
  },
  {
    id: 'e4',
    type: 'FINANCIAL_EVENT',
    title: 'Decision Awaiting Approval',
    description: 'Agent paused execution. Awaiting manual authorization to transfer $5,000 from Savings.',
    timestamp: 'Just now',
    icon: ShieldCheck,
    color: 'text-amber-500 bg-amber-500/10 border-amber-500/20'
  }
];

export function ContextTimeline() {
  return (
    <div className="relative border-l-2 border-border ml-4 space-y-8 py-4">
      {MOCK_TIMELINE.map((event, i) => {
        const Icon = event.icon;
        
        return (
          <motion.div 
            key={event.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.1 }}
            className="relative pl-6 group"
          >
            {/* Timeline Node */}
            <div className={cn(
              "absolute -left-[17px] top-1 w-8 h-8 rounded-full border flex items-center justify-center bg-background shadow-sm",
              event.color
            )}>
              <Icon className="w-4 h-4" />
            </div>

            {/* Content */}
            <div className="bg-card border border-border p-4 rounded-xl shadow-sm hover:border-border/80 transition-colors">
              <div className="flex items-start justify-between mb-2">
                <h4 className="font-medium text-sm text-foreground">{event.title}</h4>
                <div className="flex items-center gap-1.5 text-xs text-muted-foreground">
                  <Clock className="w-3 h-3" />
                  {event.timestamp}
                </div>
              </div>
              <p className="text-sm text-muted-foreground">{event.description}</p>
              
              {event.type === 'FINANCIAL_EVENT' && (
                <button className="mt-3 px-3 py-1.5 bg-secondary hover:bg-secondary/80 text-foreground text-xs font-medium rounded transition-colors flex items-center gap-1.5">
                  Review Details <ArrowRight className="w-3 h-3" />
                </button>
              )}
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
