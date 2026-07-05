import { useDevStore } from '../../store/useDevStore';
import { useFeatureFlags } from '../../core/flags/useFeatureFlags';
import type { FeatureFlag } from '../../core/flags/useFeatureFlags';
import { GROWTH_PERSONA, STABILIZATION_PERSONA } from '../../data/personas';
import { Activity, TestTube, Network, Flag } from 'lucide-react';
import { cn } from '../../utils/cn';

export function DeveloperWorkspace() {
  const { activePersonaId, setActivePersonaId, mockNetworkDelay, setMockNetworkDelay } = useDevStore();
  const { flags, toggleFlag } = useFeatureFlags();

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight flex items-center gap-3">
          <TestTube className="w-8 h-8 text-purple-500" />
          Developer Workspace
        </h1>
        <p className="text-muted-foreground mt-1">Configure mocking, simulated environments, and feature flags.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <section className="p-6 rounded-xl border border-border bg-card">
          <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Activity className="w-5 h-5 text-blue-500" />
            Active Persona
          </h2>
          <div className="space-y-3">
            {[GROWTH_PERSONA, STABILIZATION_PERSONA].map(p => (
              <button
                key={p.id}
                onClick={() => setActivePersonaId(p.id)}
                className={cn(
                  "w-full text-left p-4 rounded-lg border transition-all",
                  activePersonaId === p.id 
                    ? "border-blue-500 bg-blue-500/10 shadow-[0_0_15px_rgba(59,130,246,0.15)]" 
                    : "border-border hover:border-border/80 bg-background"
                )}
              >
                <div className="font-medium">{p.name}</div>
                <div className="text-xs text-muted-foreground mt-1">{p.description}</div>
              </button>
            ))}
          </div>
        </section>

        <section className="p-6 rounded-xl border border-border bg-card">
          <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Network className="w-5 h-5 text-emerald-500" />
            Network Simulation
          </h2>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">Mock Network Delay (ms)</label>
              <input 
                type="range" 
                min="0" max="3000" step="100"
                value={mockNetworkDelay}
                onChange={e => setMockNetworkDelay(parseInt(e.target.value))}
                className="w-full mt-2"
              />
              <div className="text-right text-xs text-muted-foreground mt-1">{mockNetworkDelay}ms latency</div>
            </div>
          </div>
        </section>

        <section className="p-6 rounded-xl border border-border bg-card md:col-span-2">
          <h2 className="text-lg font-semibold flex items-center gap-2 mb-4">
            <Flag className="w-5 h-5 text-amber-500" />
            Feature Flags
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {(Object.keys(flags) as FeatureFlag[]).map(key => (
              <div key={key} className="flex items-center justify-between p-3 rounded-lg border border-border bg-background">
                <span className="text-sm font-medium capitalize">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                <button 
                  onClick={() => toggleFlag(key)}
                  className={cn(
                    "relative inline-flex h-5 w-9 items-center rounded-full transition-colors",
                    flags[key] ? "bg-blue-500" : "bg-secondary"
                  )}
                >
                  <span className={cn(
                    "inline-block h-3 w-3 transform rounded-full bg-white transition-transform",
                    flags[key] ? "translate-x-5" : "translate-x-1"
                  )} />
                </button>
              </div>
            ))}
          </div>
        </section>
      </div>
    </div>
  );
}
