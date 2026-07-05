import { motion } from 'framer-motion';
import { Target, Clock, CheckCircle2, ChevronRight, Play, Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';
import { useMissions } from '../hooks/useData';

export function Missions() {
  const { data: missions, isLoading } = useMissions();

  if (isLoading || !missions) {
    return (
      <div className="flex items-center justify-center h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Mission Center</h1>
        <p className="text-muted-foreground mt-1">Monitor and manage autonomous agent workflows.</p>
      </div>

      <div className="grid gap-6">
        {missions.map((mission, i) => (
          <motion.div 
            key={mission.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
            className={cn(
              "p-6 rounded-xl border bg-card overflow-hidden relative",
              mission.status === 'ACTIVE' ? "border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.1)]" : "border-border"
            )}
          >
            {mission.status === 'ACTIVE' && (
              <div className="absolute top-0 left-0 w-1 h-full bg-blue-500"></div>
            )}
            
            <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
              <div>
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-xl font-semibold">{mission.title}</h2>
                  <span className={cn(
                    "px-2.5 py-0.5 text-[10px] uppercase tracking-wider font-semibold rounded-full",
                    mission.status === 'ACTIVE' ? "bg-blue-500/10 text-blue-500" : "bg-emerald-500/10 text-emerald-500"
                  )}>
                    {mission.status}
                  </span>
                </div>
                <p className="text-muted-foreground text-sm max-w-xl">{mission.description}</p>
                <div className="mt-4 flex items-center gap-2 text-xs text-muted-foreground">
                  <span className="px-2 py-1 bg-secondary rounded flex items-center gap-1">
                    <Target className="w-3 h-3" />
                    Agent: {mission.agent}
                  </span>
                </div>
              </div>

              <div className="shrink-0 sm:text-right">
                <div className="text-3xl font-bold">{mission.progress}%</div>
                <div className="text-sm text-muted-foreground">Completed</div>
              </div>
            </div>

            <div className="mt-6 pt-6 border-t border-border">
              <h3 className="text-sm font-medium mb-3 flex items-center gap-2">
                Execution Plan
              </h3>
              <div className="space-y-3">
                {mission.tasks.map((task, j) => (
                  <div key={task.id} className="flex items-center gap-3 text-sm">
                    {task.completed ? (
                      <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0" />
                    ) : mission.status === 'ACTIVE' && j === mission.tasks.findIndex(t => !t.completed) ? (
                      <div className="relative flex items-center justify-center w-5 h-5 shrink-0">
                        <span className="absolute w-full h-full bg-blue-500/20 rounded-full animate-ping"></span>
                        <Play className="w-3 h-3 text-blue-500 relative z-10 fill-current" />
                      </div>
                    ) : (
                      <Clock className="w-5 h-5 text-muted-foreground shrink-0" />
                    )}
                    <span className={cn(
                      "transition-colors",
                      task.completed ? "text-muted-foreground line-through" : "text-foreground"
                    )}>
                      {task.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            
            {mission.status === 'ACTIVE' && (
              <div className="mt-6 flex justify-end">
                <button className="flex items-center gap-2 px-4 py-2 bg-secondary hover:bg-secondary/80 text-foreground text-sm font-medium rounded-md transition-colors">
                  Intervene <ChevronRight className="w-4 h-4" />
                </button>
              </div>
            )}
          </motion.div>
        ))}
        {missions.length === 0 && (
          <div className="p-12 text-center text-muted-foreground border border-border border-dashed rounded-xl">
            No missions found for this persona.
          </div>
        )}
      </div>
    </div>
  );
}
