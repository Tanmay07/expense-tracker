import { useState } from 'react';
import { useAppStore } from '../store/useAppStore';
import { Database, Network, Server, Shield, Activity, HardDrive, WifiOff } from 'lucide-react';
import { cn } from '../utils/cn';
import { PERSONAS } from '../data/personas';

export function DeveloperWorkspace() {
  const { currentProvider, setCurrentProvider, activePersona, setActivePersona, isOfflineMode, setOfflineMode } = useAppStore();
  const [activeTab, setActiveTab] = useState<'providers' | 'architecture' | 'telemetry'>('providers');

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Developer Workspace</h1>
        <p className="text-muted-foreground mt-1">Configure providers, simulate personas, and monitor system architecture.</p>
      </div>

      <div className="flex gap-4 border-b border-border">
        <button 
          onClick={() => setActiveTab('providers')}
          className={cn("pb-3 text-sm font-medium border-b-2 transition-colors", activeTab === 'providers' ? "border-blue-500 text-foreground" : "border-transparent text-muted-foreground hover:text-foreground")}
        >
          Data & Providers
        </button>
        <button 
          onClick={() => setActiveTab('architecture')}
          className={cn("pb-3 text-sm font-medium border-b-2 transition-colors", activeTab === 'architecture' ? "border-blue-500 text-foreground" : "border-transparent text-muted-foreground hover:text-foreground")}
        >
          Architecture & BFF
        </button>
        <button 
          onClick={() => setActiveTab('telemetry')}
          className={cn("pb-3 text-sm font-medium border-b-2 transition-colors", activeTab === 'telemetry' ? "border-blue-500 text-foreground" : "border-transparent text-muted-foreground hover:text-foreground")}
        >
          Telemetry
        </button>
      </div>

      {activeTab === 'providers' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <section className="p-6 rounded-xl border border-border bg-card">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <Database className="w-5 h-5 text-blue-500" />
              Active Provider
            </h2>
            <div className="space-y-3">
              {[
                { id: 'backend', name: 'BackendProvider', desc: 'Real API via MissionControlBFF' },
                { id: 'developer', name: 'DeveloperProvider', desc: 'Mocked in-memory data' },
                { id: 'offline', name: 'OfflineProvider', desc: 'Local IndexedDB cache' },
              ].map(provider => (
                <label key={provider.id} className={cn("flex items-start gap-3 p-3 border rounded-lg cursor-pointer transition-colors", currentProvider === provider.id ? "border-blue-500 bg-blue-500/5" : "border-border bg-background hover:bg-secondary/50")}>
                  <input 
                    type="radio" 
                    name="provider" 
                    value={provider.id} 
                    checked={currentProvider === provider.id}
                    onChange={(e) => setCurrentProvider(e.target.value as any)}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-medium text-sm">{provider.name}</div>
                    <div className="text-xs text-muted-foreground">{provider.desc}</div>
                  </div>
                </label>
              ))}
            </div>

            <div className="mt-6 pt-6 border-t border-border">
              <label className="flex items-center gap-3">
                <input 
                  type="checkbox" 
                  checked={isOfflineMode}
                  onChange={(e) => setOfflineMode(e.target.checked)}
                  className="w-4 h-4 rounded border-border"
                />
                <span className="font-medium flex items-center gap-2">
                  <WifiOff className="w-4 h-4 text-amber-500" />
                  Simulate Offline Network
                </span>
              </label>
            </div>
          </section>

          <section className="p-6 rounded-xl border border-border bg-card">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <UserIcon className="w-5 h-5 text-emerald-500" />
              Data Persona
            </h2>
            <p className="text-xs text-muted-foreground mb-4">When using DeveloperProvider, select which dataset to load into the UI.</p>
            <div className="space-y-3">
              {Object.values(PERSONAS).map(persona => (
                <label key={persona.id} className={cn("flex items-start gap-3 p-3 border rounded-lg cursor-pointer transition-colors", activePersona === persona.id ? "border-emerald-500 bg-emerald-500/5" : "border-border bg-background hover:bg-secondary/50")}>
                  <input 
                    type="radio" 
                    name="persona" 
                    value={persona.id} 
                    checked={activePersona === persona.id}
                    onChange={(e) => setActivePersona(e.target.value)}
                    className="mt-1"
                  />
                  <div>
                    <div className="font-medium text-sm">{persona.name}</div>
                    <div className="text-xs text-muted-foreground">{persona.description}</div>
                  </div>
                </label>
              ))}
            </div>
          </section>
        </div>
      )}

      {activeTab === 'architecture' && (
        <div className="space-y-6">
          <div className="p-6 rounded-xl border border-border bg-card">
             <h2 className="text-lg font-semibold mb-4">System Architecture</h2>
             <div className="bg-secondary/20 p-6 rounded-lg font-mono text-sm border border-border overflow-x-auto">
               <pre className="text-muted-foreground">
{`UI Layer (Mission Control)
   │
   ├─ Zustand (Local UI State)
   ├─ TanStack Query (Server State)
   │
   ▼
[ Provider Resolver ] ───▶ OfflineProvider (IndexedDB)
   │
   ▼
BackendProvider (Network)
   │
   ▼
MissionControlBFF (FastAPI)
   │
   ├─ Auth Middleware
   ├─ Rate Limiting
   │
   ▼
PFOS Platform SDKs
   │
   ├─ execution-policy
   ├─ decision-intelligence
   ├─ financial-ontology
   └─ autonomous-intelligence`}
               </pre>
             </div>
          </div>
        </div>
      )}

      {activeTab === 'telemetry' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
           {[
             { name: 'BFF Connection', status: 'Healthy', icon: Server, color: 'text-emerald-500' },
             { name: 'Event Bus', status: 'Listening', icon: Activity, color: 'text-blue-500' },
             { name: 'Auth Token', status: 'Valid (24h)', icon: Shield, color: 'text-emerald-500' },
             { name: 'Local Cache', status: '4.2 MB', icon: HardDrive, color: 'text-purple-500' },
             { name: 'WebSocket', status: 'Connected', icon: Network, color: 'text-emerald-500' },
           ].map(t => (
             <div key={t.name} className="p-4 rounded-xl border border-border bg-card flex items-center justify-between">
               <div className="flex items-center gap-3">
                 <t.icon className={cn("w-5 h-5", t.color)} />
                 <span className="font-medium text-sm">{t.name}</span>
               </div>
               <span className="text-xs text-muted-foreground font-mono">{t.status}</span>
             </div>
           ))}
        </div>
      )}
    </div>
  );
}

function UserIcon(props: any) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
      <circle cx="12" cy="7" r="4" />
    </svg>
  );
}
