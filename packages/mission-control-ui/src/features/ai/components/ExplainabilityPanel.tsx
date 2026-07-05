import { useState } from 'react';
import { Shield, Network, FileText, CheckCircle2, ChevronDown, ChevronUp, Brain, Clock } from 'lucide-react';

interface ExplainabilityPanelProps {
  metadata?: Record<string, any>;
}

export function ExplainabilityPanel({ metadata }: ExplainabilityPanelProps) {
  const [expanded, setExpanded] = useState(false);

  if (!metadata || Object.keys(metadata).length === 0) {
    return null;
  }

  const confidence = metadata.confidence || 0;

  return (
    <div className="mt-2 border border-blue-100 dark:border-blue-900/50 rounded-xl overflow-hidden bg-white/50 dark:bg-black/20">
      <button 
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center justify-between p-2 hover:bg-black/5 dark:hover:bg-white/5 transition-colors"
      >
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-1.5 px-2 py-0.5 bg-blue-50 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 rounded-md text-xs font-semibold">
            <CheckCircle2 size={12} />
            {Math.round(confidence * 100)}% Confidence
          </div>
          <span className="text-[10px] text-gray-500 uppercase font-medium tracking-wider">
            AI Explainability Report
          </span>
        </div>
        <div className="text-gray-400">
          {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </div>
      </button>

      {expanded && (
        <div className="p-3 border-t border-gray-100 dark:border-gray-800 space-y-3">
          {metadata.influencing_memories && metadata.influencing_memories.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1">
                <Brain size={12} /> Influencing Memories
              </span>
              <div className="flex flex-col gap-1.5">
                {metadata.influencing_memories.map((mem: any, i: number) => (
                  <div key={i} className="flex flex-col gap-1 text-xs bg-purple-50 dark:bg-purple-900/10 border border-purple-100 dark:border-purple-900/30 p-2 rounded text-gray-700 dark:text-gray-300">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-purple-700 dark:text-purple-400">{mem.type}</span>
                      <span className="text-[10px] bg-purple-200 dark:bg-purple-800/50 px-1.5 rounded">{mem.confidence}% match</span>
                    </div>
                    <span>{mem.content}</span>
                    <span className="text-[10px] text-gray-500">Source: {mem.source} • Reason: {mem.reason}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {metadata.policies && metadata.policies.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1">
                <Shield size={12} /> Applied Policies
              </span>
              <div className="flex flex-wrap gap-1.5">
                {metadata.policies.map((p: string, i: number) => (
                  <span key={i} className="text-xs bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded border border-gray-200 dark:border-gray-700 font-mono text-gray-600 dark:text-gray-400">
                    {p}
                  </span>
                ))}
              </div>
            </div>
          )}

          {metadata.sources && metadata.sources.length > 0 && (
            <div className="space-y-1.5">
              <span className="text-[10px] font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1">
                <Network size={12} /> Knowledge Graph Sources
              </span>
              <div className="flex flex-col gap-1">
                {metadata.sources.map((s: string, i: number) => (
                  <a key={i} href="#" className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-1">
                    <FileText size={10} /> {s}
                  </a>
                ))}
              </div>
            </div>
          )}

          {metadata.active_workspace && (
             <div className="flex items-center justify-between pt-2 border-t border-gray-200 dark:border-gray-800">
               <span className="text-gray-500 flex items-center gap-1"><Clock size={12}/> Snapshot</span>
               <span className="font-mono text-[10px] text-gray-600 dark:text-gray-400">{metadata.active_workspace}</span>
             </div>
          )}
        </div>
      )}
    </div>
  );
}
