import { Wrench, CheckCircle2, XCircle, AlertCircle, Loader2, LayoutDashboard, Pin } from 'lucide-react';
import type { ToolInvocation } from '../../../store/useAIStore';
import { ApprovalCard } from './ApprovalCard';

interface ToolInvocationCardProps {
  tool: ToolInvocation;
  turnId: string;
}

export function ToolInvocationCard({ tool, turnId }: ToolInvocationCardProps) {
  if (tool.tool_name === 'GenerateWidget' && tool.status === 'SUCCESS') {
    return (
      <div className="mt-2 border border-indigo-200 dark:border-indigo-900/50 rounded-xl overflow-hidden bg-white dark:bg-gray-900 w-full max-w-[320px]">
        <div className="flex items-center justify-between p-3 border-b border-gray-100 dark:border-gray-800 bg-indigo-50/50 dark:bg-indigo-900/10">
          <div className="flex items-center gap-2 text-indigo-700 dark:text-indigo-400 font-medium text-xs">
            <LayoutDashboard size={14} />
            Generated Widget: {tool.arguments.title}
          </div>
          <button className="flex items-center gap-1 text-[10px] uppercase font-bold tracking-wider px-2 py-1 bg-indigo-600 hover:bg-indigo-700 text-white rounded transition-colors shadow-sm">
            <Pin size={12} /> Pin
          </button>
        </div>
        <div className="p-4 flex flex-col items-center justify-center bg-gray-50/50 dark:bg-gray-900/50 min-h-[120px]">
           <div className="text-3xl font-bold text-gray-900 dark:text-gray-100 font-mono tracking-tight mb-2">
             {tool.arguments.data?.value || "$12,450.00"}
           </div>
           <div className="text-xs text-emerald-600 dark:text-emerald-400 font-medium px-2 py-0.5 bg-emerald-50 dark:bg-emerald-900/20 rounded-full">
             +14% vs last month
           </div>
           <div className="mt-4 w-full h-8 flex items-end gap-1 px-4">
             {[30, 45, 25, 60, 40, 70, 85].map((h, i) => (
               <div key={i} className="flex-1 bg-indigo-200 dark:bg-indigo-900/40 rounded-t-sm" style={{ height: `${h}%` }} />
             ))}
           </div>
        </div>
      </div>
    );
  }

  const getStatusIcon = () => {
    switch(tool.status) {
      case 'SUCCESS': return <CheckCircle2 size={16} className="text-emerald-500" />;
      case 'ERROR': return <XCircle size={16} className="text-red-500" />;
      case 'PENDING': 
      case 'EXECUTING': return <Loader2 size={16} className="text-blue-500 animate-spin" />;
      case 'REJECTED': return <XCircle size={16} className="text-gray-400" />;
      default: return <AlertCircle size={16} className="text-amber-500" />;
    }
  };

  return (
    <div className="bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden w-full max-w-[320px]">
      <div className="px-3 py-2 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between bg-white dark:bg-gray-900">
        <div className="flex items-center gap-2">
          <Wrench size={14} className="text-gray-400" />
          <span className="text-xs font-mono font-medium text-gray-700 dark:text-gray-300">
            {tool.tool_name}
          </span>
        </div>
        {getStatusIcon()}
      </div>
      
      {tool.requires_approval && tool.status === 'PENDING' && (
        <ApprovalCard tool={tool} turnId={turnId} />
      )}
      
      {(!tool.requires_approval || tool.status !== 'PENDING') && (
        <div className="p-3">
          <div className="text-xs font-mono text-gray-500 bg-white dark:bg-gray-900 border border-gray-100 dark:border-gray-800 rounded p-2 overflow-x-auto break-all">
            {JSON.stringify(tool.arguments)}
          </div>
        </div>
      )}
    </div>
  );
}
