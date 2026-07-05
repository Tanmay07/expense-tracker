import { useState } from 'react';
import { motion } from 'framer-motion';
import { AlertCircle, ArrowRight, BrainCircuit, Info, Lightbulb, Target, TrendingDown, TrendingUp } from 'lucide-react';
import { cn } from '../../../utils/cn';
import type { ContextCard as ContextCardModel } from '../../../core/models';
import { AIExplanationPanel } from './AIExplanationPanel';

interface ContextCardProps {
  card: ContextCardModel;
}

const PRIORITY_STYLES = {
  CRITICAL: 'border-red-500/50 bg-red-500/5',
  HIGH: 'border-amber-500/50 bg-amber-500/5',
  MEDIUM: 'border-blue-500/50 bg-blue-500/5',
  LOW: 'border-border bg-card'
};

const ICON_MAP: Record<string, any> = {
  DEBT_ALERT: AlertCircle,
  EMERGENCY_FUND_PROGRESS: Target,
  INVESTMENT_OPPORTUNITY: TrendingUp,
  SUBSCRIPTION_WASTE: TrendingDown,
  BILL_REMINDER: AlertCircle,
  AI_RECOMMENDATION: Lightbulb
};

export function ContextCard({ card }: ContextCardProps) {
  const [showExplanation, setShowExplanation] = useState(false);
  const Icon = ICON_MAP[card.card_type] || Info;

  return (
    <>
      <motion.div 
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        className={cn("rounded-xl border p-5 shadow-sm relative group overflow-hidden", PRIORITY_STYLES[card.priority as keyof typeof PRIORITY_STYLES] || PRIORITY_STYLES.LOW)}
      >
        {card.priority === 'CRITICAL' && (
          <div className="absolute top-0 left-0 w-1 h-full bg-red-500"></div>
        )}
        
        <div className="flex items-start justify-between">
          <div className="flex items-center gap-3">
            <div className={cn(
              "w-10 h-10 rounded-lg flex items-center justify-center border",
              card.priority === 'CRITICAL' ? 'bg-red-500/20 text-red-500 border-red-500/30' :
              card.priority === 'HIGH' ? 'bg-amber-500/20 text-amber-500 border-amber-500/30' :
              'bg-blue-500/10 text-blue-500 border-blue-500/20'
            )}>
              <Icon className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold">{card.title}</h3>
              <p className="text-sm text-muted-foreground mt-1 max-w-sm">{card.description}</p>
            </div>
          </div>
          
          <button 
            onClick={() => setShowExplanation(true)}
            className="p-2 bg-secondary/50 hover:bg-secondary rounded-full text-muted-foreground transition-colors group-hover:text-blue-500"
            title="View AI Reasoning"
          >
            <BrainCircuit className="w-4 h-4" />
          </button>
        </div>

        {card.actions && card.actions.length > 0 && (
          <div className="mt-5 flex items-center gap-3">
            {card.actions.map((action: any) => (
              <button 
                key={action.id}
                className={cn(
                  "px-4 py-2 text-sm font-medium rounded-md transition-colors flex items-center gap-2",
                  action.primary 
                    ? (card.priority === 'CRITICAL' ? "bg-red-500 hover:bg-red-600 text-white" : "bg-blue-500 hover:bg-blue-600 text-white")
                    : "bg-secondary hover:bg-secondary/80 text-foreground"
                )}
              >
                {action.label}
                <ArrowRight className="w-4 h-4" />
              </button>
            ))}
          </div>
        )}
      </motion.div>

      <AIExplanationPanel 
        isOpen={showExplanation} 
        onClose={() => setShowExplanation(false)} 
        explanation={card.explanation}
        title={card.title}
      />
    </>
  );
}
