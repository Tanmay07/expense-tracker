import { useState } from 'react';
import { Check, X, AlertTriangle, Info, HelpCircle, ShieldAlert, ArrowRight, ShieldCheck } from 'lucide-react';
import type { ToolInvocation } from '../../../store/useAIStore';
import { useAIStore } from '../../../store/useAIStore';
import { cn } from '../../../utils/cn';

interface ApprovalCardProps {
  tool: ToolInvocation;
  turnId: string;
}

export function ApprovalCard({ tool, turnId }: ApprovalCardProps) {
  const { updateToolStatus } = useAIStore();
  const [showDetails, setShowDetails] = useState(false);

  const handleApprove = () => {
    updateToolStatus(turnId, tool.id, 'EXECUTING');
    setTimeout(() => {
      updateToolStatus(turnId, tool.id, 'SUCCESS', { message: "Action completed successfully.", executed_at: new Date().toISOString() });
    }, 1500);
  };

  const handleReject = () => {
    updateToolStatus(turnId, tool.id, 'REJECTED');
  };
  
  const handleClarify = () => {
    updateToolStatus(turnId, tool.id, 'PENDING');
    // In reality this would trigger a message back to AI
    alert("Clarification requested. AI will now explain this action further.");
  };

  const meta = tool.approval_metadata;
  const level = tool.approval_level || 'ONE_CLICK';
  
  const levelColors = {
    'INFORM_ONLY': 'bg-blue-50 dark:bg-blue-900/10 border-blue-200 dark:border-blue-900',
    'RECOMMENDATION': 'bg-purple-50 dark:bg-purple-900/10 border-purple-200 dark:border-purple-900',
    'ONE_CLICK': 'bg-amber-50 dark:bg-amber-900/10 border-amber-200 dark:border-amber-900',
    'TWO_STEP': 'bg-orange-50 dark:bg-orange-900/10 border-orange-200 dark:border-orange-900',
    'HOUSEHOLD': 'bg-red-50 dark:bg-red-900/10 border-red-200 dark:border-red-900',
  };

  return (
    <div className={cn("p-4 border-t", levelColors[level])}>
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          {level === 'HOUSEHOLD' || level === 'TWO_STEP' ? (
            <ShieldAlert className="text-orange-600 dark:text-orange-500" size={18} />
          ) : (
            <ShieldCheck className="text-amber-600 dark:text-amber-500" size={18} />
          )}
          <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
            {meta?.title || "Action requires approval"}
          </h4>
        </div>
        <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-white/50 dark:bg-black/20 text-gray-600 dark:text-gray-400">
          {level.replace('_', ' ')}
        </span>
      </div>
      
      {meta?.summary && (
        <p className="text-sm text-gray-700 dark:text-gray-300 mb-3">{meta.summary}</p>
      )}

      {showDetails ? (
        <div className="space-y-3 mb-4 text-xs bg-white/60 dark:bg-black/20 p-3 rounded-lg">
          {meta?.reason && (
            <div>
              <span className="font-semibold text-gray-900 dark:text-gray-100 block mb-1">Reason:</span>
              <p className="text-gray-700 dark:text-gray-300">{meta.reason}</p>
            </div>
          )}
          
          <div className="grid grid-cols-2 gap-3">
            {meta?.expected_financial_impact && (
              <div>
                <span className="font-semibold text-gray-900 dark:text-gray-100 block mb-1">Expected Impact:</span>
                <p className="text-emerald-600 dark:text-emerald-400">{meta.expected_financial_impact}</p>
              </div>
            )}
            {meta?.confidence_score && (
              <div>
                <span className="font-semibold text-gray-900 dark:text-gray-100 block mb-1">Confidence:</span>
                <p className="text-blue-600 dark:text-blue-400">{meta.confidence_score}%</p>
              </div>
            )}
          </div>

          {meta?.expected_risks && meta.expected_risks.length > 0 && (
            <div>
              <span className="font-semibold text-orange-700 dark:text-orange-400 flex items-center gap-1 mb-1">
                <AlertTriangle size={12} /> Risks
              </span>
              <ul className="list-disc pl-4 text-gray-700 dark:text-gray-300 space-y-0.5">
                {meta.expected_risks.map((r, i) => <li key={i}>{r}</li>)}
              </ul>
            </div>
          )}
          
          <div>
            <span className="font-semibold text-gray-900 dark:text-gray-100 block mb-1 flex items-center gap-1">
              <Info size={12} /> Technical Payload
            </span>
            <div className="font-mono text-gray-600 dark:text-gray-400 bg-black/5 p-2 rounded break-all">
              {JSON.stringify(tool.arguments)}
            </div>
          </div>
        </div>
      ) : (
        <button 
          onClick={() => setShowDetails(true)}
          className="text-xs text-blue-600 dark:text-blue-400 hover:underline mb-4 flex items-center gap-1"
        >
          View detailed impact and risks <ArrowRight size={12} />
        </button>
      )}

      <div className="flex flex-wrap items-center gap-2">
        {level !== 'INFORM_ONLY' && (
          <button 
            onClick={handleApprove}
            className="flex-1 min-w-[120px] flex items-center justify-center gap-1 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-medium py-2 px-3 rounded-lg shadow-sm transition-all"
          >
            <Check size={14} />
            {level === 'TWO_STEP' ? 'Proceed (Step 1 of 2)' : 'Approve Execution'}
          </button>
        )}
        {level !== 'INFORM_ONLY' && (
          <button 
            onClick={handleReject}
            className="flex-1 min-w-[100px] flex items-center justify-center gap-1 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 text-xs font-medium py-2 px-3 rounded-lg shadow-sm transition-all"
          >
            <X size={14} />
            Reject
          </button>
        )}
        <button 
          onClick={handleClarify}
          className="px-3 py-2 flex items-center justify-center bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 text-gray-600 dark:text-gray-400 transition-all shadow-sm"
          title="Request Clarification"
        >
          <HelpCircle size={14} />
        </button>
      </div>
    </div>
  );
}
