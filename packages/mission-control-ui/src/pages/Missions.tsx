import { motion } from 'framer-motion';
import { Target, Activity, ShieldAlert, CheckCircle2, ChevronRight, BarChart, FileText, FastForward, Clock } from 'lucide-react';
import { cn } from '../utils/cn';
import { GROWTH_PERSONA } from '../data/personas';

export function Missions() {
  const missions = GROWTH_PERSONA.missions; // In a real app, we'd fetch these from BFF

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Mission Center</h1>
          <p className="text-muted-foreground mt-1">Orchestrate and monitor autonomous AI executions.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="px-4 py-2 bg-secondary text-secondary-foreground text-sm font-medium rounded-md hover:bg-secondary/80 transition-colors">
            Mission History
          </button>
          <button className="px-4 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:bg-primary/90 transition-colors flex items-center gap-2">
            <Target className="w-4 h-4" />
            Launch Mission
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between border-b border-border pb-4">
            <h2 className="text-lg font-semibold flex items-center gap-2">
              <Activity className="w-5 h-5 text-blue-500" />
              Active Executions
            </h2>
            <div className="flex gap-2">
              <span className="px-2 py-1 bg-blue-500/10 text-blue-500 text-xs rounded-full font-medium border border-blue-500/20">
                {missions.length} Active
              </span>
            </div>
          </div>

          <div className="space-y-4">
            {missions.map((mission) => (
              <motion.div 
                key={mission.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-card border border-blue-500/30 rounded-xl overflow-hidden shadow-sm"
              >
                <div className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="px-2 py-0.5 bg-blue-500/10 text-blue-500 text-[10px] uppercase font-bold tracking-wider rounded border border-blue-500/20">
                          {mission.agent}
                        </span>
                        <span className="text-xs text-muted-foreground flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          Started 2h ago
                        </span>
                      </div>
                      <h3 className="text-xl font-bold">{mission.title}</h3>
                      <p className="text-muted-foreground text-sm mt-1 max-w-xl">{mission.description}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-3xl font-bold text-blue-500">{mission.progress}%</div>
                      <div className="text-xs text-muted-foreground uppercase tracking-wide font-medium mt-1">Completion</div>
                    </div>
                  </div>

                  {/* Dependency Graph UI representation */}
                  <div className="mt-8 bg-secondary/20 rounded-lg p-4 border border-border">
                    <h4 className="text-xs font-semibold uppercase tracking-wider text-muted-foreground mb-4">Execution Graph</h4>
                    <div className="space-y-3 relative before:absolute before:inset-0 before:ml-3 before:-translate-x-px md:before:mx-auto md:before:translate-x-0 before:h-full before:w-0.5 before:bg-gradient-to-b before:from-transparent before:via-border before:to-transparent">
                      {mission.tasks.map((task) => (
                        <div key={task.id} className="relative flex items-center justify-between md:justify-normal md:odd:flex-row-reverse group is-active">
                          <div className="flex items-center justify-center w-6 h-6 rounded-full border-4 border-card shrink-0 md:order-1 md:group-odd:-translate-x-1/2 md:group-even:translate-x-1/2 shadow-sm z-10 
                            bg-blue-500 text-white">
                            {task.completed ? <CheckCircle2 className="w-3 h-3" /> : <div className="w-1.5 h-1.5 bg-white rounded-full"></div>}
                          </div>
                          
                          <div className="w-[calc(100%-3rem)] md:w-[calc(50%-2rem)] p-3 rounded bg-background border border-border shadow-sm flex items-center justify-between">
                            <span className={cn("text-sm font-medium", task.completed ? "text-muted-foreground" : "text-foreground")}>
                              {task.name}
                            </span>
                            {!task.completed && (
                              <button className="text-xs font-medium text-blue-500 hover:text-blue-400">Review</button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="mt-6 flex items-center justify-between pt-4 border-t border-border">
                    <div className="flex items-center gap-4 text-sm">
                       <span className="flex items-center gap-1.5 text-muted-foreground">
                        <ShieldAlert className="w-4 h-4" />
                        Awaiting Authorization
                      </span>
                    </div>
                    <button className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-md transition-colors flex items-center gap-2">
                      Authorize Next Step
                      <FastForward className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>

        <div className="space-y-6">
          <div className="bg-card border border-border rounded-xl p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <BarChart className="w-4 h-4 text-muted-foreground" />
              Impact Estimation
            </h3>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Est. Tax Savings (EOY)</span>
                  <span className="font-medium text-emerald-500">+$1,250</span>
                </div>
                <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-emerald-500 w-[60%]"></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Est. Debt Reduction (Q4)</span>
                  <span className="font-medium text-emerald-500">-$3,400</span>
                </div>
                <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 w-[45%]"></div>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-card border border-border rounded-xl p-5">
            <h3 className="font-semibold mb-4 flex items-center gap-2">
              <FileText className="w-4 h-4 text-muted-foreground" />
              Recent Decisions
            </h3>
            <div className="space-y-3">
              {[
                { title: 'Rebalanced 401k to 80/20', date: '2d ago', status: 'Executed' },
                { title: 'Paused Gym Subscription', date: '4d ago', status: 'Executed' },
                { title: 'Transferred $500 to Savings', date: '5d ago', status: 'Executed' },
              ].map((d, i) => (
                <div key={i} className="flex items-center justify-between text-sm p-2 hover:bg-secondary rounded-md cursor-pointer transition-colors group">
                  <div>
                    <p className="font-medium group-hover:text-blue-400 transition-colors">{d.title}</p>
                    <p className="text-xs text-muted-foreground">{d.date}</p>
                  </div>
                  <ChevronRight className="w-4 h-4 text-muted-foreground" />
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
