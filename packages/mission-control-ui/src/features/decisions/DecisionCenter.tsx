import { Check, X, ArrowRight, GitBranch } from 'lucide-react';

export function DecisionCenter() {
  const decisions = [
    {
      id: "DEC-2026-001",
      title: "Execute Tax Loss Harvesting Strategy",
      impact: "+$450 to Net Worth",
      confidence: 94,
      status: "PENDING",
      alternatives: 2
    },
    {
      id: "DEC-2026-002",
      title: "Rebalance Tech Portfolio",
      impact: "-5% Risk Exposure",
      confidence: 88,
      status: "PENDING",
      alternatives: 1
    }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center justify-between border-b pb-4 border-gray-200 dark:border-gray-800">
        <h1 className="text-3xl font-bold tracking-tight">Decision Center</h1>
        <div className="text-sm text-gray-500 font-medium">2 Pending Decisions</div>
      </div>

      <div className="space-y-4">
        {decisions.map((decision) => (
          <div key={decision.id} className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 hover:border-blue-300 transition-colors">
            <div className="flex justify-between items-start mb-4">
              <div>
                <p className="text-xs font-mono text-gray-400 mb-1">{decision.id}</p>
                <h2 className="text-xl font-bold">{decision.title}</h2>
              </div>
              <div className="flex space-x-2">
                <button className="p-2 bg-green-100 text-green-700 hover:bg-green-200 rounded-lg transition-colors" title="Approve">
                  <Check size={20} />
                </button>
                <button className="p-2 bg-red-100 text-red-700 hover:bg-red-200 rounded-lg transition-colors" title="Reject">
                  <X size={20} />
                </button>
              </div>
            </div>

            <div className="flex items-center space-x-6 text-sm">
              <div className="flex flex-col">
                <span className="text-gray-500">Expected Impact</span>
                <span className="font-semibold text-green-600">{decision.impact}</span>
              </div>
              <div className="flex flex-col">
                <span className="text-gray-500">AI Confidence</span>
                <span className="font-semibold">{decision.confidence}%</span>
              </div>
              <div className="flex flex-col flex-1 items-end">
                <button className="flex items-center text-blue-600 hover:text-blue-700 font-medium">
                  <GitBranch size={16} className="mr-2" />
                  View {decision.alternatives} Alternatives
                  <ArrowRight size={16} className="ml-1" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
