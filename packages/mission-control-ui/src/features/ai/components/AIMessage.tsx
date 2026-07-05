import { Bot, User, Loader2, Pause, RotateCw, XCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import type { AITurn } from '../../../store/useAIStore';
import { cn } from '../../../utils/cn';
import { ExplainabilityPanel } from './ExplainabilityPanel';
import { ToolInvocationCard } from './ToolInvocationCard';
import { useState } from 'react';

interface AIMessageProps {
  turn: AITurn;
}

export function AIMessage({ turn }: AIMessageProps) {
  const isUser = turn.role === 'user';
  const isAssistant = turn.role === 'assistant';
  const { isStreaming } = turn;
  const [streamPaused, setStreamPaused] = useState(false);

  if (!isUser && !isAssistant) return null;

  return (
    <div className={cn("flex gap-3", isUser ? "flex-row-reverse" : "flex-row")}>
      {/* Avatar */}
      <div className={cn(
        "w-8 h-8 rounded-full flex items-center justify-center shrink-0 shadow-sm",
        isUser ? "bg-blue-100 text-blue-600 dark:bg-blue-900/50 dark:text-blue-300" : "bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-300"
      )}>
        {isUser ? <User size={16} /> : <Bot size={16} />}
      </div>

      {/* Content */}
      <div className={cn(
        "flex flex-col gap-2 max-w-[85%]",
        isUser ? "items-end" : "items-start"
      )}>
        {/* Text bubble */}
        {turn.content && (
          <div className={cn(
            "px-4 py-2.5 rounded-2xl text-sm shadow-sm border",
            isUser 
              ? "bg-blue-600 text-white border-blue-700 rounded-tr-sm" 
              : "bg-white dark:bg-gray-900 border-gray-200 dark:border-gray-800 text-gray-900 dark:text-gray-100 rounded-tl-sm"
          )}>
            <div className={cn("prose prose-sm dark:prose-invert max-w-none leading-relaxed", isUser && "prose-p:text-white prose-a:text-white")}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {turn.content}
              </ReactMarkdown>
            </div>
            {isAssistant && isStreaming && (
              <div className="flex items-center gap-2 mt-4 pt-3 border-t border-gray-100 dark:border-gray-700">
                 {!streamPaused ? <Loader2 size={12} className="animate-spin text-blue-500" /> : <div className="w-2 h-2 rounded-full bg-amber-500" />}
                 <span className="text-[10px] text-gray-400 uppercase tracking-wider">{streamPaused ? 'Paused' : 'Generating response...'}</span>
                 <div className="ml-auto flex items-center gap-1">
                   <button onClick={() => setStreamPaused(!streamPaused)} className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-gray-600 dark:hover:text-gray-300">
                     {streamPaused ? <RotateCw size={12} /> : <Pause size={12} />}
                   </button>
                   <button className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded text-gray-400 hover:text-red-500">
                     <XCircle size={12} />
                   </button>
                 </div>
              </div>
            )}
          </div>
        )}

        {/* Tools and Approvals */}
        {turn.tool_invocations && turn.tool_invocations.length > 0 && (
          <div className="flex flex-col gap-2 w-full mt-1">
            {turn.tool_invocations.map((tool) => (
              <ToolInvocationCard key={tool.id} tool={tool} turnId={turn.id} />
            ))}
          </div>
        )}

        {/* Explainability / Metadata (Only on Assistant) */}
        {isAssistant && !turn.isStreaming && (turn.content || turn.tool_invocations?.length) && (
          <ExplainabilityPanel metadata={turn.metadata} />
        )}
      </div>
    </div>
  );
}
