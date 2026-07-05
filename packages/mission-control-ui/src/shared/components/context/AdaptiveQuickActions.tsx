import { motion } from 'framer-motion';
import { CreditCard, Bot, Target, FileText, Settings, ArrowRight } from 'lucide-react';
import { cn } from '../../../utils/cn';
import type { AdaptiveAction } from '../../../core/models';

interface AdaptiveQuickActionsProps {
  actions: AdaptiveAction[];
}

const ICON_MAP: Record<string, any> = {
  CreditCard: CreditCard,
  Bot: Bot,
  Target: Target,
  FileText: FileText,
  Settings: Settings
};

export function AdaptiveQuickActions({ actions }: AdaptiveQuickActionsProps) {
  if (!actions || actions.length === 0) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {actions.map((action, i) => {
        const Icon = ICON_MAP[action.icon] || ArrowRight;
        
        return (
          <motion.button
            key={action.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className={cn(
              "p-4 rounded-xl border text-left transition-all hover:scale-[1.02] active:scale-[0.98] flex flex-col justify-between h-24 group",
              action.primary 
                ? "bg-blue-500 hover:bg-blue-600 border-blue-500 shadow-md text-white" 
                : "bg-card hover:bg-secondary/50 border-border shadow-sm text-foreground"
            )}
          >
            <Icon className={cn("w-5 h-5", action.primary ? "text-blue-100" : "text-blue-500 group-hover:text-blue-400")} />
            <span className="text-sm font-medium">{action.label}</span>
          </motion.button>
        );
      })}
    </div>
  );
}
